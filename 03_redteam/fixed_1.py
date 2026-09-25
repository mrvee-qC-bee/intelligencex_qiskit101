"""Exercise 1 (fixed) -- Qiskit 2.5 / qiskit-ibm-runtime 0.49.
`qiskit.execute` and `qiskit.Aer` were removed in Qiskit 1.0 (Feb 2024). The replacement is the
Qiskit patterns skeleton used everywhere in this workshop (Qiskit 101 section 5):
  Step 1 Map (build circuit) -> Step 2 Optimize (pass manager) -> Step 3 Execute (Sampler) -> Step 4 Post-process (counts)
Docs: https://quantum.cloud.ibm.com/docs/en/guides/qiskit-1.0-features#execute
      https://quantum.cloud.ibm.com/docs/en/guides/qiskit-1.0-features#aer
      https://quantum.cloud.ibm.com/docs/en/guides/primitives
"""
from qiskit import QuantumCircuit
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler

# Step 1 -- Map
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

# Step 2 -- Optimize: transpile to the backend's instruction set (the simulator accepts h/cx; a QPU would not)
backend = AerSimulator()
pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
isa_circuit = pm.run(qc)

# Step 3 -- Execute: SamplerV2 takes a LIST of PUBs (primitive unified blocs: a circuit plus its parameters and shots).
# Swap AerSimulator() for a QPU later; nothing else changes.
sampler = Sampler(mode=backend)
job = sampler.run([isa_circuit], shots=1024)

# Step 4 -- Post-process: one result per PUB; counts live under the classical register's name ('c' here)
counts = job.result()[0].data.c.get_counts()
print(counts)
assert set(counts) <= {"00", "11"}, "an ideal Bell state only ever gives 00 or 11"
print("OK: Bell state on AerSimulator, only 00 and 11 observed")
