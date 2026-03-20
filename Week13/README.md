## QFT for 3 Qubits
This program shows a fixed implementation QFT for 3 Qubits - intentionally to demonstrate how the QFT is set up for 3 Qubits. For example, the follow segment shows that the first Qubit is applied with Hadamard gate to put in superposition state, and then controlled phase is applied for Pi/2 - 90 degrees - having Qubit 1 as the control and Qubit 0 as the target.
`qc.h(0)
qc.cp(np.pi / 2, 1, 0)
qc.cp(np.pi / 4, 2, 0)`

The similar activity moves on to the next Qubit - Qubit 1, and so on. Finally, the swapping done to order the qubits in reverse - so MSB in the real case will come to first.

The output circuit, statevector and amplitudes will be as follows:
![QFT Output](/QFT-Output.png)
