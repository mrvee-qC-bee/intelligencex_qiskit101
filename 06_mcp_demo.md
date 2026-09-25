# Block H — Reality 2b: the Qiskit MCP servers (5 min, lecturer demo)

**Mode:** lecturer screen-shares an MCP-connected client. Students watch. The live script is **4:00 spoken + 60 s slack** in a 5-minute slot; the "No MCP client?" box and the Code Assistant appendix after the close are **handout material, said only if asked**.

**What you will take away**
1. Block E showed you a chatbot confidently writing Qiskit that was deleted in 2024. This block shows the fix.
2. The fix is not a smarter model — it is giving the model a tool that reads the current docs.
3. The same trick works with no MCP client at all: paste the docs URL into the chat.

---

## Setup before the room arrives (do NOT do this live)

```bash
pip install qiskit-mcp-servers              # core servers
pip install "qiskit-mcp-servers[all]"       # everything, incl. community servers
```

Register with Claude Code (one line, shown on screen for 5 seconds):

```bash
claude mcp add qiskit-docs -- uvx qiskit-docs-mcp-server
claude mcp add qiskit -- uvx qiskit-mcp-server
```

For Claude Desktop / Cline, the same thing in `claude_desktop_config.json`:

```json
{ "mcpServers": { "qiskit-docs": { "command": "uvx", "args": ["qiskit-docs-mcp-server"] } } }
```

Requirements: Python 3.10+ (3.11+ recommended). **`qiskit-docs-mcp-server` needs no authentication** — it reads public documentation. Only the Runtime and Transpiler servers want `QISKIT_IBM_TOKEN`, and we do not use those here. Apache 2.0.

What is in the repo (github.com/Qiskit/mcp-servers), one line each:

| Server | What it does | Used today? |
|---|---|---|
| `qiskit-docs-mcp-server` | search docs, fetch any docs page as markdown, look up error codes | **yes** |
| `qiskit-mcp-server` | build / analyse / transpile / serialise circuits locally | **yes** |
| `qiskit-ibm-runtime-mcp-server` | backends and job submission via Runtime (needs a token) | no — we are on Open Plan and not spending quota on a demo |
| Qiskit IBM Transpiler | cloud routing service (AI transpiler passes) | **no** — the workshop's veto: no AI transpiler passes |
| Qiskit Gym (community) | RL-based circuit synthesis | no |

One removed entry worth naming out loud: **the Qiskit Code Assistant MCP server was removed from the repo because IBM discontinued the service.** The handout appendix at the end has the quote (say it only if asked).

**Fallback:** if the live client misbehaves, everything below was run ahead of time and the raw output is in `data/mcp_demo_outputs.md`. Open that file and read from it — the demo still lands.

---

## 0:00 — Frame (20 s)

> "Twenty-five minutes ago your chatbot wrote `from qiskit import execute`. It did that because it learned Qiskit from three-year-old Stack Overflow. The model is not going to get less stale on its own. What fixes it is a tool that lets it *look*."

---

## 0:20 — Step 1: the question that broke the room (80 s)

Type into the MCP client, exactly:

> **what replaced execute() in Qiskit 2? use the qiskit docs server**

**What the audience sees:** the client calls `search_docs_tool`, a tool-call block expands, and among the hits is *Qiskit v1.0 feature changes → execute*. The model then quotes the actual docs text rather than inventing it:

> "The `qiskit.execute` function is not available in Qiskit v1.0. … Instead of `qiskit.execute`, use the `transpile` function followed by `backend.run()`."

*If the hits come back irrelevant:* the docs search endpoint ranks short keyword phrases far better than sentences (see reliability note 1 in `data/mcp_demo_outputs.md`). Say so out loud — it is a real lesson — and re-ask: **search the qiskit docs for "execute function removed"**, which is the query behind the pre-run output.

Say the honest second half yourself, because the page is a v1.0 page: on hardware in 2026 the answer is **not** `backend.run()` — it is `transpile`/`generate_preset_pass_manager` followed by **SamplerV2 or EstimatorV2**. Ask the follow-up live:

> **and what do I use on IBM hardware specifically? check the primitives guide**

**Takeaway:** the tool does not make the model right, it makes the model *checkable*. You still read the page it cites.

---

## 1:40 — Step 2: the error code (60 s)

Type:

> **look up error code 1352**

**What the audience sees:** `lookup_error_code_tool` fires and returns, in about a second:

```
1352 | You are not authorized to run a session when using the {} plan. |
Create an instance of a different plan type or use a different execution mode.
```

This is *the* error code for this room — it is exactly what an Open Plan account gets when the chatbot hands it `with Session(...)`, which is one of the bug-bingo squares from block E. Land the connection out loud.

Two more in the pocket if there is time or a question:

- **7001** — "Instruction {} is not supported. Remove the instruction … or convert the input to conform to the backend's Instruction Set Architecture (ISA)." That is the missing-transpile bug.
- **1217** — "Session has been closed."

**Takeaway:** a four-digit number that means nothing to you is a documented sentence with a documented fix, and the assistant can fetch it faster than you can find the tab.

---

## 2:40 — Step 3: analyse a circuit (60 s)

Paste a 5-qubit GHZ as QASM3 (the text is at the end of `data/mcp_demo_outputs.md`) and type:

> **analyse this circuit, then transpile it for a linear coupling map with ibm_heron basis gates at optimization level 3**

**What the audience sees:** `analyze_circuit_tool` returns structure with no transpilation —

