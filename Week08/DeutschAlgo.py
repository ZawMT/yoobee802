# Run this as ipnyb in JupyterLab

import cirq
import numpy as np

# Function to create an oracle gate from a given unitary matrix


def create_oracle_gate(oracle_matrix):
    return cirq.MatrixGate(oracle_matrix)

# Function to prompt the user to input a 4x4 unitary matrix


def input_unitary_matrix():
    print("Enter the 16 comma-separated values for the 4x4 unitary matrix:")
    matrix_values = input().strip().split(',')
    oracle_matrix = np.array([[float(matrix_values[i]) for i in range(4)],
                              [float(matrix_values[i]) for i in range(4, 8)],
                              [float(matrix_values[i]) for i in range(8, 12)],
                              [float(matrix_values[i]) for i in range(12, 16)]])
    return oracle_matrix

# Define Deutsch's algorithm


def deutsch_algorithm(oracle_gate):
    # Define qubits
    qubits = cirq.LineQubit.range(2)

    # Create a quantum circuit
    circuit = cirq.Circuit()

    # Apply Hadamard gate to both qubits to create superposition
    circuit.append(cirq.X(qubits[1]))
    circuit.append([cirq.H(q) for q in qubits])

    # Apply the oracle gate
    circuit.append(oracle_gate(*qubits[:2]))

    # Apply Hadamard gate to the first qubit only
    circuit.append(cirq.H(qubits[0]))

    # Measure the first qubit
    circuit.append(cirq.measure(qubits[0], key='result'))

    return circuit


# Prompt the user to input the 4x4 unitary matrix
oracle_matrix = input_unitary_matrix()

# Create the oracle gate from the user-defined unitary matrix
oracle_gate = create_oracle_gate(oracle_matrix)

# Run Deutsch's algorithm with the user-defined oracle gate
circuit = deutsch_algorithm(oracle_gate)

simulator = cirq.Simulator()
measurement_outcomes = []

for _ in range(10):
    result = simulator.run(circuit)
    measurement_outcome = result.measurements['result'][0][0]
    measurement_outcomes.append(measurement_outcome)

# Print all measurement outcomes
print("Measurement outcomes:", measurement_outcomes)

# Determine the type of function based on the measurement outcomes
function_type = "constant" if all(
    outcome == 0 for outcome in measurement_outcomes) else "balanced"
print("Function type:", function_type)

# Print the circuit
print("\nCircuit:")
print(circuit)
