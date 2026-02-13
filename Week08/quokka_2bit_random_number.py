# Run this as ipnyb in JupyterLab

import qiskit.qasm2
import requests
import json
from qiskit.circuit import QuantumCircuit
import warnings
warnings.filterwarnings('ignore')


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


def fn_prep_qc():
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.h(1)
    qc.measure([0, 1], [0, 1])
    return qc


ret = fn_send_to_quokka_and_run(fn_prep_qc(), 100, True)
print(ret)

shots = ret['result']['c']  # Extract the result to count
n_00 = sum(1 for s in shots if s == [0, 0])   # Count 00
n_01 = sum(1 for s in shots if s == [0, 1])   # Count 01
n_10 = sum(1 for s in shots if s == [1, 0])   # Count 10
n_11 = sum(1 for s in shots if s == [1, 1])   # Count 11

print("Number of 00:", n_00)
print("Number of 01:", n_01)
print("Number of 10:", n_10)
print("Number of 11:", n_11)
