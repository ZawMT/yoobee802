import numpy as np


def rref_mod2(M):
    M = M.copy()
    rows, cols = M.shape
    r = 0

    for c in range(cols):
        # find pivot
        pivot = None
        for i in range(r, rows):
            if M[i, c] == 1:
                pivot = i
                break

        if pivot is None:
            continue

        # swap rows
        M[[r, pivot]] = M[[pivot, r]]

        # eliminate other rows
        for i in range(rows):
            if i != r and M[i, c] == 1:
                M[i] ^= M[r]     # XOR row operation

        r += 1
        if r == rows:
            break

    return M


def find_hidden_string(A):
    n = A.shape[1]

    for i in range(1, 2**n):   # skip zero vector
        c = np.array(list(map(int, f"{i:0{n}b}")))
        if np.all((A @ c) % 2 == 0):
            return c


bitstrings = [
    "0010001",
    "1010110",
    "1100101",
    "0011011",
    "0101001",
    "0011010",
    "0110111"
]

A = np.array([[int(b) for b in s] for s in bitstrings], dtype=int)

print(A)

R = rref_mod2(A)
print(R)

hidden = find_hidden_string(A)
print("Hidden string:", hidden)
