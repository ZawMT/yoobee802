# Run this program as ipynb using JupyterLab

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import numpy as np

# ── QFT ──────────────────────────────────────────────────────────────────────


def qft_3qubit():
    qc = QuantumCircuit(3, name='QFT')

    qc.h(0)
    qc.cp(np.pi / 2, 1, 0)
    qc.cp(np.pi / 4, 2, 0)

    qc.h(1)
    qc.cp(np.pi / 2, 2, 1)

    qc.h(2)

    qc.swap(0, 2)

    return qc

# ── IQFT — built manually ─────────────────────────────────────────────────────


def iqft_manual_3qubit():
    qc = QuantumCircuit(3, name='IQFT (manual)')

    # Reverse the swap first
    qc.swap(0, 2)

    # Undo qubit 2
    qc.h(2)

    # Undo qubit 1
    qc.cp(-np.pi / 2, 2, 1)
    qc.h(1)

    # Undo qubit 0
    qc.cp(-np.pi / 4, 2, 0)
    qc.cp(-np.pi / 2, 1, 0)
    qc.h(0)

    return qc

# ── IQFT — using Qiskit's built-in inverse ────────────────────────────────────


def iqft_builtin_3qubit():
    qft = qft_3qubit()
    iqft = qft.inverse()
    iqft.name = 'IQFT (built-in)'
    return iqft

# ── Demo ──────────────────────────────────────────────────────────────────────


# Start from |000>
initial = Statevector.from_label('000')

print("=" * 60)
print("QFT Circuit:")
qft = qft_3qubit()
print(qft.draw(output='text'))

sv_after_qft = initial.evolve(qft)
print("\nStatevector after QFT on |000>:")
for i, amp in enumerate(sv_after_qft.data):
    print(f"  |{i:03b}> : {amp:.6f}")

# ── Apply manual IQFT to the QFT output ──────────────────────────────────────

print("\n" + "=" * 60)
print("IQFT Manual Circuit:")
iqft_manual = iqft_manual_3qubit()
print(iqft_manual.draw(output='text'))

sv_manual = sv_after_qft.evolve(iqft_manual)
print("\nStatevector after manual IQFT (should recover |000>):")
for i, amp in enumerate(sv_manual.data):
    print(f"  |{i:03b}> : {amp:.6f}")

# ── Apply built-in IQFT to the QFT output ────────────────────────────────────

print("\n" + "=" * 60)
print("IQFT Built-in Circuit:")
iqft_builtin = iqft_builtin_3qubit()
print(iqft_builtin.draw(output='text'))

sv_builtin = sv_after_qft.evolve(iqft_builtin)
print("\nStatevector after built-in IQFT (should recover |000>):")
for i, amp in enumerate(sv_builtin.data):
    print(f"  |{i:03b}> : {amp:.6f}")
