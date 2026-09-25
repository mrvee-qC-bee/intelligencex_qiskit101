"""Exercise 2 (broken) -- what a 2023-era chatbot writes for the prompt:
   "Now change it to run on a real IBM quantum computer using my IBM Quantum account."
This file dies on its first import line, so it never reaches the network. Do not fix it here; open fixed_2.py.
"""
from qiskit import QuantumCircuit, transpile, IBMQ
from qiskit.providers.ibmq import least_busy
from qiskit.tools.monitor import job_monitor

IBMQ.save_account("MY_IBM_QUANTUM_TOKEN")
provider = IBMQ.load_account()
backend = least_busy(provider.backends(filters=lambda b: b.configuration().n_qubits >= 2
                                       and not b.configuration().simulator
                                       and b.status().operational))
print("Running on", backend.name())

qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

transpiled = transpile(qc, backend, optimization_level=3)
job = backend.run(transpiled, shots=1024)
job_monitor(job)
counts = job.result().get_counts()
print(counts)
