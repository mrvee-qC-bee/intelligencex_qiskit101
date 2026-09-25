"""Exercise 4 (broken) -- what a 2023-era chatbot writes for the prompt:
   "Run the Bell circuit on IBM hardware with error mitigation, and use a session so my jobs don't wait in the queue."
Everything below the switch is the bot's code, unchanged. The switch is ours: it swaps the bot's two account
lines for a local fake backend so the script can reach the bot's next bug without touching the network.
Leave it False. Then open fixed_4.py.
"""
from qiskit import QuantumCircuit
from qiskit_ibm_runtime import QiskitRuntimeService, Session, Sampler, Options

RUN_ON_HARDWARE = False          # workshop safety switch (ours) -- keep False
if RUN_ON_HARDWARE:
    service = QiskitRuntimeService(channel="ibm_quantum")             # bot's line ('ibm_quantum' channel was retired 1 July 2025)
    backend = service.least_busy(operational=True, simulator=False)   # bot's line
else:
    from qiskit_ibm_runtime.fake_provider import FakeFez
    service, backend = None, FakeFez()

qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

options = Options()
options.optimization_level = 3
options.resilience_level = 1
options.execution.shots = 1024

with Session(service=service, backend=backend) as session:
    sampler = Sampler(session=session, options=options)
    job = sampler.run(qc)
    result = job.result()
    print(result.quasi_dists[0])
