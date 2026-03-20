from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import numpy as np

# Build the QFT circuit for 3 qubits
def qft_3qubit():
    qc = QuantumCircuit(3)

    # Qubit 0
    qc.h(0)
    qc.cp(np.pi / 2, 1, 0)   # controlled-P(pi/2)
    qc.cp(np.pi / 4, 2, 0)   # controlled-P(pi/4)

    # Qubit 1
    qc.h(1)
    qc.cp(np.pi / 2, 2, 1)   # controlled-P(pi/2)

    # Qubit 2
    qc.h(2)

    # Swap to reverse qubit order (standard QFT convention)
    qc.swap(0, 2)

    return qc

qc = qft_3qubit()

# Draw the circuit
print("QFT Circuit (3 qubits):")
print(qc.draw(output='text'))

# Compute and print the statevector (starting from |000>)
sv = Statevector.from_label('000')
sv = sv.evolve(qc)

print("\nStatevector after QFT on |000>:")
print(sv)

print("\nAmplitudes (index: amplitude):")
for i, amp in enumerate(sv.data):
    print(f"  |{i:03b}> ({i}): {amp:.6f}")
