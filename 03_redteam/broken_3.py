"""Exercise 3 (broken) -- what a 2023-era chatbot writes for the prompt:
   "Use the Qiskit Sampler primitive to run the Bell circuit and print the probability of each outcome."
Run it, read the traceback, then open fixed_3.py.
"""
from qiskit import QuantumCircuit
from qiskit.primitives import Sampler

qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

sampler = Sampler()
job = sampler.run(qc, shots=1024)
result = job.result()
quasi_dist = result.quasi_dists[0]
print(quasi_dist.binary_probabilities())
