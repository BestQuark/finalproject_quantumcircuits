import Pkg 
Pkg.develop(path="Jabalizer3")
Pkg.add("PythonCall")
cirq = pyimport("cirq");
using PythonCall
using Jabalizer

circuit_file_name = "groverK.json"
cirq_circuit = cirq.read_json(circuit_file_name)

gates_to_decomp = ["T", "T^-1"];
icm_input = Jabalizer.load_circuit_from_cirq_json("grover2.json")
icm_circuit = Jabalizer.compile(icm_input, gates_to_decomp)

Jabalizer.save_circuit_to_cirq_json(icm_circuit, "icm_output.json");
cirq_circuit = cirq.read_json("icm_output.json")
rm("icm_output.json")
print(cirq_circuit)

n_qubits = Jabalizer.count_qubits(icm_circuit)
state = Jabalizer.zero_state(n_qubits);

print(state)


(g,A,seq) = Jabalizer.to_graph(state)
draw(SVG("grover_graph.svg", 16cm, 16cm), Jabalizer.gplot(g))
