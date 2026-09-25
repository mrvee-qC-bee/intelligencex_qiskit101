"""Exercise 6 (broken, but it RUNS) -- what a chatbot writes for the prompt:
   "Make a 3-qubit circuit, flip qubit 0 with an X gate, measure all qubits, and tell me from the counts which qubit is 1."
Modern imports, no traceback, exit code 0 -- and a wrong answer. Run it, then open fixed_6.py.
"""
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

qc = QuantumCircuit(3)
qc.x(0)              # flip qubit 0
qc.measure_all()

sampler = StatevectorSampler()
counts = sampler.run([qc], shots=1000).result()[0].data.meas.get_counts()
print("counts:", counts)

bitstring = max(counts, key=counts.get)
print("most frequent bitstring:", bitstring)
for i, bit in enumerate(bitstring):
    if bit == "1":
        print(f"Conclusion: qubit {i} ended up as 1")
