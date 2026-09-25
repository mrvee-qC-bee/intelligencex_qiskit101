"""Exercise 3 (fixed) -- Qiskit 2.5.
qiskit.primitives.Sampler (the V1 reference primitive) was deprecated in Qiskit 1.2 and removed in Qiskit 2.0.
V2 differences: the class is StatevectorSampler; run() takes a LIST of PUBs (primitive unified blocs: a circuit
plus its parameters and shots); results are per PUB; counts are read from data.<classical register name>;
there are no quasi-probabilities, you get shots.
Docs: https://quantum.cloud.ibm.com/docs/en/guides/qiskit-1.0-features#qiskit-primitives   (V1 -> V2 table)
      https://quantum.cloud.ibm.com/docs/en/api/qiskit/release-notes/2.0                   (Primitives Upgrade Notes)
      https://quantum.cloud.ibm.com/docs/en/guides/primitives
"""
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

qc = QuantumCircuit(2, 2)      # the classical register is called 'c' -> data.c   (measure_all() would name it 'meas')
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

sampler = StatevectorSampler(seed=42)
job = sampler.run([qc], shots=1024)      # a list of PUBs, even for a single circuit
pub_result = job.result()[0]             # one PubResult per PUB
counts = pub_result.data.c.get_counts()
shots = pub_result.data.c.num_shots
probabilities = {bits: n / shots for bits, n in sorted(counts.items())}
print("counts       :", counts)
print("probabilities:", probabilities)
assert set(counts) <= {"00", "11"}
