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


def generate_oracle_matrix():
    # Ask number of input qubits (n)
    n = int(input("How many input qubits: ").strip())

    # Total qubits = input qubits + 1 helper qubit
    total_qubits = n + 1

    # Number of basis states (e.g 2^2 => 4)
    dim = 2 ** total_qubits

    # Number of function inputs (e.g 2^1 => 2)
    num_inputs = 2 ** n

    print(f"Enter the function values f(x) as 0 or 1:")

    # Read truth table
    f = {}
    for i in range(num_inputs):
        bitstring = format(i, f"0{n}b")   # e.g. 00, 01, 10, 11
        val = int(input(f"f({bitstring}) = ").strip())
        f[i] = val  # Take the output value and keep it first

    # Create empty oracle matrix
    oracle_matrix = np.zeros((dim, dim))

    # Build matrix using |x,y> -> |x, y XOR f(x)>
    for col in range(dim):
        print(f"Col: {col}")
        x = col >> 1        # all bits except last = input register
        y = col & 1         # last bit = helper qubit
        print(f"X: {x}")
        print(f"Y: {y}")
        new_y = y ^ f[x]    # XOR rule
        print(f"New Y: {new_y}")
        row = (x << 1) | new_y
        print(f"Row: {row}")

        print(f"Set: Matrix({row}, {col}) as 1")
        oracle_matrix[row, col] = 1

    return oracle_matrix


# Prompt the user to input the 4x4 unitary matrix
# oracle_matrix = input_unitary_matrix()
oracle_matrix = generate_oracle_matrix()

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
