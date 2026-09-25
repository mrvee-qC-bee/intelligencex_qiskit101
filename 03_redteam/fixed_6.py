"""Exercise 6 (fixed) -- Qiskit 2.5.
Qiskit is little-endian: qubit 0 is the RIGHTMOST character of a bitstring (and the top wire of the drawing).
'001' means q2=0, q1=0, q0=1. Reading a bitstring left-to-right as qubit 0, 1, 2 silently mirrors your answer.
Docs: https://quantum.cloud.ibm.com/learning/en/courses/utility-scale-quantum-computing/bits-gates-and-circuits#note-qiskit-bit-ordering
      https://quantum.cloud.ibm.com/learning/en/courses/use-a-qc-today/quantum-mechanics-basics#a-note-on-the-ordering-of-qubits
"""
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

qc = QuantumCircuit(3)
qc.x(0)
qc.measure_all()
print(qc.draw(output="text"))   # q_0 is the top wire; the 'meas' register numbers show which bit each wire lands in

data = StatevectorSampler(seed=7).run([qc], shots=1000).result()[0].data.meas
counts = data.get_counts()
print("counts:", counts)        # {'001': 1000}: read right-to-left -> q0=1, q1=0, q2=0

# Way 1: reverse the string so that index i is qubit i
bitstring = max(counts, key=counts.get)
flipped = [i for i, bit in enumerate(reversed(bitstring)) if bit == "1"]
print(f"Conclusion (string reversed): qubit {flipped} ended up as 1")

# Way 2: never index strings -- ask the BitArray for one bit at a time
for q in range(3):
    print(f"  qubit {q}: {data.slice_bits(q).get_counts()}")

assert flipped == [0], "qubit 0 was flipped, nothing else"
