# Reality 2 -- Red-team the AI: six exercises

Block E of the workshop (25 min, hands-on). Environment used to produce every error and every fix below: Qiskit 2.5.2,
qiskit-ibm-runtime 0.49.0, qiskit-aer 0.17.2, Python 3.13, on 2026-09-24. Tracebacks are verbatim from
`bash run_all.sh`; the file paths inside them will be your own on your machine.

Rules of the game
- `broken_N.py` is what a chatbot plausibly writes for the prompt shown. Run it; do not fix it in place.
- `fixed_N.py` is the same task in today's API. Read the docstring first: it links the docs page that explains the change.
- Five files (`fixed_2`, `broken_4`, `fixed_4`, `broken_5`, `fixed_5`) carry a `RUN_ON_HARDWARE = False` switch; only the
  three fixed ones are meant to be flipped at home. Leave it False in the room: offline they use
  FakeFez (a local noisy model of the 156-qubit Heron `ibm_fez`) or AerSimulator and cost zero QPU seconds.
- `bash run_all.sh` runs all twelve files and prints PASS/FAIL against the expected outcome (broken 1-5 must fail,
  broken 6 must run and be wrong, fixed 1-6 must pass with no DeprecationWarning).

The exercises get more modern as you go: 1-3 are pure 2023 Qiskit, 4 is 2023 runtime, 5 is half-updated 2024 code, 6 is
current code with a physics/convention bug. That is deliberate: the further a bot gets, the quieter the failure.

---

## Exercise 1 -- `execute` and `Aer` (removed function)

**Prompt a student types:** "Write Qiskit code that creates a Bell state and prints the measurement counts from a simulator."

**What the bot writes** (`broken_1.py`):
```python
from qiskit import QuantumCircuit, execute, Aer
...
backend = Aer.get_backend("qasm_simulator")
job = execute(qc, backend, shots=1024)
counts = job.result().get_counts(qc)
```

**Real error** (last 3 lines):
```
  File ".../03_redteam/broken_1.py", line 5, in <module>
    from qiskit import QuantumCircuit, execute, Aer
ImportError: cannot import name 'execute' from 'qiskit' (.../site-packages/qiskit/__init__.py)
```
Fix that one name and `Aer` fails next with the same ImportError.

**Fix** (`fixed_1.py`): `AerSimulator` from `qiskit_aer`; `generate_preset_pass_manager(backend=...)` then `pm.run(qc)`;
`SamplerV2(mode=backend).run([isa_circuit], shots=1024)`; counts from `result[0].data.c.get_counts()`.
Same four steps as Qiskit 101 section 5, so the only thing that changes for hardware is the backend object.

**Docs:**
- https://quantum.cloud.ibm.com/docs/en/guides/qiskit-1.0-features#execute -- "The `qiskit.execute` function is not available in Qiskit v1.0."
- https://quantum.cloud.ibm.com/docs/en/guides/qiskit-1.0-features#aer -- "The `qiskit.Aer` object is not available in Qiskit v1.0. Instead, use the same object from the `qiskit_aer` namespace."
- https://quantum.cloud.ibm.com/docs/en/guides/primitives

**Teaching point:** `execute` died in Feb 2024 with Qiskit 1.0; a bot that offers it is quoting a world two major versions old.

---

## Exercise 2 -- `IBMQ` / `qiskit.providers.ibmq` / `backend.run` (old provider)

**Prompt:** "Now change it to run on a real IBM quantum computer using my IBM Quantum account."

**What the bot writes** (`broken_2.py`):
```python
from qiskit import QuantumCircuit, transpile, IBMQ
from qiskit.providers.ibmq import least_busy
from qiskit.tools.monitor import job_monitor
IBMQ.save_account("MY_IBM_QUANTUM_TOKEN")
provider = IBMQ.load_account()
backend = least_busy(provider.backends(filters=...))
...
job = backend.run(transpiled, shots=1024)
```

