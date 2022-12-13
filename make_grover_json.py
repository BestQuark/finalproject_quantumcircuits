import cirq
import random
import matplotlib.pyplot as plt
import numpy as np
import json
import ast

nqubits = 2
qubits = cirq.LineQubit.range(nqubits)
ancilla = cirq.NamedQubit("Ancilla")

def make_oracle(qubits, ancilla, xprime):
    """Implements the function {f(x) = 1 if x == x', f(x) = 0 if x != x'}."""
    yield (cirq.X(q) for (q, bit) in zip(qubits, xprime) if not bit)
    yield (cirq.TOFFOLI(qubits[0], qubits[1], ancilla))
    yield (cirq.X(q) for (q, bit) in zip(qubits, xprime) if not bit)

def grover_iteration(qubits, ancilla, oracle):
    circuit = cirq.Circuit()
    circuit.append(cirq.H.on_each(*qubits))
    circuit.append([cirq.X(ancilla), cirq.H(ancilla)])
    circuit.append(oracle)
    circuit.append(cirq.H.on_each(*qubits))
    circuit.append(cirq.X.on_each(*qubits))
    circuit.append(cirq.H.on(qubits[1]))
    circuit.append(cirq.CNOT(qubits[0], qubits[1]))
    circuit.append(cirq.H.on(qubits[1]))
    circuit.append(cirq.X.on_each(*qubits))
    circuit.append(cirq.H.on_each(*qubits))

    return circuit

xprime = [random.randint(0, 1) for _ in range(nqubits)]

oracle = make_oracle(qubits, ancilla, xprime)
circuit = grover_iteration(qubits, ancilla, oracle)

def keep_clifford_plus_T(op):
    if isinstance(op.gate, (cirq.XPowGate,
                            cirq.YPowGate,
                            cirq.ZPowGate,
                            cirq.HPowGate,
                            cirq.CNotPowGate,
                            cirq.SwapPowGate
                            )):
        return True

ct_circuit = cirq.Circuit(cirq.decompose(circuit, keep=keep_clifford_plus_T))


json_string = cirq.to_json(ct_circuit)

with open("grover.txt", "w") as text_file:
    text_file.write(repr(json_string))

data = ast.literal_eval(json_string)
with open('groverK.json', 'w') as f:
    json.dump(data, f)