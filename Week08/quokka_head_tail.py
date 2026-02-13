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
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.measure([0], [0])
    return qc


ret = fn_send_to_quokka_and_run(fn_prep_qc(), 100, True)
print(ret)

shots = ret['result']['c']  # Extract the result to count
heads = sum(1 for s in shots if s[0] == 0)   # Count 0 as Head
tails = sum(1 for s in shots if s[0] == 1)   # Count 1 as Tail

print("Heads (0):", heads)
print("Tails (1):", tails)
