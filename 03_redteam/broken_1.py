"""Exercise 1 (broken) -- what a 2023-era chatbot writes for the prompt:
   "Write Qiskit code that creates a Bell state and prints the measurement counts from a simulator."
Do not fix this file. Run it, read the traceback, then open fixed_1.py.
"""
from qiskit import QuantumCircuit, execute, Aer
from qiskit.visualization import plot_histogram

qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

backend = Aer.get_backend("qasm_simulator")
job = execute(qc, backend, shots=1024)
result = job.result()
counts = result.get_counts(qc)
print(counts)
plot_histogram(counts)
