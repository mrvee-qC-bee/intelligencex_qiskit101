# Red-team the AI -- lecturer answer key

Block E, 25 min. Files: `exercises.md` (full story + verbatim errors), `worksheet.md` (student flow), `bingo_card.md`, `broken_1..6.py`,
`fixed_1..6.py`, `run_all.sh`. Built and executed 2026-09-24 on Qiskit 2.5.2 / qiskit-ibm-runtime 0.49.0 / qiskit-aer 0.17.2;
`bash run_all.sh` -> 12/12 expected verdicts, fixed files clean under `-W error::DeprecationWarning`.

Safety: nothing in this folder can reach IBM Quantum unless someone edits `RUN_ON_HARDWARE = False` to True (fixed_2, broken_4, fixed_4,
broken_5, fixed_5). Say that out loud once. Offline stand-ins: FakeFez (156-qubit Heron model with noise) and AerSimulator.

## Timing and what to say

| Time | Beat | Say / do |
|---|---|---|
| 0:00 | Opener | Everyone prompts their own bot. While they read: "mark the card before you run; the point is that you can already see it." Tally squares on the board. Expect: removed function and old provider from older models; V1 primitives and Session from mid-2024 models; ISA omission from almost all. |
| 0:05 | `run_all.sh` | Project it. Twelve verdicts, one screen. "Five loud failures, one silent one, six fixes. The silent one is the lesson." |
| 0:08 | Exercises | Pairs. Must-do 1, 5, 6. Walk the room with the cascade for Ex 4 in your head (below). |
| 0:20 | Twist | Self-fix with traceback vs self-fix with docs URL. Ask two pairs to read their bot's two fixes aloud. |
| 0:24 | Close | "Map is where the physics is, Optimize is where the bot forgets, Execute is where the plan says no, Post-process is where the endianness bites." Segue: MCP demo if it has its own five minutes (block H), else the QAOA demo (block F). |

## Per-exercise answers

| # | Bug (bingo square) | First real error (verbatim last line) | Pattern step broken | Fix in one line | Docs |
|---|---|---|---|---|---|
| 1 | `execute`, `Aer` (removed function) | `ImportError: cannot import name 'execute' from 'qiskit' (...)` | Execute | `AerSimulator` + pass manager + `SamplerV2(mode=backend).run([isa])` + `result[0].data.c.get_counts()` | guides/qiskit-1.0-features#execute, #aer |
| 2 | `IBMQ`, `qiskit.providers.ibmq`, `qiskit.tools.monitor`, `backend.run` (old provider) | `ImportError: cannot import name 'IBMQ' from 'qiskit' (...)`; on a real backend `IBMBackendError: 'Support for backend.run() has been removed. ...'` | Execute (and account setup) | `QiskitRuntimeService()`, `service.least_busy(operational=True, simulator=False, min_num_qubits=2)`, SamplerV2 | migration-guides/qiskit-runtime-from-ibmq-provider (archived banner), migration-guides/qiskit-runtime, runtime release notes 0.35.0, guides/hello-world |
| 3 | `qiskit.primitives.Sampler`, `run(qc)`, `quasi_dists` (wrong primitive version) | `ImportError: cannot import name 'Sampler' from 'qiskit.primitives' (...). Did you mean: 'compiler'?` | Execute + Post-process | `StatevectorSampler().run([qc], shots=1024)`; `result[0].data.c.get_counts()`; divide by `num_shots` | guides/qiskit-1.0-features#qiskit-primitives, api/qiskit/release-notes/2.0 |
| 4 | `Options` fields, `Session(service=)`, `Sampler(session=)`, `run(qc)`, `quasi_dists`, Session on Open Plan, `channel="ibm_quantum"` (deprecated Options + Session) | `Object has no attribute 'optimization_level' [type=no_such_attribute, input_value=3, input_type=int]` (pydantic ValidationError for OptionsV2) | Optimize (options in the wrong place) + Execute (mode) | `SamplerOptions` (default_shots, DD, twirling), `optimization_level` in the pass manager, `Batch(backend=)` + `Sampler(mode=batch)`, `run([isa])` | guides/execution-modes, guides/run-jobs-batch, guides/runtime-options-overview, guides/sampler-options, errors (1352) |
| 5 | no `generate_preset_pass_manager` (no ISA transpile) | `qiskit_ibm_runtime.exceptions.IBMInputValueError: 'The instruction h on qubits (0,) is not supported by the target system. ...'` | Optimize | `isa_circuit = generate_preset_pass_manager(optimization_level=1, backend=backend).run(qc)` | guides/transpile#instruction-set-architecture, guides/get-started-with-sampler, errors (1517) |
| 6 | `enumerate(bitstring)` read as qubit index (bit order) | none: exit 0, prints `Conclusion: qubit 2 ended up as 1` | Post-process | `reversed(bitstring)` or `data.meas.slice_bits(q).get_counts()` | learning .../bits-gates-and-circuits#note-qiskit-bit-ordering |

