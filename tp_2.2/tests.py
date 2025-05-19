import numpy as np
from scipy.stats import chisquare, uniform, expon, norm, poisson, binom, kstest, anderson, gamma, nbinom

class Tests:

    @staticmethod
    def continuous_bins(dist, random_numbers, num_intervals):
        qs = np.linspace(0, 1, num_intervals + 1)

        eps = 1e-6
        qs[0] = eps
        qs[-1] = 1 - eps

        edges = dist.ppf(qs)
        edges = np.sort(edges)
        
        if not np.isfinite(edges[0]):
            edges[0] = min(random_numbers)
        if np.isnan(edges[-1]):
            edges[-1] = max(random_numbers)

        return edges

    @staticmethod
    def observed_frequencies(random_numbers, dist_name, params, num_intervals):
        n = len(random_numbers)

        if dist_name in ('poisson', 'binomial', 'empirical_discrete'):
            if dist_name == 'poisson':
                dist = poisson(mu=params['lambda'])
                x_min, x_max = int(min(random_numbers)), int(max(random_numbers))
                values = list(range(x_min, x_max + 1))
            elif dist_name == 'binomial':
                dist = binom(n=params['n'], p=params['p'])
                x_min, x_max = int(min(random_numbers)), int(max(random_numbers))
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
        elif dist_name == 'gamma':
            dist = gamma(a=params['alpha'], scale=params['beta'])
        elif dist_name == 'pascal':
            dist = nbinom(n=params['r'], p=params['p'])

        edges = Tests.continuous_bins(dist, random_numbers, num_intervals)

        observed, _ = np.histogram(random_numbers, bins=edges)
        return observed, edges


    @staticmethod
    def expected_frequencies(n, dist_name, params, bins=None):
        if dist_name in ('poisson', 'binomial', 'empirical_discrete'):
            if dist_name == 'poisson':
                dist = poisson(mu=params['lambda'])
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
        elif dist_name == 'gamma':
            dist = gamma(a=params['alpha'], scale=params['beta'])
        elif dist_name == 'pascal':
            dist = nbinom(n=params['r'], p=params['p'])
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

        mask = expected > 0
        observed = observed[mask]
        expected = expected[mask]

        expected = expected * (observed.sum() / expected.sum())

        chi2_stat, p = chisquare(f_obs=observed,
                                f_exp=expected,
                                ddof=len(params)) # ddof = parámetros estimados
        passed = p > alpha
        return chi2_stat, p, passed

    @staticmethod
    def kolmogorov_smirnov_test(random_numbers, dist_name, params):

        required_keys = {
            'uniform': ['a', 'b'],
            'exponential': ['lambda'],
            'normal': ['mu', 'sigma'],
            'poisson': ['mu'],
            'binomial': ['n', 'p']
        }

        if dist_name not in required_keys:
            raise ValueError(f"KS test no implementado para distribución: {dist_name}")
    
        # Verificar keys de params
        for key in required_keys[dist_name]:
            if key not in params:
                raise KeyError(f"Parámetro '{key}' faltante en params para KS test con distribución '{dist_name}'")

        discrete_dists = ['poisson', 'binomial']
        if dist_name in discrete_dists:
            raise NotImplementedError(f"KS test no es adecuado para distribuciones discretas como '{dist_name}'")

        if dist_name == 'uniform':
            dist = uniform(loc=params['a'], scale=params['b'] - params['a'])
        elif dist_name == 'exponential':
            dist = expon(scale=1 / params['lambda'])
        elif dist_name == 'normal':
            dist = norm(loc=params['mu'], scale=params['sigma'])
        else:
            raise ValueError(f"KS test no implementado para distribución: {dist_name}")

        if dist is None:
            raise ValueError(f"KS test no implementado para distribución: {dist_name}")
        
        # Para distribuciones discretas usar "cdf" o "pmf"
   
        ks_stat, p_value = kstest(random_numbers, dist.cdf)
        return ks_stat, p_value, p_value > 0.05

    @staticmethod
    def anderson_darling_test(random_numbers, dist_name, params):
        # Solo implemento para normal y exponencial, que scipy soporta directo
        if dist_name == 'normal':
            ad_result = anderson(random_numbers, dist='norm')
        elif dist_name == 'exponential':
            ad_result = anderson(random_numbers, dist='expon')
        else:
            raise ValueError(f"AD test solo implementado para 'normal' y 'exponential', no para {dist_name}")
        
        statistic = ad_result.statistic
        # El test devuelve critical values para diferentes alfas, el más común es 5%
        crit_value = ad_result.critical_values[2]  # índice 2 corresponde a 5%
        passed = statistic < crit_value
        return statistic, crit_value, passed

    @classmethod
    def all_tests(cls, random_numbers, params, dist_name, num_intervals=10, alpha=0.05):
        results = {}

        # Test Chi2
        try:
            chi2_stat, chi2_p, chi2_passed = cls.frequency_test(random_numbers, params, num_intervals, alpha, dist_name)
            results['Chi2'] = (chi2_stat, chi2_p, chi2_passed)
        except Exception as e:
            results['Chi2'] = f"Error: {e}"

        # Test KS (solo para distribuciones continuas)
        try:
            ks_stat, ks_p, ks_passed = cls.kolmogorov_smirnov_test(random_numbers, dist_name, params)
            results['KS'] = (ks_stat, ks_p, ks_passed)
        except Exception as e:
            results['KS'] = f"Error: {e}"

        # Test AD (solo para normal y exponencial)
        try:
            ad_stat, ad_crit, ad_passed = cls.anderson_darling_test(random_numbers, dist_name, params)
            results['AD'] = (ad_stat, ad_crit, ad_passed)
        except Exception as e:
            results['AD'] = f"Error: {e}"

        return results