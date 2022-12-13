import cirq
import random
import matplotlib.pyplot as plt
import numpy as np

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
    circuit.append(cirq.measure(*qubits, key="result"))

    return circuit

xprime = [random.randint(0, 1) for _ in range(nqubits)]

oracle = make_oracle(qubits, ancilla, xprime)
circuit = grover_iteration(qubits, ancilla, oracle)
json_string = cirq.to_json(circuit)

with open("grover.json", "w") as text_file:
    text_file.write(json_string)