**Real error** (last 3 lines):
```
  File ".../03_redteam/broken_2.py", line 5, in <module>
    from qiskit import QuantumCircuit, transpile, IBMQ
ImportError: cannot import name 'IBMQ' from 'qiskit' (.../site-packages/qiskit/__init__.py)
```
Every one of the four stale names fails in turn: `qiskit.providers.ibmq` and `qiskit_ibm_provider` give
`ModuleNotFoundError`, `qiskit.tools.monitor` is gone, and on a real `IBMBackend` the last line raises
(reproduced without a network call via `IBMBackend.run(None)`):
```
IBMBackendError: 'Support for backend.run() has been removed. Please see our migration guide
https://quantum.cloud.ibm.com/docs/migration-guides/qiskit-runtime for instructions on how to migrate to the primitives interface.'
```

**Fix** (`fixed_2.py`): `QiskitRuntimeService()` (credentials saved once with `save_account(channel="ibm_quantum_platform", ...)`,
never a token in code), `service.least_busy(operational=True, simulator=False, min_num_qubits=2)`, pass manager,
`SamplerV2(mode=backend)`, `job.job_id()`, counts from `result[0].data.c`. Runs on FakeFez offline; prints the backend and
whether QPU time is being used.

**Docs:**
- https://quantum.cloud.ibm.com/docs/en/migration-guides/qiskit-runtime-from-ibmq-provider -- note the banner: "This guide is no longer maintained. It is archived in GitHub for historical reference only." The bot's world is an archived page.
- https://quantum.cloud.ibm.com/docs/en/migration-guides/qiskit-runtime -- "`backend.run` and `qiskit-ibm-provider`, which only exposed the `backend.run` interface, are no longer supported."
- https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/release-notes -- 0.35.0 (2025-02-04): "Support for `backend.run()` has been removed."
- https://quantum.cloud.ibm.com/docs/en/guides/hello-world -- the canonical current version of this exact task.

**Teaching point:** three provider generations (`IBMQ` -> `qiskit-ibm-provider` -> `qiskit-ibm-runtime`) fit inside one bot's training window; only the last one exists today.

---

## Exercise 3 -- V1 `Sampler` and `quasi_dists` (wrong primitive version)

**Prompt:** "Use the Qiskit Sampler primitive to run the Bell circuit and print the probability of each outcome."

**What the bot writes** (`broken_3.py`):
```python
from qiskit.primitives import Sampler
sampler = Sampler()
job = sampler.run(qc, shots=1024)
quasi_dist = job.result().quasi_dists[0]
print(quasi_dist.binary_probabilities())
```

**Real error** (last 3 lines):
```
  File ".../03_redteam/broken_3.py", line 6, in <module>
    from qiskit.primitives import Sampler
ImportError: cannot import name 'Sampler' from 'qiskit.primitives' (.../site-packages/qiskit/primitives/__init__.py). Did you mean: 'compiler'?
```
If the bot "fixes" only the import to `StatevectorSampler`, two more V1 habits fail: `sampler.run(qc)` ->
`ValueError: An invalid Sampler pub-like was given ... you need to wrap it with [] like sampler.run([circuit])`, and
`result.quasi_dists` -> `AttributeError: 'PrimitiveResult' object has no attribute 'quasi_dists'`.

**Fix** (`fixed_3.py`): `StatevectorSampler(seed=42).run([qc], shots=1024)`; `pub_result = job.result()[0]`;
`counts = pub_result.data.c.get_counts()`; probabilities = counts / `pub_result.data.c.num_shots`.
The register name matters: `QuantumCircuit(2, 2)` gives `data.c`; `measure_all()` gives `data.meas`.

**Docs:**
- https://quantum.cloud.ibm.com/docs/en/guides/qiskit-1.0-features#qiskit-primitives -- migration table: `qiskit.primitives.Sampler` -> `qiskit.primitives.StatevectorSampler`.
- https://quantum.cloud.ibm.com/docs/en/api/qiskit/release-notes/2.0 -- Primitives Upgrade Notes: "Primitive V1 implementations ... deprecated in Qiskit v1.2, have been removed."
- https://quantum.cloud.ibm.com/docs/en/guides/primitives

**Teaching point:** V2 primitives take a list of PUBs (primitive unified blocs: a circuit plus its parameters and shots) and give you shots per PUB, addressed by classical-register name; there are no quasi-probabilities to "fix" any more.

