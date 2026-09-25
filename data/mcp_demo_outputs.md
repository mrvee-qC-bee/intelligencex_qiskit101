# Raw MCP demo outputs — lecturer fallback for block H

**Source: local MCP servers, run offline on this machine. No IBM Quantum hardware, no account, no QPU time was used.**
**Backend: none — `qiskit-docs-mcp-server` 0.3.0 reads public documentation over HTTPS; `qiskit-mcp-server` 0.3.1 runs Qiskit 2.5.2 locally.**
**Created: 2026-09-24** (docs content as served on that date). **Re-verified 2026-09-24 by an independent check:** the two searches, all three error lookups, `analyze_circuit_tool` and both `transpile_circuit_tool` runs reproduce byte-for-byte; see reliability note 1 for the one behaviour that has drifted.

If the live demo in `../06_mcp_demo.md` fails — no network, client will not start, search endpoint flaky — open this file and read the outputs from here. Every block below is the verbatim stdout of the command shown above it, with only the base64 `circuit_qpy` fields removed.

The commands were issued through a thin stdio client (`qmcp.py`) rather than a chat UI, so the output is the raw JSON the MCP tool returns — which is exactly what the model sees before it writes its answer. Showing the room this JSON is itself a decent demo: *this* is what "the assistant checked the docs" actually means.

---

## Demo step 1 — `search_docs_tool`: "what replaced execute()?"

```
$ qmcp.py search 'execute function removed' 4
```

The first hit is *Qiskit v1.0 feature changes → execute*. That is the page to open on screen. Note the query that works: short keyword phrases retrieve well; long conversational questions sometimes return `status: error` from the search endpoint (see the reliability note at the bottom).

```json
{
    "status": "success",
    "query": "execute function removed",
    "scope": "all",
    "detail": "snippet",
    "results": [
        {
            "id": "docs_section-en-1738",
            "url": "https://quantum.cloud.ibm.com/docs/en/guides/qiskit-1.0-features#execute",
            "title": "execute",
            "pageTitle": "Qiskit v1.0 feature changes",
            "module": "documentation",
            "section": "Guides",
            "snippet": "\u2026primitive is semantically equivalent to the removed qiskit.execute function\u2026"
        },
        {
            "id": "learning_section-en-1219",
            "url": "https://quantum.cloud.ibm.com/learning/en/courses/utility-scale-quantum-computing/utility-iii#12-your-goal",
            "title": "1.2 Your goal",
            "pageTitle": "Utility III",
            "module": "learning",
            "section": "Courses / Utility-scale quantum computing",
            "snippet": "\u2026execute the GHZ circuit using the execute_ghz_fidelity function\u2026"
        },
        {
            "id": "learning_section-en-1226",
            "url": "https://quantum.cloud.ibm.com/learning/en/courses/utility-scale-quantum-computing/utility-iii#5-your-goal-recap",
            "title": "5. Your goal (recap)",
            "pageTitle": "Utility III",
            "module": "learning",
            "section": "Courses / Utility-scale quantum computing",
            "snippet": "\u2026execute the GHZ circuit using the execute_ghz_fidelity function\u2026"
        },
        {
            "id": "docs_section-en-1386",
            "url": "https://quantum.cloud.ibm.com/docs/en/guides/install-c-api#build",
            "title": "Build",
            "pageTitle": "Install the Qiskit C API",
            "module": "documentation",
            "section": "Guides",
            "snippet": "\u2026qiskit.h header with all function declarations in dist/c\u2026"
        }
    ],
    "total_results": 50,
    "returned_results": 4,
    "truncated": true,
    "note": "Showing top 4 of 50 matches. Refine the query for fewer, more relevant results. Showing snippets; call get_page_tool with a result's url for full page content.",
    "metadata": {
        "url": "https://quantum.cloud.ibm.com/endpoints-docs-learning/api/search?query=execute%20function%20removed&module=all",
        "timestamp": "2026-09-23T17:35:11.036147+00:00",
        "content_type": "json"
    }
}
```

---

## Demo step 1b — `search_docs_tool`: "migrate to primitives"

```
$ qmcp.py search 'migrate to primitives' 4
```

Backup query for the same teaching point, and it surfaces the primitives guide plus the V1→V2 migration page. Use this if the first query returns an error.

