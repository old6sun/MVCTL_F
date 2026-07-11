import numpy as np

def max_min_composition_numpy(A, B):

    return np.max(np.minimum(A[:, :, np.newaxis], B[np.newaxis, :, :]), axis=1)

A = np.array([[0.8, 0.7],
              [0.3, 0.5]])

B = np.array([[0.2, 0.4],
              [0.6, 0.9]])

C_numpy = max_min_composition_numpy(A, B)

print("--- NumPy Operation Result ---")
print(C_numpy)