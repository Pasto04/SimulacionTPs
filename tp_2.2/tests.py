import numpy as np
from scipy.stats import chisquare, uniform, expon, norm, poisson, binom

class Tests:
    @staticmethod
    def continuous_bins(dist, random_numbers, num_intervals):
        qs = np.linspace(0, 1, num_intervals + 1)
        edges = dist.ppf(qs)
        if not np.isfinite(edges[0]):
            edges[0] = min(random_numbers)
        if not np.isfinite(edges[-1]):
            edges[-1] = max(random_numbers)
        return edges

    @staticmethod
    def observed_frequencies(random_numbers, dist_name, params, num_intervals):
        n = len(random_numbers)

        if dist_name in ('poisson', 'binomial', 'emp_discrete'):
            if dist_name == 'poisson':
                dist = poisson(mu=params['mu'])
                x_min, x_max = min(random_numbers), max(random_numbers)
                values = list(range(x_min, x_max + 1))
            elif dist_name == 'binomial':
                dist = binom(n=params['n'], p=params['p'])
                x_min, x_max = min(random_numbers), max(random_numbers)
                values = list(range(x_min, x_max + 1))
            else:  
                values = params['values']

            observed = np.array([random_numbers.count(x) for x in values])
            return observed, values

        if dist_name == 'uniform':
            dist = uniform(loc=params['a'], scale=params['b'] - params['a'])
        elif dist_name == 'exponential':
            dist = expon(scale=1 / params['lambda'])
        elif dist_name == 'normal':
            dist = norm(loc=params['mu'], scale=params['sigma'])

        edges = Tests.continuous_bins(dist, random_numbers, num_intervals)
        observed, _ = np.histogram(random_numbers, bins=edges)
        return observed, edges


    @staticmethod
    def expected_frequencies(n, dist_name, params, bins=None):
        if dist_name in ('poisson', 'binomial', 'emp_discrete'):
            if dist_name == 'poisson':
                dist = poisson(mu=params['mu'])
            elif dist_name == 'binomial':
                dist = binom(n=params['n'], p=params['p'])
            else:
                probs = np.array(params['probs'])
                return probs * n

            values = bins
            probs = np.array([dist.pmf(x) for x in values])
            return probs * n

        if dist_name == 'uniform':
            dist = uniform(loc=params['a'], scale=params['b'] - params['a'])
        elif dist_name == 'exponential':
            dist = expon(scale=1 / params['lambda'])
        elif dist_name == 'normal':
            dist = norm(loc=params['mu'], scale=params['sigma'])
        else:
            raise ValueError(f"Distribución desconocida: {dist_name}")

        edges = bins
        cdf_vals = dist.cdf(edges)
        probs = np.diff(cdf_vals)
        return probs * n


    @classmethod
    def frequency_test(cls, random_numbers, params, num_intervals=10,
                       alpha=0.05, dist_name=None):
        n = len(random_numbers)

        observed, bins = cls.observed_frequencies(
            random_numbers, dist_name, params, num_intervals
        )
        expected = cls.expected_frequencies(
            n, dist_name, params, bins=bins
        )

        # ddof = # parámetros estimados
        ddof = len(params)

        mask = expected > 0
        observed = observed[mask]
        expected = expected[mask]

        if not np.isclose(observed.sum(), expected.sum()):
            # Reescalar expected para que sumen igual que observed
            expected = expected * (observed.sum() / expected.sum())

        chi2_stat, p = chisquare(f_obs=observed,
                                 f_exp=expected,
                                 ddof=ddof)
        passed = p > alpha
        return chi2_stat, p, passed