```json
{
    "status": "success",
    "query": "migrate to primitives",
    "scope": "all",
    "detail": "snippet",
    "results": [
        {
            "id": "docs_section-en-678",
            "url": "https://quantum.cloud.ibm.com/docs/en/errors#:~:text=Error%20code%20registry",
            "title": "Error code registry",
            "pageTitle": "Error code registry",
            "module": "documentation",
            "snippet": "\u2026Migration guide for instructions to migrate to the primitives. 1213\u2026"
        },
        {
            "id": "docs_section-en-1755",
            "url": "https://quantum.cloud.ibm.com/docs/en/guides/qiskit-1.0-features#qiskitprimitives",
            "title": "qiskit.primitives",
            "pageTitle": "Qiskit v1.0 feature changes",
            "module": "documentation",
            "section": "Guides",
            "snippet": "\u2026how to migrate your workflow from primitives V1 to primitives\u2026"
        },
        {
            "id": "docs_section-en-1678",
            "url": "https://quantum.cloud.ibm.com/docs/en/guides/primitives#next-steps",
            "title": "Next steps",
            "pageTitle": "Introduction to primitives",
            "module": "documentation",
            "section": "Guides",
            "snippet": "\u2026primitives. * See the API references. * Read Migrate to V2 primitives\u2026"
        },
        {
            "id": "qiskit-addon-cutting_current_section-en-189",
            "url": "https://quantum.cloud.ibm.com/docs/en/api/qiskit-addon-cutting/release-notes#070",
            "title": "0.7.0",
            "pageTitle": "Circuit cutting release notes",
            "module": "api",
            "section": "Circuit cutting",
            "snippet": "\u2026Runtime primitives. User are encouraged to migrate to v2 primitives\u2026"
        }
    ],
    "total_results": 45,
    "returned_results": 4,
    "truncated": true,
    "note": "Showing top 4 of 45 matches. Refine the query for fewer, more relevant results. Showing snippets; call get_page_tool with a result's url for full page content.",
    "metadata": {
        "url": "https://quantum.cloud.ibm.com/endpoints-docs-learning/api/search?query=migrate%20to%20primitives&module=all",
        "timestamp": "2026-09-23T17:35:17.061770+00:00",
        "content_type": "json"
    }
}
```

---

## Demo step 2 — `lookup_error_code_tool` 1352 (the Open Plan Session error)

```
$ qmcp.py error 1352
```

**This is the headline output of the block.** 1352 is exactly what an Open Plan account gets when a chatbot hands it `with Session(...)` — one of the bug-bingo squares from block E.

```json
{
    "status": "success",
    "code": "1352",
    "details": "1352 | You are not authorized to run a session when using the {} plan. | Create an instance of a different plan type or use a differentexecution mode.",
    "metadata": {
        "url": "https://quantum.cloud.ibm.com/docs/errors#1xxx",
        "timestamp": "2026-09-23T17:35:24.503727+00:00",
        "content_type": "text"
    }
}
```

---

## Demo step 2b — `lookup_error_code_tool` 7001 (the missing-transpile error)

```
$ qmcp.py error 7001
```

The ISA bug, in IBM's own words. Pairs with the "no transpile before hardware" bingo square.

```json
{
    "status": "success",
    "code": "7001",
    "details": "7001 | Instruction {} is not supported. | Remove the instruction shown in the error message. Alternatively, convert the input to conform to the backend's Instruction Set Architecture (ISA).  SeeHello Worldfor an example.",
    "metadata": {
        "url": "https://quantum.cloud.ibm.com/docs/errors#7xxx",
        "timestamp": "2026-09-23T17:35:32.098190+00:00",
        "content_type": "text"
    }
}
```

---

## Demo step 2c — `lookup_error_code_tool` 1217 (session closed)

```
$ qmcp.py error 1217
```

Third in the pocket; only show if someone asks.

```json
{
    "status": "success",
    "code": "1217",
    "details": "1217 | Session has been closed. | Increase the sessionmax_timeif possible, or keep session active by reducing the time between jobs.  For details, see theSession lengthguide.",
    "metadata": {
        "url": "https://quantum.cloud.ibm.com/docs/errors#1xxx",
        "timestamp": "2026-09-23T17:35:38.802866+00:00",
        "content_type": "text"
    }
}
```

