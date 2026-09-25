"""Exercise 2 (fixed) -- Qiskit 2.5 / qiskit-ibm-runtime 0.49, IBM Quantum Open Plan.
IBMQ, qiskit.providers.ibmq, qiskit-ibm-provider, qiskit.tools.monitor and backend.run() are all gone.
Account -> QiskitRuntimeService (saved once, no token in code); backend -> service.least_busy(); run -> SamplerV2.
Docs: https://quantum.cloud.ibm.com/docs/en/migration-guides/qiskit-runtime-from-ibmq-provider
      https://quantum.cloud.ibm.com/docs/en/migration-guides/qiskit-runtime
      https://quantum.cloud.ibm.com/docs/en/guides/hello-world

RUN_ON_HARDWARE = False keeps this script offline on FakeFez, a local noisy model of the 156-qubit Heron ibm_fez.
Set it True only when you mean to spend your own Open Plan quota (a 2-qubit, 1024-shot job costs a few seconds of QPU).
"""
from qiskit import QuantumCircuit
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime import SamplerV2 as Sampler

RUN_ON_HARDWARE = False

if RUN_ON_HARDWARE:
    from qiskit_ibm_runtime import QiskitRuntimeService
    # Credentials were saved once with QiskitRuntimeService.save_account(channel="ibm_quantum_platform", token=..., instance=...)
    service = QiskitRuntimeService()
    backend = service.least_busy(operational=True, simulator=False, min_num_qubits=2)
else:
    from qiskit_ibm_runtime.fake_provider import FakeFez
    backend = FakeFez()
print(f"Backend: {backend.name}  ({'HARDWARE' if RUN_ON_HARDWARE else 'local fake backend, no QPU time used'})")

# Step 1 -- Map
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

# Step 2 -- Optimize: the QPU only knows rz / sx / x / cz on its own coupling map
pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
isa_circuit = pm.run(qc)
print("ISA ops:", dict(isa_circuit.count_ops()), "| physical qubits used:", isa_circuit.layout.final_index_layout())

# Step 3 -- Execute in job mode (allowed on the Open Plan)
sampler = Sampler(mode=backend)
job = sampler.run([isa_circuit], shots=1024)
print("job id:", job.job_id())

# Step 4 -- Post-process
counts = job.result()[0].data.c.get_counts()
print(counts)
good = counts.get("00", 0) + counts.get("11", 0)
print(f"Fraction of shots in 00/11: {good / 1024:.3f}  (noise pushes this below 1 on a QPU or a fake backend)")