All URLs are `https://quantum.cloud.ibm.com/docs/en/` + path (learning pages: `https://quantum.cloud.ibm.com/learning/en/courses/...`).

### The Exercise 4 cascade (memorise; students will ask "and then?")

1. `options.optimization_level = 3` -> `pydantic ValidationError ... Object has no attribute 'optimization_level'` (`Options` is now an alias of `OptionsV2`).
2. `Session(service=service, backend=backend)` -> `TypeError: Session.__init__() got an unexpected keyword argument 'service'`.
3. `Sampler(session=session, options=options)` -> `TypeError: SamplerV2.__init__() got an unexpected keyword argument 'session'` (same for `backend=`).
4. `sampler.run(qc)` -> `ValueError: An invalid Sampler pub-like was given ... wrap it with [] like sampler.run([circuit])`.
5. `sampler.run([qc])` un-transpiled -> the Ex 5 `IBMInputValueError`.
6. `result.quasi_dists` -> `AttributeError: 'PrimitiveResult' object has no attribute 'quasi_dists'`.
7. On the real service, Open Plan: error 1352 "You are not authorized to run a session when using the {} plan." Not demonstrated live (guaranteed failure still counts as a job submission; do not spend the room's quota). Quote the registry: https://quantum.cloud.ibm.com/docs/en/errors.
8. `channel="ibm_quantum"`: runtime release notes -- "the `ibm_quantum` channel is no longer supported from `qiskit-ibm-runtime`" (sunset 1 July 2025); the default today is `ibm_quantum_platform`.

Also worth saying: a `Session(backend=FakeFez())` *works* locally (local testing mode, `session_id` is None). So "it ran on the fake backend" proves nothing about the plan restriction. That is the honest limit of offline testing, the same limit the GHZ block hits with mitigation options ("have no effect in local testing mode" -- students see that exact warning in `fixed_4.py`).

### Reproducing the `backend.run()` message without a network call

```
python -c "from qiskit_ibm_runtime import IBMBackend; IBMBackend.run(None)"
IBMBackendError: 'Support for backend.run() has been removed. Please see our migration guide https://quantum.cloud.ibm.com/docs/migration-guides/qiskit-runtime ...'
```

## Expected outputs of the fixed files (one run, 2026-09-24; counts vary by seed / noise)

- fixed_1: `{'00': 527, '11': 497}` then `OK: Bell state on AerSimulator, only 00 and 11 observed`
- fixed_2: `Backend: fake_fez (local fake backend, no QPU time used)`, `ISA ops: {'rz': 6, 'sx': 3, 'measure': 2, 'cz': 1} | physical qubits used: [0, 1]`, counts with ~3% of shots in 01/10 (noise model), `Fraction of shots in 00/11: 0.972`
- fixed_3: `counts: {'11': 509, '00': 515}`, probabilities 0.503 / 0.497
- fixed_4: `note: Options {...dynamical_decoupling..., twirling...} have no effect in local testing mode.` then counts ~ 50/50 with ~1% leakage
- fixed_5: `Before transpile: {'measure': 2, 'h': 1, 'cx': 1}` / `After transpile : {'rz': 6, 'sx': 3, 'measure': 2, 'cz': 1}` then counts
- fixed_6: circuit drawing, `counts: {'001': 1000}`, `Conclusion (string reversed): qubit [0] ended up as 1`, then per-qubit slices `qubit 0: {'1': 1000}`, `qubit 1: {'0': 1000}`, `qubit 2: {'0': 1000}`

## Likely live-opener outcomes and how to handle them

- Bot writes `execute` + `Aer`: Ex 1 square, ask "how old is the newest fact in this code?" (answer: pre-Feb-2024).
- Bot writes V1 `Sampler` from `qiskit_ibm_runtime` with `Session`: Ex 3 + Ex 4 squares; note `from qiskit_ibm_runtime import Sampler` *imports* today (it is SamplerV2 now) so the failure moves down to `session=` / `run(qc)`.
- Bot writes correct V2 code but no pass manager: Ex 5 square; the most common failure from current-generation models.
- Bot writes correct code including `generate_preset_pass_manager`: run it and check the counts; then ask it for "a session so it is faster" and watch it violate the Open Plan.
- Bot says "I cannot run code": fine, the code is the deliverable; run it yourself.
- No internet / bot down: `run_all.sh` alone carries the block; the six prompts are in `exercises.md`, read them out and let the room predict the bot's answer.

## Scoring reminders

The rubric is in `worksheet.md`. The -3 for "declared fixed without running" is the only negative score; make it visible. If time is short, drop the twist to 3 minutes and skip Ex 2 (its lesson is the same as Ex 1 with a network attached).

## Sources (fetched 2026-09-24 from the docs MCP server)

- https://quantum.cloud.ibm.com/docs/en/guides/qiskit-1.0-features (execute, Aer, IBMQ tooling, V1 -> V2 primitives table)
- https://quantum.cloud.ibm.com/docs/en/migration-guides/qiskit-2.0 (2.0 breaking changes, no execute mention: it was already gone)
- https://quantum.cloud.ibm.com/docs/en/api/qiskit/release-notes/2.0 (Primitives Upgrade Notes: V1 implementations removed)
- https://quantum.cloud.ibm.com/docs/en/migration-guides/qiskit-runtime and .../qiskit-runtime-from-ibmq-provider and .../qiskit-runtime-from-ibm-provider (all three carry the "no longer maintained, archived" banner)
- https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/release-notes (0.35.0 backend.run removed; 0.30.0 session/backend args -> mode; 0.28.0 V1 primitives removed; 0.38.0/0.41.0 ibm_quantum channel sunset 1 July 2025)
- https://quantum.cloud.ibm.com/docs/en/guides/execution-modes ("Open Plan users cannot submit session jobs.")
- https://quantum.cloud.ibm.com/docs/en/guides/runtime-options-overview , https://quantum.cloud.ibm.com/docs/en/guides/sampler-options , https://quantum.cloud.ibm.com/docs/en/guides/run-jobs-batch
- https://quantum.cloud.ibm.com/docs/en/guides/transpile , https://quantum.cloud.ibm.com/docs/en/guides/get-started-with-sampler , https://quantum.cloud.ibm.com/docs/en/guides/hello-world
- https://quantum.cloud.ibm.com/docs/en/errors (1352 session on plan, 1517 non-ISA, 7000 instruction not in basis)
- https://quantum.cloud.ibm.com/learning/en/courses/utility-scale-quantum-computing/bits-gates-and-circuits#note-qiskit-bit-ordering , https://quantum.cloud.ibm.com/learning/en/courses/use-a-qc-today/quantum-mechanics-basics#a-note-on-the-ordering-of-qubits
- https://quantum.cloud.ibm.com/docs/en/guides/changelog-qiskit-code-assistant (29 May 2026: service discontinued, extensions archived, models remain for local use) and https://quantum.cloud.ibm.com/docs/en/guides/qiskit-code-assistant
- https://quantum.cloud.ibm.com/docs/en/guides/estimate-job-run-time (quick usage formula `2 + 0.00035 * <num executions>`)
