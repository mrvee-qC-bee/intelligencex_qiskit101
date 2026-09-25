"""Exercise 5 (fixed) -- qiskit-ibm-runtime 0.49.
IBM QPUs accept only ISA circuits: instructions from the backend's Target (Heron: rz, sx, x, cz, measure, ...)
on qubit pairs that are physically connected. Since March 2024 the primitives reject anything else, client-side
(IBMInputValueError) and server-side (error 1517). Step 2 of the pattern -- generate_preset_pass_manager -- is not optional.
Docs: https://quantum.cloud.ibm.com/docs/en/guides/transpile#instruction-set-architecture
      https://quantum.cloud.ibm.com/docs/en/guides/get-started-with-sampler
      https://quantum.cloud.ibm.com/docs/en/errors                         (codes 1517, 7000)
"""
from qiskit import QuantumCircuit
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime import SamplerV2 as Sampler

RUN_ON_HARDWARE = False
if RUN_ON_HARDWARE:
    from qiskit_ibm_runtime import QiskitRuntimeService
    service = QiskitRuntimeService()
    backend = service.backend("ibm_fez")
else:
    from qiskit_ibm_runtime.fake_provider import FakeFez
    backend = FakeFez()
print(f"Backend: {backend.name}  ({'HARDWARE' if RUN_ON_HARDWARE else 'local fake backend, no QPU time used'})")
print("Backend basis gates:", sorted(backend.target.operation_names))

qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])
print("Before transpile:", dict(qc.count_ops()))

# Step 2 -- Optimize: this is the line the bot forgot
pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
isa_circuit = pm.run(qc)
print("After transpile :", dict(isa_circuit.count_ops()), "| physical qubits:", isa_circuit.layout.final_index_layout())

sampler = Sampler(mode=backend)
job = sampler.run([isa_circuit], shots=1024)
counts = job.result()[0].data.c.get_counts()
print(counts)
