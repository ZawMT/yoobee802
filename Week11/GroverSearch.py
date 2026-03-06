# Run this program as ipynb using JupyterLab

import cirq
import math
import numpy as np
from collections import Counter


def generate_grover_oracle_matrix():
    # Number of input qubits
    n = int(input("How many input qubits (n)? ").strip())

    dim = 2 ** n

    print("\nEnter marked states (space separated bitstrings).")
    print(f"Each must be {n} bits long.")
    print("Example: 010 111")

    marked_inputs = input("Marked states: ").strip().split()

    # Convert marked states to integer indices
    marked_indices = set()
    for bitstring in marked_inputs:
        if len(bitstring) != n:
            raise ValueError(f"{bitstring} is not {n} bits long.")
        marked_indices.add(int(bitstring, 2))

    # Create identity matrix
    oracle = np.identity(dim)

    # Flip phase for marked states
    for idx in marked_indices:
        oracle[idx, idx] = -1

    print(oracle)
    return n, oracle


def create_oracle_gate(oracle_matrix):
    return cirq.MatrixGate(oracle_matrix)


def grover_circuit(oracle_gate, n):
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()

    # Step 1: Put into uniform superposition
    circuit.append([cirq.H(q) for q in qubits])

    # Calculating optimal iteration
    N = 2**n
    r = int((math.pi/4) * math.sqrt(N))

    for _ in range(r):
        # Step 2: Apply oracle
        circuit.append(oracle_gate(*qubits))

        # Step 3: Diffusion operator
        circuit.append([cirq.H(q) for q in qubits])
        circuit.append([cirq.X(q) for q in qubits])

        # Multi-controlled Z
        circuit.append(cirq.Z(qubits[-1]).controlled_by(*qubits[:-1]))

        circuit.append([cirq.X(q) for q in qubits])
        circuit.append([cirq.H(q) for q in qubits])

    # Measure
    circuit.append(cirq.measure(*qubits, key='result'))

    return circuit


n, oracle_matrix = generate_grover_oracle_matrix()
oracle_gate = create_oracle_gate(oracle_matrix)

circuit = grover_circuit(oracle_gate, n)

simulator = cirq.Simulator()
result = simulator.run(circuit, repetitions=1)

# Translating the result
# The result format is 111, 100, 011 for 3 repeats and 3 bits -
# It is to be translated as 110 (a group of first bits), 101 (a group of second bits),  101 (a group of third bits)
# Meaning 35% 110 and 70% 101, so the answer is 101
measurements = result.measurements['result']
bitstrings = [''.join(str(bit) for bit in row) for row in measurements]
counts = Counter(bitstrings)
total = sum(counts.values())

print("\nMeasurement statistics:")
for state, count in sorted(counts.items()):
    percentage = 100 * count / total
    print(f"{state} : {percentage:.1f}%")

print("\nCircuit:")
print(circuit)