---

## Exercise 4 -- `Options` + `Session` on the Open Plan (deprecated options, forbidden mode)

**Prompt:** "Run the Bell circuit on IBM hardware with error mitigation, and use a session so my jobs don't wait in the queue."

**What the bot writes** (`broken_4.py`, account lines behind the safety switch):
```python
from qiskit_ibm_runtime import QiskitRuntimeService, Session, Sampler, Options
service = QiskitRuntimeService(channel="ibm_quantum")
backend = service.least_busy(operational=True, simulator=False)
options = Options()
options.optimization_level = 3
options.resilience_level = 1
options.execution.shots = 1024
with Session(service=service, backend=backend) as session:
    sampler = Sampler(session=session, options=options)
    job = sampler.run(qc)
    print(job.result().quasi_dists[0])
```

**Real error** (last 3 lines, on FakeFez; the pydantic wording is because `Options` now aliases `OptionsV2`):
```
optimization_level
  Object has no attribute 'optimization_level' [type=no_such_attribute, input_value=3, input_type=int]
    For further information visit https://errors.pydantic.dev/2.13/v/no_such_attribute
```
The full cascade if you fix one line at a time (all reproduced in this environment):
1. `options.optimization_level = 3` -> `pydantic_core._pydantic_core.ValidationError: ... Object has no attribute 'optimization_level'`
2. `Session(service=service, backend=backend)` -> `TypeError: Session.__init__() got an unexpected keyword argument 'service'`
3. `Sampler(session=session, options=options)` -> `TypeError: SamplerV2.__init__() got an unexpected keyword argument 'session'`
4. `sampler.run(qc)` -> `ValueError: An invalid Sampler pub-like was given ... wrap it with []`
5. `sampler.run([qc])` -> the ISA error of Exercise 5
6. `result.quasi_dists` -> `AttributeError: 'PrimitiveResult' object has no attribute 'quasi_dists'`
7. Only the real service can show the last one, so we quote the registry instead: error **1352** "You are not authorized to run a session when using the {} plan." (needs a real backend; on the Open Plan a Session is refused server-side. Not demonstrated live: never spend the room's quota on a guaranteed failure.)
8. Bonus: `channel="ibm_quantum"` was retired on 1 July 2025 (runtime release notes); today's channel is `ibm_quantum_platform`, the default.

**Fix** (`fixed_4.py`): `SamplerOptions()` with `default_shots`, `dynamical_decoupling.enable/sequence_type`, `twirling.enable_gates/enable_measure`
(the Sampler-side error suppression; `resilience_level` is an Estimator option; `optimization_level` goes to the pass manager);
`Batch(backend=backend)` + `SamplerV2(mode=batch, options=options)`; `run([isa_circuit])`. Offline the script prints the expected
note that DD/twirling "have no effect in local testing mode".

**Docs:**
- https://quantum.cloud.ibm.com/docs/en/guides/execution-modes -- "Open Plan users cannot submit session jobs."
- https://quantum.cloud.ibm.com/docs/en/guides/run-jobs-batch
- https://quantum.cloud.ibm.com/docs/en/guides/runtime-options-overview and https://quantum.cloud.ibm.com/docs/en/guides/sampler-options
- https://quantum.cloud.ibm.com/docs/en/errors -- code 1352.
- https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/release-notes -- 0.30.0 (2024-09-23) upgrade notes: "The arguments backend and session for Sampler and Estimator have been removed and replaced with 'mode'".

**Teaching point:** eight lines, eight stale facts; the one that would cost you is invisible locally (Session is refused only by the server), so read the plan page before you read the bot.

---

## Exercise 5 -- `sampler.run([qc])` on a QPU without an ISA circuit (no transpile)

**Prompt:** "Run the Bell circuit on ibm_fez with the SamplerV2 primitive."

**What the bot writes** (`broken_5.py`, account lines behind the switch): correct imports, `Sampler(mode=backend)`, list of circuits -- and no pass manager.

**Real error** (last 3 lines, FakeFez; `validate_isa_circuits` is the same client-side check that runs before any submission to the real `ibm_fez`):
```
    ...<7 lines>...
    )
qiskit_ibm_runtime.exceptions.IBMInputValueError: 'The instruction h on qubits (0,) is not supported by the target system. Circuits that do not match the target hardware definition are no longer supported after March 4, 2024. See the transpilation documentation (https://quantum.cloud.ibm.com/docs/guides/transpile) for instructions to transform circuits and the primitive examples (https://quantum.cloud.ibm.com/docs/guides/primitives-examples) to see this coupled with operator transformations.'
```
Server-side the same rejection is error 1517 "Circuits do not match the target definition (non-ISA circuits)."

**Fix** (`fixed_5.py`): `pm = generate_preset_pass_manager(optimization_level=1, backend=backend); isa_circuit = pm.run(qc)`.
The script prints the backend's basis (`cz, rz, sx, x, measure, ...`), the ops before (`h, cx`) and after (`rz x6, sx x3, cz x1`) and the physical qubits chosen.

**Docs:**
- https://quantum.cloud.ibm.com/docs/en/guides/transpile#instruction-set-architecture -- "When submitting a job to an IBM Quantum backend, the circuits must adhere to the backend's ISA."
- https://quantum.cloud.ibm.com/docs/en/guides/get-started-with-sampler -- "The circuit ... need to be transformed to only use instructions supported by the QPU (referred to as instruction set architecture (ISA) circuits)."
- https://quantum.cloud.ibm.com/docs/en/errors -- codes 1517, 7000.

**Teaching point:** the error message carries its own docs URL; a bot that is given the traceback can fix this one, a bot that is not will keep omitting Step 2.

---

## Exercise 6 -- runs, exits 0, wrong (bit ordering)

**Prompt:** "Make a 3-qubit circuit, flip qubit 0 with an X gate, measure all qubits, and tell me from the counts which qubit is 1."

**What the bot writes** (`broken_6.py`): current API, then
```python
bitstring = max(counts, key=counts.get)          # '001'
for i, bit in enumerate(bitstring):
    if bit == "1":
        print(f"Conclusion: qubit {i} ended up as 1")
```

**Real output** (no traceback, exit code 0):
```
counts: {'001': 1000}
most frequent bitstring: 001
Conclusion: qubit 2 ended up as 1
```
You flipped qubit 0. Qiskit is little-endian: qubit 0 is the rightmost character.

**Fix** (`fixed_6.py`): draw the circuit (q_0 is the top wire, and the `meas` register labels show which bit it lands in); either
`enumerate(reversed(bitstring))` or, without touching strings, `data.meas.slice_bits(q).get_counts()` per qubit
(`qubit 0: {'1': 1000}`, `qubit 1: {'0': 1000}`, `qubit 2: {'0': 1000}`).

**Docs:**
- https://quantum.cloud.ibm.com/learning/en/courses/utility-scale-quantum-computing/bits-gates-and-circuits#note-qiskit-bit-ordering -- "Qiskit uses Little Endian notation ... qubit 0 is the rightmost bit in the bitstrings."
- https://quantum.cloud.ibm.com/learning/en/courses/use-a-qc-today/quantum-mechanics-basics#a-note-on-the-ordering-of-qubits

**Teaching point:** the dangerous bug is the one that runs; a green exit code is not a check, a prediction you made before running is.

---

## Cross-cutting notes

- Every fix uses the same skeleton as Qiskit 101 section 5 and the QAOA demo: Map -> Optimize -> Execute -> Post-process.
  The bots skip Optimize (Ex 5) or never heard of it (Ex 1-4).
- Verbatim outputs of the twelve files on 2026-09-24 are in `bash run_all.sh` (0 unexpected results).
- If a student flips `RUN_ON_HARDWARE = True` in fixed_2/4/5 at home: one 2-qubit, 1024-shot job is about
  `2 + 0.00035 * 1024 = 2.4 s` of QPU by the docs' quick formula (https://quantum.cloud.ibm.com/docs/en/guides/estimate-job-run-time),
  so all three together stay under 10 s of a 10-minute monthly Open Plan allowance. Queue wait, not quota, is the cost.