---

## Demo step 3 — `analyze_circuit_tool` on a 5-qubit GHZ (QASM3)

```
$ analyze_circuit_tool (GHZ-5)
```

The circuit tools take JSON, so through `qmcp.py` the real form of this and the three calls below is
`qmcp.py call qiskit <tool> '{"circuit": "<the QASM3 at the bottom of this page>", ...}'` —
with `{"optimization_level": 0|3, "basis_gates": "ibm_heron", "coupling_map": "linear"}` added for steps 3c and 3d.

No transpilation at all: this is the circuit *as you wrote it*. Read the `notes` field out loud — the server ships the teaching point for free. (`circuit_qpy`, a long base64 blob, has been stripped from every output on this page for readability.)

```json
{
 "status": "success",
 "circuit_info": {
  "num_qubits": 5,
  "num_clbits": 5,
  "depth": 6,
  "size": 10,
  "width": 10,
  "operation_counts": {
   "h": 1,
   "cx": 4,
   "measure": 5
  },
  "total_operations": 10
 },
 "gate_categories": {
  "single_qubit_gates": 6,
  "two_qubit_gates": 4,
  "multi_qubit_gates": 0
 },
 "notes": [
  "Two-qubit gates are typically the noisiest operations",
  "Circuit depth affects decoherence - lower is better",
  "Consider transpiling with optimization_level=2 or 3 for hardware execution"
 ]
}
```

---

## Demo step 3b — `compare_optimization_levels_tool` on the same GHZ

```
$ compare_optimization_levels_tool (GHZ-5, no coupling map)
```

**The deliberate non-result.** All four levels are identical (depth 6, size 10) because the tool was given no coupling map and no basis gates — there is nothing to route and nothing to decompose. Use this to make the point that "optimization level" is meaningless without a target. Then run the two calls below.

```json
{
 "status": "success",
 "original_circuit": {
  "num_qubits": 5,
  "num_clbits": 5,
  "depth": 6,
  "size": 10,
  "width": 10,
  "operation_counts": {
   "h": 1,
   "cx": 4,
   "measure": 5
  },
  "total_operations": 10
 },
 "optimization_results": {
  "level_0": {
   "depth": 6,
   "size": 10,
   "operation_counts": {
    "h": 1,
    "cx": 4,
    "measure": 5
   },
   "depth_vs_original": 0,
   "size_vs_original": 0
  },
  "level_1": {
   "depth": 6,
   "size": 10,
   "operation_counts": {
    "h": 1,
    "cx": 4,
    "measure": 5
   },
   "depth_vs_original": 0,
   "size_vs_original": 0
  },
  "level_2": {
   "depth": 6,
   "size": 10,
   "operation_counts": {
    "h": 1,
    "cx": 4,
    "measure": 5
   },
   "depth_vs_original": 0,
   "size_vs_original": 0
  },
  "level_3": {
   "depth": 6,
   "size": 10,
   "operation_counts": {
    "h": 1,
    "cx": 4,
    "measure": 5
   },
   "depth_vs_original": 0,
   "size_vs_original": 0
  }
 },
 "recommendation": {
  "best_for_depth": "level_0",
  "note": "Level 2 is recommended for most use cases (balanced compilation time and quality)"
 }
}
```

---

## Demo step 3c — `transpile_circuit_tool`, Heron basis + linear map, **level 0**

```
$ transpile_circuit_tool (GHZ-5, ibm_heron, linear, level 0)
```

Now there is a target. 5 gates became 36 instructions and depth 6 became depth 20. The `improvements` block reports negative "reductions" — the circuit got *bigger*, which is correct and is the point.

```json
{
 "status": "success",
 "original_circuit": {
  "num_qubits": 5,
  "num_clbits": 5,
  "depth": 6,
  "size": 10,
  "width": 10,
  "operation_counts": {
   "h": 1,
   "cx": 4,
   "measure": 5
  },
  "total_operations": 10
 },
 "transpiled_circuit": {
  "num_qubits": 5,
  "num_clbits": 5,
  "depth": 20,
  "size": 36,
  "width": 10,
  "operation_counts": {
   "rz": 18,
   "sx": 9,
   "cz": 4,
   "measure": 5
  },
  "total_operations": 36
 },
 "optimization_level": 0,
 "basis_gates": [
  "id",
  "rz",
  "sx",
  "x",
  "cz",
  "reset"
 ],
 "coupling_map_type": "linear",
 "improvements": {
  "depth_reduction": -14,
  "depth_reduction_percent": -233.33,
  "size_reduction": -26,
  "size_reduction_percent": -260.0
 }
}
```

