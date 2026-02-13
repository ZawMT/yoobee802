# Run this as ipnyb in JupyterLab

import qiskit.qasm2
import requests
import json
from qiskit.circuit import QuantumCircuit
import warnings
warnings.filterwarnings('ignore')


def fn_run_on_cirq(repetitions=100, print_circuit=False):
    import cirq
    print("\nRunning on Cirq")
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key='m')
    )
    if print_circuit:
        print(circuit)
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=repetitions)
    hist = result.histogram(key='m')
    counts = {}
    for state, count in hist.items():
        bitstring = format(state, '02b')[::-1]
        counts[bitstring] = count
    return counts


def fn_send_to_quokka_and_run(qc, repetitions=100, print_circuit=False):
    print("\nRunning on Quokka")
    req_str_qasm = 'http://quokka2.quokkacomputing.com/qsim/qasm'

    # If tracing is needed, open the file or uncomment this
    # print(qiskit.qasm2.dumps(qc))
    qiskit.qasm2.dump(qc, "myfile.qasm")
    circuit = qiskit.qasm2.load("myfile.qasm")
    if print_circuit:
        print(circuit)
    code = qiskit.qasm2.dumps(circuit)
    code = code[:14] + code[(14 + 22):]
    data = {
        'script': code,
        'count': repetitions
    }
    result = requests.post(req_str_qasm, json=data, verify=False)
    json_obj = json.loads(result.content)
    return json_obj


def fn_run_on_qiskit(qc, repetitions=100, print_circuit=False):
    from qiskit import transpile
    from qiskit_aer import AerSimulator
    print("\nRunning on Qiskit")
    if print_circuit:
        print(qc)

    # create simulator
    simulator = AerSimulator()

    # transpile circuit
    tqc = transpile(qc, simulator)

    # run with shots (same as repetitions)
    job = simulator.run(tqc, shots=repetitions)

    result = job.result()
    ret = result.get_counts()
    return ret


def fn_prep_qc():
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])
    return qc


run_at = int(
    input("Where to run? \n1: On Quokka \n2: On Qiskit \n3: On Cirq\n"))
match run_at:
    case 1:
        ret = fn_send_to_quokka_and_run(fn_prep_qc(), 100, True)
    case 2:
        ret = fn_run_on_qiskit(fn_prep_qc(), 100, True)
    case 3:
        ret = fn_run_on_cirq(100, True)
print(ret)
