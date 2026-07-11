import numpy as np
from maxmin import max_min_composition_numpy

def calculate_P_plus(P):

    P = np.array(P)
    N = P.shape[0]

    P_k = np.copy(P)
    P_plus = np.copy(P)

    for _ in range(1, N):
        P_k = max_min_composition_numpy(P_k, P)
        P_plus = np.maximum(P_plus, P_k)

    return P_plus

def calculate_P_star(P_plus):

    N = P_plus.shape[0]
    P_0 = np.eye(N)
    P_star = np.maximum(P_0, P_plus)
    return P_star

def calculate_r_P(P_plus, D):

    P_plus = np.array(P_plus)
    D = np.array(D)

    if D.ndim == 1:
        D = D.reshape(-1, 1)

    r_P = max_min_composition_numpy(P_plus, D)
    return r_P

if __name__ == '__main__':
    P_matrix = [
        [0.8, 0.5, 0.2],
        [0.4, 0.9, 0.6],
        [0.1, 0.3, 0.7]
    ]

    D_vector = [
        [0.3],
        [0.8],
        [0.5]
    ]

    print("--- Original Matrix P ---")
    print(np.array(P_matrix))
    print("\n" + "=" * 30 + "\n")

    P_plus_result = calculate_P_plus(P_matrix)
    print("--- Result: P^+ (Transitive Closure) ---")
    print(P_plus_result)
    print("\n" + "=" * 30 + "\n")

    P_star_result = calculate_P_star(P_plus_result)
    print("--- Result: P^* (Fuzzy Equivalence Matrix) ---")
    print(P_star_result)
    print("\n" + "=" * 30 + "\n")

    print("--- Vector D ---")
    print(np.array(D_vector))
    print("\n--- Result: r_P = P^+ ∘ D ---")
    r_P_result = calculate_r_P(P_plus_result, D_vector)
    print(r_P_result)