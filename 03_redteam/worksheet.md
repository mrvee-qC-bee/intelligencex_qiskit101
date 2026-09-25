# Red-team the AI -- student worksheet (25 minutes)

**What you will take away**
1. A chatbot's Qiskit is, on average, two major versions old; the failures range from a loud ImportError to a silent wrong answer.
2. The fix is never "trust the bot": it is run it, paste the traceback or the docs URL back, and verify against https://quantum.cloud.ibm.com/docs.
3. The four-step pattern you used in Qiskit 101 (Map, Optimize, Execute, Post-process) is the checklist that catches every bug on the bingo card.

You need: this folder (`03_redteam/`), your chatbot of choice (ChatGPT / Claude / Gemini, whatever you have), a terminal in the
workshop Python environment, and the docs site open in a tab. No IBM account is needed for this block; nothing here spends QPU time.

---

## 0:00-0:05  Live opener -- one prompt, many bots

Type this into your chatbot, exactly:

> write Qiskit code that runs a Bell state on an IBM quantum computer

Do not run it yet. Read it against the bingo card (`bingo_card.md`) and mark every square you can point to.
Then run it in the terminal. Count: how many lines until the first error? Compare with your neighbour. The room tallies which squares came up most.

If your bot's code ran unmodified on Qiskit 2.5: congratulations, verify the counts are only 00/11 and tell the lecturer which model it was.

## 0:05-0:20  Exercises with the bingo card

First, together: `bash run_all.sh`. Twelve files, twelve verdicts, all six tracebacks on one screen.

Then in pairs, for each exercise (files `broken_N.py` / `fixed_N.py`, story in `exercises.md`):
1. **Predict** the bug from reading the bot's code, before running. Mark the bingo square.
2. **Run** `python broken_N.py`. Does the traceback match your prediction? (Exercise 6 has no traceback. Read its output twice.)
3. **Find the docs page** that explains the change (the fixed file's docstring has the URL; try searching the docs site first).
4. **Run** `python fixed_N.py` and identify which of the four pattern steps the bot had wrong.

Must do: 1, 5 and 6. Then 3, 2, 4 in that order as time allows. Exercise 4 has an eight-bug cascade: peel one, run, peel the next.

## 0:20-0:25  The twist -- make the bot fix itself, then check it

Paste the *whole traceback* from your opener code (or from `broken_4.py`) back into the chat and ask: "fix this". Then:
- Run the fix. Did it run? Did it hit a *new* bingo square (V1 Sampler instead of `execute` is the classic)?
- Now paste the docs URL from the relevant `fixed_N.py` docstring into the chat and ask again. Compare the two fixes.
- Verify the final code against the docs page yourself, line by line, before you call it fixed.

---

## Scoring (per pair, honour system)

| Phase | Points |
|---|---|
| Opener | +1 per bingo square you can point to in your own bot's output (max 9); +2 if it ran unmodified and you verified the counts |
| Each exercise | +1 correct prediction before running; +1 correct docs page found; +1 you can name the pattern step (Map / Optimize / Execute / Post-process) the bot broke |
| Twist | +2 if the bot's self-fix runs; +3 if you caught a new bug in the self-fix; +2 if the docs-URL version was better than the traceback-only version; -3 if you declared a fix "done" without running it |

Bingo (three in a row) at any point: +5. Full card: +10 and a photo of the card for the lecturer.

## Tips that actually work

- **Paste the traceback, not a description.** "It doesn't work" gets you a rewrite of the same 2023 code; the last three lines of the traceback get you the fix.
- **Paste the docs URL.** Bots follow a pasted page far better than they recall one. The URLs are in every `fixed_N.py` docstring.
- **Name the version.** Start prompts with "Qiskit 2.5, qiskit-ibm-runtime 0.49, IBM Quantum Open Plan (no sessions)". It removes half the card.
- **Ask for the four steps by name.** "Map, Optimize with generate_preset_pass_manager, Execute with SamplerV2, Post-process from result[0].data" leaves no room for `execute`.
- **Never trust exit code 0.** Predict the histogram before you run; Exercise 6 is what "it ran fine" looks like.
- **Never put a token in code, never set `RUN_ON_HARDWARE = True` in the room.** Offline the scripts use FakeFez / AerSimulator and cost nothing.

## Why a plain chatbot is the realistic tool

IBM's hosted assistant is gone. From the docs changelog (https://quantum.cloud.ibm.com/docs/en/guides/changelog-qiskit-code-assistant, entry dated 29 May 2026):

> **Qiskit Code Assistant service discontinued** - The preview service has been discontinued and the Visual Studio Code and JupyterLab extensions have been archived. [...] Qiskit Code Assistant models remain available for local use.

So today you either run the open `mistral-small-3.2-24b-qiskit` model locally (https://quantum.cloud.ibm.com/docs/en/guides/qiskit-code-assistant)
or you use a general chatbot and feed it the docs yourself, which is exactly what this block trains. If your chatbot client can attach
tools, the Qiskit MCP servers (https://github.com/Qiskit/mcp-servers) give it the docs and a circuit analyser directly; the lecturer will show that.

**Key takeaway:** the bot is a fast typist with an old textbook. You bring the current docs, the traceback and the prediction; then it is useful.