```
depth 6, size 10, {h: 1, cx: 4, measure: 5},
single_qubit_gates 6, two_qubit_gates 4
notes: "Two-qubit gates are typically the noisiest operations"
```

then **one** `transpile_circuit_tool` call gives the hardware answer:

| | depth | size | gates |
|---|---|---|---|
| abstract circuit | 6 | 10 | h 1, cx 4, measure 5 |
| level 3, Heron basis + linear map | 16 | 32 | rz 14, sx 9, cz 4, measure 5 |

> "Your five-gate circuit is a 32-instruction circuit on real hardware, and the depth *went up*, 6 to 16 — 'optimize' here means 'make it executable and then tidy', not 'make it smaller than what you wrote'."

*Cut from the live script, kept as fallback material in `data/mcp_demo_outputs.md` (steps 3b–3d), say only if asked:* `compare_optimization_levels_tool` returns the same numbers at all four levels when no coupling map or basis is given (nothing to route, nothing to decompose), and the level-0 transpile is depth 20 / size 36, so level 3 buys back four gates and four layers of depth.

**Takeaway:** the assistant can run real Qiskit against your circuit, so "how bad is this on hardware?" becomes a question with a number instead of an opinion.

---

## 3:40 — Close (20 s; say this, then hand back)

> "Two realities in this workshop. Reality one: hardware is noisy, so you measure the noise and design around it. Reality two: your AI is stale, so you give it a tool that reads the docs — and you still read them yourself. Those are the same discipline applied to two different unreliable machines."

**4:00 — done.** The last 60 s of the slot is slack for one slow tool call or one question. Everything below this line is handout material: point at it, say it only if asked.

---

## Handout / say only if asked — No MCP client? Do this instead.

> **The 30-second version of everything above, for any plain chatbot:**
>
> 1. Ask your question normally.
> 2. Then paste the docs URL and say: **"check your answer against this page and quote the part you used: https://quantum.cloud.ibm.com/docs/en/guides/primitives"**
> 3. For an error code, paste the code *and* the registry URL: **https://quantum.cloud.ibm.com/docs/en/errors**
> 4. If it cannot browse, paste the page text itself. Models are far better at reading than remembering.
>
> Useful URLs to keep in a note:
> `.../docs/en/guides/primitives` · `.../docs/en/guides/qiskit-1.0-features` · `.../docs/en/errors` · `.../docs/en/guides/hello-world`
>
> This is the *whole* mechanism of MCP, done by hand. MCP just means the model does the pasting.

---

## Handout / say only if asked — Current status of IBM's Qiskit Code Assistant (if you do say it, quote, do not paraphrase)

From the changelog, entry dated **29 May 2026** (https://quantum.cloud.ibm.com/docs/en/guides/changelog-qiskit-code-assistant):

> "**Qiskit Code Assistant service discontinued** — The preview service has been discontinued and the Visual Studio Code and JupyterLab extensions have been archived.
>
> Based on feedback and usage patterns, more users are running Qiskit Code Assistant models locally and working in editor integrations that are already part of their development workflow.
>
> Qiskit Code Assistant models remain available for local use."

And from the guide itself (https://quantum.cloud.ibm.com/docs/en/guides/qiskit-code-assistant):

> "Qiskit Code Assistant currently relies on the model `mistral-small-3.2-24b-qiskit`, built on the Mistral-Small-3.2-24B-Qiskit model."

So: **the hosted service is gone; the models are still open on Hugging Face** (https://huggingface.co/Qiskit) and you can run them locally through Ollama — `ollama run hf.co/Qiskit/Qwen2.5-Coder-14B-Qiskit`. IBM also publishes execution-based benchmarks for Qiskit code generation, Qiskit HumanEval and Qiskit HumanEval Hard (~150 problems, three difficulty levels; the "Hard" variant strips the imports so the model must find the right classes itself).

> "The practical read for this room: there is no magic IBM plugin that writes correct Qiskit for you any more. What there is, is a general chatbot plus the docs — which is exactly the setup you have, and exactly the setup you spent the last half hour learning to distrust productively."

---

## Key takeaway

**An assistant with a docs tool is not smarter, it is accountable.** Every claim comes with a URL you can open, and when it is wrong the page is right there proving it. That is the only property worth demanding from an AI in a field that deprecates an API every eighteen months.

---

## Sources (all fetched 2026-09-24)

- https://github.com/Qiskit/mcp-servers — server list, install commands, client configuration, Apache 2.0, and the removal note: "**Qiskit Code Assistant MCP Server** — previously published as `qiskit-code-assistant-mcp-server`. Removed because the underlying Qiskit Code Assistant service has been discontinued by IBM Quantum."
- https://github.com/Qiskit/mcp-servers/tree/main/qiskit-docs-mcp-server — the three docs tools, "no authentication".
- https://quantum.cloud.ibm.com/docs/en/guides/changelog-qiskit-code-assistant — 29 May 2026 discontinuation entry (quoted above).
- https://quantum.cloud.ibm.com/docs/en/guides/qiskit-code-assistant — current model, Hugging Face + Ollama local install, Qiskit HumanEval benchmarks.
- https://quantum.cloud.ibm.com/docs/en/guides/qiskit-1.0-features — the `execute` removal text quoted in step 1.
- https://quantum.cloud.ibm.com/docs/en/errors — error code registry behind `lookup_error_code_tool`.
- Raw pre-run output of every step above: `data/mcp_demo_outputs.md` (this folder).
