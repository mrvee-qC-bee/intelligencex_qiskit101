# Intro to Quantum and Qiskit: hands-on notebooks

**IntelligenceX 2026 · National University of Singapore**
Instructor: Vishal Bajpe

These are the notebooks and exercises for the hands-on half of the *Introduction to Quantum and Qiskit* session. The first hour is slides; the remaining two hours are spent in this folder. Everything runs on the free **IBM Quantum Open Plan** and Qiskit 2.5.

## What's in this folder

| File | What it is |
|---|---|
| `00_setup_check.ipynb` | Run this **before the workshop**. Checks your Qiskit install, saves your IBM Quantum credentials, lists the QPUs you can reach, and runs a Bell state locally. |
| `01_qiskit101_gates.ipynb` | The main notebook. Single-qubit gates on the QSphere, a multi-qubit quiz (Bell and GHZ states), then nine circuits on a real IBM quantum computer using the four-step Qiskit pattern (Map, Optimize, Execute, Post-process). Section 6 is an optional error-mitigation demo. |
| `01_qiskit101_gates_SOLUTION.ipynb` | The same notebook with the answers filled in and outputs from a real run on `ibm_fez`. Open it after you have tried the exercises yourself. |
| `03_redteam/` | *Red-team the AI.* Ask your chatbot for Qiskit code, spot the stale APIs, and fix them against the docs. Start with `worksheet.md` and `bingo_card.md`; `run_all.sh` runs all twelve scripts at once. No QPU time needed. |
| `06_mcp_demo.md` | Script for the Qiskit MCP servers demo: how to give an AI assistant access to the live Qiskit docs. `data/mcp_demo_outputs.md` has the outputs if you want to read along. |
| `data/` | Pre-run results and figures the notebooks load, including counts from a real `ibm_fez` job so nobody has to wait on a queue. |

## Before you arrive

1. **IBM Quantum account.** Sign up on IBM Cloud, create an **Open Plan** instance, and copy its CRN and an API key. Guide: https://quantum.cloud.ibm.com/docs/guides/cloud-setup
2. **Python environment** (3.11 or newer):
   ```bash
   pip install 'qiskit[visualization]' qiskit-ibm-runtime qiskit-aer pylatexenc jupyter
   ```
3. **Setup check.** Start Jupyter *inside this folder* (the notebooks load `data/` by relative path), open `00_setup_check.ipynb`, set `HAVE_ACCOUNT = True`, paste your key and CRN once, and run it top to bottom. You are ready when it lists a Heron backend.
4. **A chatbot** (ChatGPT, Claude, Gemini, whatever you use) logged in for the red-team block. No MCP client is needed.


## Good to know

- The Open Plan gives you about 10 minutes of QPU time per rolling 28 days. Notebook 01 uses roughly 5 seconds, plus about 30 seconds for the optional section 6, so quota is not the problem; queue wait is. The notebook prints your job id so you can fetch results later with `service.job(id)`, and it can fall back to the instructor's saved counts.
- If the connection to IBM Quantum fails, notebook 01 switches to a local `FakeFez` simulator by itself. Those results are noise-modelled, not real.
- Nothing here opens a Session. The Open Plan does not allow them, and you do not need them.
- Verified with `qiskit 2.5.2`, `qiskit-ibm-runtime 0.49.0` and `qiskit-aer 0.17.2` on Python 3.13.

## Credits

The main notebook is adapted from **"First Step into Quantum Computing" (Qiskit 101 Hands-on)** by Sophy Shin, IBM Corp., Apache-2.0; the original copyright cell is retained. The setup check, red-team exercises and MCP demo were written for this workshop. Reference material: the IBM Quantum docs (https://quantum.cloud.ibm.com/docs) and the Qiskit MCP servers (https://github.com/Qiskit/mcp-servers).

