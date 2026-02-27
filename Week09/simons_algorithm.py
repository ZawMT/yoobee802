# Run this program as ipynb using JupyterLab

import cirq
import numpy as np
from collections import Counter

# Define the quantum circuit


def simon_circuit(oracle_gate, num_bits):

    num_qubits = 2 * num_bits
    # Define four qubits
    qubits = cirq.LineQubit.range(num_qubits)

    # Create a quantum circuit
    circuit = cirq.Circuit()

    # Apply Hadamard gate to the first two qubits
    circuit.append([cirq.H(qubits[i]) for i in range(num_bits)])

    # Apply the oracle gate
    circuit.append(oracle_gate(*qubits))

    # Apply Hadamard gate to the first two qubits
    circuit.append([cirq.H(qubits[i]) for i in range(num_bits)])

    # Measure the first two qubits
    circuit.append(
        [cirq.measure(qubits[i], key=f'result_{i}') for i in range(num_bits)])

    return circuit


def generate_simon_oracle():
    # Ask number of input bits
    n = int(input("How many input bits (n)? ").strip())

    # Total qubits = input register + output register
    total_qubits = 2 * n
    dim = 2 ** total_qubits

    print("\nEnter the function values f(x):")
    print(f"(Each output must be a {n}-bit string)\n")

    # Collect mapping dictionary
    f_map = {}
    for i in range(2**n):
        x = format(i, f"0{n}b")
        fx = input(f"f({x}) = ").strip()
        f_map[x] = fx

    # Create empty oracle matrix
    M = np.zeros((dim, dim), dtype=int)

    # Fill matrix using |x,y> -> |x, y XOR f(x)>
    for col in range(dim):

        # split basis index into x and y
        x_int = col >> n
        y_int = col & ((1 << n) - 1)

        x_bits = format(x_int, f"0{n}b")
        fx_bits = f_map[x_bits]

        fx_int = int(fx_bits, 2)
        new_y = y_int ^ fx_int

        row = (x_int << n) | new_y
        M[row, col] = 1

    return n, M


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


# Create the oracle gate from the unitary matrix
num_bits, oracle_matrix = generate_simon_oracle()
oracle_gate = cirq.MatrixGate(oracle_matrix)

# Create the quantum circuit with the oracle gate
circuit = simon_circuit(oracle_gate, num_bits)
# Simulate the circuit 100 times
simulator = cirq.Simulator()
result = simulator.run(circuit, repetitions=100)

# Collect the measurement results
measurements = result.measurements
counts = Counter(tuple(measurements[f'result_{i}'][j][0] for i in range(
    num_bits)) for j in range(100))

# Print the measurement results
print("Measurement results (bitstring: frequency):")
for outcome, frequency in counts.items():
    print(f"{outcome}: {frequency}")

# Print the circuit
print("\nCircuit:")
print(circuit)

bitstrings = ["".join(str(int(b)) for b in outcome)
              for outcome in counts.keys()]
print(bitstrings)

A = np.array([[int(b) for b in s] for s in bitstrings], dtype=int)

print(A)

R = rref_mod2(A)
print(R)

hidden = find_hidden_string(A)
print("Hidden string:", hidden)
