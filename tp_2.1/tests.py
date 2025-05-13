"""
Roulette Simulator:
Dev Team:
    - Cosentino, Lucio Nahuel
    - Danteo, Elías Tomás
    - De Bernardo, Aarón
    - Fernandez Da Silva, Joaquín C.
    - Malizani, Juan Pablo
    - Pastorino, Juan José
"""


from scipy.stats import chi2, chisquare

class Tests:
    
    @classmethod
    def frequency_test(cls, random_numbers, num_intervals=10, alpha=0.05):
        n = len(random_numbers)
        expected_freq = n / num_intervals
        observed_freqs = [0] * num_intervals
        for number in random_numbers:
            index = min(int(number * num_intervals), num_intervals - 1)
            observed_freqs[index] += 1

        chi_squared = sum((obs - expected_freq) ** 2 / expected_freq for obs in observed_freqs)
        df = num_intervals - 1
        critical_value = chi2.ppf(1 - alpha, df)
        passed = chi_squared < critical_value
        return chi_squared, critical_value, passed

    @classmethod
    def runs_test(cls, random_numbers):
        median = sorted(random_numbers)[len(random_numbers) // 2]
        signs = [1 if x >= median else 0 for x in random_numbers]
        runs = 1
        for i in range(1, len(signs)):
            if signs[i] != signs[i - 1]:
                runs += 1
        n1 = signs.count(1)
        n2 = signs.count(0)
        n = n1 + n2
        if n1 == 0 or n2 == 0:
            return runs, None, False
        expected_runs = (2 * n1 * n2) / n + 1
        variance_runs = (2 * n1 * n2 * (2 * n1 * n2 - n)) / (n**2 * (n - 1))
        z = (runs - expected_runs) / (variance_runs ** 0.5)
        passed = abs(z) < 1.96
        return runs, expected_runs, passed

    @classmethod
    def reverse_arrangements_test(cls, random_numbers):
        def merge_count(arr):
            if len(arr) < 2:
                return arr, 0
            mid = len(arr)//2
            left, inv_l = merge_count(arr[:mid])
            right, inv_r = merge_count(arr[mid:])
            merged, inv_split = [], 0
            i = j = 0
            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    merged.append(left[i]); i += 1
                else:
                    merged.append(right[j]); j += 1
                    inv_split += len(left) - i
            merged += left[i:] + right[j:]
            return merged, inv_l + inv_r + inv_split

        _, inversions = merge_count(random_numbers)
        n = len(random_numbers)
        expected = n * (n - 1) / 4
        var = n * (n - 1) * (2 * n + 5) / 72
        z = (inversions - expected) / (var ** 0.5)
        passed = abs(z) < 1.96
        return inversions, expected, passed

    @classmethod
    def overlapping_sums_test(cls, random_numbers, window_size=5):
        n = len(random_numbers)
        sums = [sum(random_numbers[i:i+window_size]) for i in range(n - window_size + 1)]
        expected_mean = window_size * 0.5
        sample_mean = sum(sums) / len(sums)
        std_dev = (window_size / 12) ** 0.5
        z = (sample_mean - expected_mean) / (std_dev / len(sums) ** 0.5)
        passed = abs(z) < 1.96
        return sample_mean, expected_mean, passed


    @classmethod
    def poker_test(cls, random_numbers, num_digits = 5, alpha = 0.5):
        digit_senteces = [f"{int(x * (10 ** num_digits)):05d}" for x in random_numbers]
       
        observed_values = {
            'Todos diferentes': 0,
            'Un par': 0,
            'Dos pares': 0,
            'Trio': 0,
            'Full': 0,
            'Poker': 0,
            'Quintilla': 0
        }
        for seq in digit_senteces:
            count = {}
            for d in seq:
                count[d] = count.get(d, 0) + 1
                freq = sorted(count.values(), reverse=True)

            if freq == [5] : observed_values['Quintilla'] += 1
            elif freq == [4,1] : observed_values['Poker'] += 1
            elif freq == [3,2] : observed_values['Full'] += 1
            elif freq == [3,1,1] : observed_values['Trio'] += 1
            elif freq == [2,2,1] : observed_values['Dos pares'] += 1
            elif freq == [2,1,1,1] : observed_values['Un par'] += 1
            else: observed_values['Todos diferentes'] += 1

        #Probabilidades esperadas
        total = len(random_numbers)
        expected_values = { 
            'Todos diferentes': total * 0.3024,
            'Un par': total * 0.5040,
            'Dos pares': total * 0.1080,
            'Trio': total * 0.0720,
            'Full': total * 0.009,
            'Poker': total * 0.0045,
            'Quintilla': total * 0.0001
        }


        observed_list = [observed_values[cat] for cat in observed_values]
        expected_list = [expected_values[cat] for cat in expected_values]

        chi_sq, p_value = chisquare(observed_list, f_exp=expected_list)

        return {
            'patterns' : observed_values, 
            'passed' : p_value > alpha,
        }

