"""Exercise 4 (fixed) -- qiskit-ibm-runtime 0.49 on the IBM Quantum Open Plan.
What changed since the bot's training data:
  * The V1 `Options` class is gone (the name now aliases OptionsV2, which has none of the old fields). Use
    SamplerOptions / EstimatorOptions or a dict. Sampler has no resilience_level -- that is an Estimator option;
    Sampler-side error suppression is dynamical decoupling + twirling. optimization_level belongs to the transpiler.
  * Sampler(session=..., backend=...) became Sampler(mode=...); Session(service=...) is gone.
  * Open Plan users cannot submit session jobs (server error 1352). Use job mode or Batch mode.
  * run() takes a list of ISA circuits; results have no quasi_dists.
Docs: https://quantum.cloud.ibm.com/docs/en/guides/execution-modes           ("Open Plan users cannot submit session jobs.")
      https://quantum.cloud.ibm.com/docs/en/guides/run-jobs-batch
      https://quantum.cloud.ibm.com/docs/en/guides/runtime-options-overview
      https://quantum.cloud.ibm.com/docs/en/guides/sampler-options
      https://quantum.cloud.ibm.com/docs/en/errors                         (code 1352)
"""
import warnings
from qiskit import QuantumCircuit
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime import Batch, SamplerV2 as Sampler, SamplerOptions

RUN_ON_HARDWARE = False
if RUN_ON_HARDWARE:
    from qiskit_ibm_runtime import QiskitRuntimeService
    service = QiskitRuntimeService()                      # channel defaults to "ibm_quantum_platform"
    backend = service.least_busy(operational=True, simulator=False, min_num_qubits=2)
else:
    from qiskit_ibm_runtime.fake_provider import FakeFez
    backend = FakeFez()
print(f"Backend: {backend.name}  ({'HARDWARE' if RUN_ON_HARDWARE else 'local fake backend, no QPU time used'})")

qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

# optimization_level lives in the transpiler, not in the primitive options
pm = generate_preset_pass_manager(optimization_level=3, backend=backend)
isa_circuit = pm.run(qc)

options = SamplerOptions()
options.default_shots = 1024
options.dynamical_decoupling.enable = True
options.dynamical_decoupling.sequence_type = "XY4"
options.twirling.enable_gates = True
options.twirling.enable_measure = True

# Batch mode is allowed on the Open Plan; Session mode is not.
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    with Batch(backend=backend) as batch:
        sampler = Sampler(mode=batch, options=options)
        job = sampler.run([isa_circuit])
        counts = job.result()[0].data.c.get_counts()
for w in caught:
    # Offline you will see that DD/twirling "have no effect in local testing mode" -- expected: fake backends ignore them.
    print("note:", w.message)
print("job id:", job.job_id())
print(counts)