---

## Demo step 3d — `transpile_circuit_tool`, Heron basis + linear map, **level 3**

```
$ transpile_circuit_tool (GHZ-5, ibm_heron, linear, level 3)
```

Depth 16, size 32 against level 0's 20 and 36: level 3 buys back four layers and four gates. Both are still far above the abstract circuit.

```json
{
 "status": "success",
 "original_circuit": {
  "num_qubits": 5,
  "num_clbits": 5,
  "depth": 6,
  "size": 10,
  "width": 10,
  "operation_counts": {
   "h": 1,
   "cx": 4,
   "measure": 5
  },
  "total_operations": 10
 },
 "transpiled_circuit": {
  "num_qubits": 5,
  "num_clbits": 5,
  "depth": 16,
  "size": 32,
  "width": 10,
  "operation_counts": {
   "rz": 14,
   "sx": 9,
   "cz": 4,
   "measure": 5
  },
  "total_operations": 32
 },
 "optimization_level": 3,
 "basis_gates": [
  "id",
  "rz",
  "sx",
  "x",
  "cz",
  "reset"
 ],
 "coupling_map_type": "linear",
 "improvements": {
  "depth_reduction": -10,
  "depth_reduction_percent": -166.67,
  "size_reduction": -22,
  "size_reduction_percent": -220.0
 },
 "note": "Optimization level 3 provides best results but is slower. Consider level 2 for faster transpilation with good quality."
}
```

---

## The GHZ circuit used in step 3

Paste this into the client when you get to step 3 (or keep it in the clipboard before the block starts):

```
OPENQASM 3.0;
include "stdgates.inc";
qubit[5] q;
bit[5] c;
h q[0];
cx q[0], q[1];
cx q[1], q[2];
cx q[2], q[3];
cx q[3], q[4];
c[0] = measure q[0];
c[1] = measure q[1];
c[2] = measure q[2];
c[3] = measure q[3];
c[4] = measure q[4];
```

---

## Reliability notes from the pre-run (read before going live)

1. **The docs search endpoint is intermittent, and it ranks keywords far better than sentences.** Long conversational queries such as `"what replaced execute in Qiskit 2"` and `"Model Context Protocol MCP server"` returned `{"status":"error","message":"Failed to search documentation for query ..."}` on 2026-09-24; on a re-run the same query returned `status: success` but with irrelevant hits (REST backend configuration, an SML tutorial) and no `qiskit-1.0-features` page at all. Short keyword queries (`"execute function removed"`, `"migrate to primitives"`, `"qiskit code assistant"`) succeed and rank correctly. So the failure mode is *either* an error *or* junk results. **Type keywords, not sentences**, and have the second query ready.
2. **`get_page_tool` never failed** in the pre-run. If search dies mid-demo, pivot to fetching a page directly by path (`guides/qiskit-1.0-features`, `guides/primitives`, `errors`) — it is a better demo anyway, because the model then has the whole page.
3. **`lookup_error_code_tool` never failed** and is the fastest, most reliable step. If you have to cut the block to two minutes, keep this one.
4. **Both circuit tools are fully local** — no network, so they cannot fail because of connectivity. `compare_optimization_levels_tool` runs transpilation four times; on a 5-qubit circuit that is instant, but do not paste a 100-qubit circuit into it live.
5. **The Qiskit MCP servers were not reachable as registered MCP servers in the authoring session** (the executables were not on `PATH` for that client) — they were driven through the stdio client directly. Confirm `uvx qiskit-docs-mcp-server` or the installed console script resolves in *your* shell during the T-1 hour check, not at 1:55 in the room.

---

## Versions used

```
qiskit                       2.5.2
qiskit-docs-mcp-server       0.3.0
qiskit-mcp-server            0.3.1
qiskit-ibm-runtime-mcp-server 0.6.1   (installed, deliberately not used)
mcp                          1.29.0
```
