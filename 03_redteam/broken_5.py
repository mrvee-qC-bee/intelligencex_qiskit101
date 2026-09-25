"""Exercise 5 (broken) -- what a half-updated chatbot writes for the prompt:
   "Run the Bell circuit on ibm_fez with the SamplerV2 primitive."
It knows SamplerV2 and mode=, but skipped Step 2 (Optimize): the circuit is sent with h/cx gates the QPU does not have.
Behind the switch: FakeFez, the local model of ibm_fez. The ISA check that rejects this circuit is the same client-side
validation qiskit-ibm-runtime performs before it would submit to the real ibm_fez. Leave the switch False. See fixed_5.py.
"""
from qiskit import QuantumCircuit
from qiskit_ibm_runtime import SamplerV2 as Sampler

RUN_ON_HARDWARE = False          # workshop safety switch (ours) -- keep False
if RUN_ON_HARDWARE:
    from qiskit_ibm_runtime import QiskitRuntimeService
    service = QiskitRuntimeService()          # bot's line
    backend = service.backend("ibm_fez")      # bot's line
else:
    from qiskit_ibm_runtime.fake_provider import FakeFez
    backend = FakeFez()

qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

sampler = Sampler(mode=backend)
job = sampler.run([qc], shots=1024)
print(job.result()[0].data.c.get_counts())
