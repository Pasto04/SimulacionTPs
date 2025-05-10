import numpy as np

def chi_squared_critical_value(df, alpha=0.05):
    critical_values = {
        1: 3.841, 2: 5.991, 3: 7.815, 4: 9.488, 5: 11.070,
        6: 12.592, 7: 14.067, 8: 15.507, 9: 16.919, 10: 18.307,
    }
    return critical_values.get(df, None)

def frequency_test(random_numbers, num_intervals=10, alpha=0.05):
    n = len(random_numbers)
    expected_freq = n / num_intervals
    observed_freqs = [0] * num_intervals
    for number in random_numbers:
        index = min(int(number * num_intervals), num_intervals - 1)
        observed_freqs[index] += 1
    chi_squared = sum((obs - expected_freq) ** 2 / expected_freq for obs in observed_freqs)
    critical_value = chi_squared_critical_value(num_intervals - 1, alpha)
    passed = chi_squared < critical_value if critical_value else False
    return chi_squared, critical_value, passed

def runs_test(random_numbers):
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

def reverse_arrangements_test(random_numbers):
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

def overlapping_sums_test(random_numbers, window_size=5):
    n = len(random_numbers)
    sums = [sum(random_numbers[i:i+window_size]) for i in range(n - window_size + 1)]
    expected_mean = window_size * 0.5
    sample_mean = sum(sums) / len(sums)
    std_dev = (window_size / 12) ** 0.5
    z = (sample_mean - expected_mean) / (std_dev / len(sums) ** 0.5)
    passed = abs(z) < 1.96
    return sample_mean, expected_mean, passed

def binary_rank_test(random_numbers, matrix_size=32):
    matrices = []
    bits = [int(x * (2**32)) for x in random_numbers]
    while len(bits) >= matrix_size * matrix_size:
        matrix = np.zeros((matrix_size, matrix_size), dtype=np.uint8)
        for i in range(matrix_size):
            val = bits.pop(0)
            for j in range(matrix_size):
                matrix[i][j] = (val >> (31 - j)) & 1
        matrices.append(matrix)

    rank_counts = {matrix_size: 0, matrix_size - 1: 0, 'lower': 0}
    for m in matrices:
        rank = np.linalg.matrix_rank(m)  # over real field
        if rank == matrix_size:
            rank_counts[matrix_size] += 1
        elif rank == matrix_size - 1:
            rank_counts[matrix_size - 1] += 1
        else:
            rank_counts['lower'] += 1

    # Approximate expected proportions for uniform RNGs
    total = sum(rank_counts.values())
    if total == 0:
        return rank_counts, False

    expected = {
        matrix_size: 0.2888,
        matrix_size - 1: 0.5776,
        'lower': 0.1336
    }

    chi_sq = sum(
        ((rank_counts[k] - expected[k]*total) ** 2) / (expected[k]*total)
        for k in expected
    )
    passed = chi_sq < 5.99  # df=2
    return rank_counts, passed
