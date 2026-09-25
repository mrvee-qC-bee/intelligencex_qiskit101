# Bug bingo -- red-team the chatbot

Mark a square when you can point at the exact line in a bot's output that shows it. Nine squares, each with a one-line tell.
Three in a row = bingo; a full card is common with a 2023-trained model.

| | | |
|---|---|---|
| **Removed function**<br>Tell: `from qiskit import execute` or `Aer.get_backend(...)`. Both gone since Qiskit 1.0 (Feb 2024). Error: `ImportError: cannot import name 'execute' from 'qiskit'`. | **Wrong primitive version**<br>Tell: `from qiskit.primitives import Sampler` / `Estimator`, `sampler.run(qc)` with a bare circuit, or `.quasi_dists`. V1 was removed in Qiskit 2.0; V2 wants `run([pubs])` and `result[0].data.<reg>.get_counts()`. | **No ISA transpile**<br>Tell: `Sampler(mode=backend).run([qc])` with no `generate_preset_pass_manager` in sight. Error: `IBMInputValueError: The instruction h on qubits (0,) is not supported by the target system`. |
| **Session on the Open Plan**<br>Tell: `with Session(...)` anywhere. Docs: "Open Plan users cannot submit session jobs" (server error 1352). Batch or job mode only. | **Old provider**<br>Tell: `IBMQ.load_account()`, `provider.get_backend(...)`, `qiskit_ibm_provider`, `backend.run(...)`, `job_monitor`. Today: `QiskitRuntimeService()` + `service.least_busy(...)` + `SamplerV2`. | **Deprecated Options**<br>Tell: `Options()` with `optimization_level` / `resilience_level` / `execution.shots`, or `Sampler(session=..., options=...)`. Today: `SamplerOptions` / `EstimatorOptions`, `Sampler(mode=...)`, `default_shots`. |
| **Bit order**<br>Tell: `for i, bit in enumerate(bitstring)` treating index 0 as qubit 0, or a sentence like "the first bit is qubit 0". Qiskit is little-endian: qubit 0 is the rightmost character. | **Missing measurement**<br>Tell: a circuit with no `measure`/`measure_all` sent to a Sampler. It runs, warns `... has no output classical registers and so the result will be empty. Did you mean to add measurement instructions?` and returns an empty `DataBin()`. | **Hallucinated method**<br>Tell: something that reads right but does not exist: `result.get_counts()` on a V2 result, `service.get_backend("ibmq_qasm_simulator")` (no cloud simulators on today's platform), `sampler.run(qc, backend=...)`, `channel="ibm_quantum"` (retired 1 July 2025). Check the docs page, not the bot. |

How to use it
1. Live opener: everyone asks their own chatbot the same prompt and marks whichever squares their bot hit. Compare cards across the room.
2. Exercises 1-6: each maps to at least one square (1 removed function; 2 old provider; 3 wrong primitive version; 4 deprecated Options + Session; 5 no ISA transpile; 6 bit order). The two remaining squares appear in the live opener more often than you would like.
3. Twist: ask the bot to fix its own code and mark any square it hits *again*.

Docs to keep open: https://quantum.cloud.ibm.com/docs/en/guides/qiskit-1.0-features , https://quantum.cloud.ibm.com/docs/en/migration-guides/qiskit-runtime ,
https://quantum.cloud.ibm.com/docs/en/guides/execution-modes , https://quantum.cloud.ibm.com/docs/en/guides/transpile , https://quantum.cloud.ibm.com/docs/en/errors
