def sum_of_squares_slow(N):
    total = N
    for i in range(1, N + 1):
        total += i ** 2
    return total

def sum_of_squares_fast(N):
    return N * (N + 1) * (2 * N + 1) // 6