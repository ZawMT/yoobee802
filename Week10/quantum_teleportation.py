# Run this program as ipynb using JupyterLab

from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram, plot_state_city
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
import math
# Uncomment this to see diagrams when running in a notebook
%matplotlib inline

# Set up the quantum registers and classical registers
alice = QuantumRegister(1, name='alice')
ep = QuantumRegister(1, name='ep')
bob = QuantumRegister(1, name='bob')

alice_c = ClassicalRegister(1, name='alicec')
ep_c = ClassicalRegister(1, name='epc')
bob_c = ClassicalRegister(1, name='bobc')

# Create a quantum circuit with the registers
qc = QuantumCircuit(alice, ep, bob, alice_c, ep_c, bob_c)

# Step 1: Entangle the qubits (ep and bob) in the entanglement pair
qc.h(ep)        # Apply Hadamard gate to create superposition on ep
qc.cx(ep, bob)  # Apply CNOT gate to entangle ep with bob
qc.barrier()

# Step 2: Prepare alice qubit state (this is the state to be teleported)
# Begin state preparation: H → X → RY(45)
qc.h(alice)
qc.x(alice)
qc.ry(math.radians(45), alice)
qc.barrier()

# Step 3: Perform Bell basis measurement between alice and ep
qc.cx(alice, ep)  # Apply CNOT with alice as control and ep as target
qc.h(alice)       # Apply Hadamard to alice qubit
qc.measure(alice, alice_c)  # Measure alice qubit
qc.measure(ep, ep_c)        # Measure the entanglement qubit ep
qc.barrier()

# Step 4: Apply conditional operations on bob qubit based on measurement results
with qc.if_test((alice_c, 1)):
    qc.z(bob)
with qc.if_test((ep_c, 1)):
    qc.x(bob)

# Step 5: Verify bob qubit
# Inverse state prep: RY(-45) → X → H (reverse order)
qc.ry(math.radians(-45), bob)
qc.x(bob)
qc.h(bob)
qc.measure(bob, bob_c)  # Measure bob qubit to verify teleportation

# Execute the quantum circuit on a simulator
simulator = AerSimulator()
# Simulate the circuit
job = simulator.run(qc, shots=10000)

# Get the result
result = job.result()

# Get and print the measurement results
counts = result.get_counts(qc)
print('Measurement outcomes:', counts)
# Analyze how many times bob was 0 - since after doing the inverse operation, state should be back to |0>
successful_count = 0
for key, val in counts.items():
    bob_result, ep_result, alice_result = (int(bit) for bit in key.split())
    if bob_result == 0:
        successful_count += val

total_shots = sum(counts.values())  # Total number of shots

# Calculate the percentage of successful teleportations
success_percentage = (successful_count / total_shots) * 100

print(
    f"Occurrences where bob is 0: {successful_count} out of {total_shots} shots")
print(f"Success percentage: {success_percentage:.2f}%")

# Draw the quantum circuit for visualization
# Use 'mpl' for a better graphical representation (if in a Jupyter notebook)
qc.draw(output='mpl')
