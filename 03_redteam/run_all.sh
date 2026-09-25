#!/usr/bin/env bash
# Red-team block: run every broken_N.py (expected to FAIL, except 6 which runs but is wrong)
# and every fixed_N.py (expected to PASS with no DeprecationWarning). Never touches IBM Quantum:
# every hardware line sits behind RUN_ON_HARDWARE = False and runs on FakeFez / AerSimulator instead.
# Usage:  bash run_all.sh            (uses $PY if set, else the workshop conda python, else python3 on PATH;
#                                     exits 2 with a one-line message if that python has no Qiskit)
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY="${PY:-/Users/vishalbajpe/miniforge3/envs/qiskit-paper/bin/python}"
[ -x "$PY" ] || PY="$(command -v python3 || true)"
echo "python: ${PY:-<none found>}"
if [ -z "$PY" ] || ! "$PY" -c "import qiskit, qiskit_ibm_runtime, qiskit_aer" >/dev/null 2>&1; then
  echo "ERROR: this python has no Qiskit. Set PY=/path/to/python with Qiskit 2.x installed (qiskit, qiskit-ibm-runtime, qiskit-aer) and re-run." >&2
  exit 2
fi
"$PY" -c "import qiskit, qiskit_ibm_runtime, qiskit_aer; print('qiskit', qiskit.__version__, '| qiskit-ibm-runtime', qiskit_ibm_runtime.__version__, '| qiskit-aer', qiskit_aer.__version__)"
echo
fails=0
check() {  # check <label> <expected: fail|pass|runs-wrong> <file>
  local label="$1" expect="$2" file="$3" out rc
  out="$("$PY" -W error::DeprecationWarning "$HERE/$file" 2>&1)"; rc=$?
  case "$expect" in
    fail)       [ $rc -ne 0 ] && verdict=PASS || verdict=FAIL ;;
    pass)       [ $rc -eq 0 ] && verdict=PASS || verdict=FAIL ;;
    runs-wrong) { [ $rc -eq 0 ] && grep -q "qubit 2 ended up as 1" <<<"$out"; } && verdict=PASS || verdict=FAIL ;;
  esac
  [ "$verdict" = PASS ] || fails=$((fails+1))
  printf '%-4s %-12s expected=%-10s exit=%s\n' "$verdict" "$file" "$expect" "$rc"
  if [ "$expect" = fail ]; then
    echo "     last 3 lines of traceback:"; tail -n 3 <<<"$out" | sed 's/^/     | /'
  else
    tail -n 3 <<<"$out" | sed 's/^/     | /'
  fi
  echo
}
echo "== broken files (the bot's code) =="
check 1 fail broken_1.py
check 2 fail broken_2.py
check 3 fail broken_3.py
check 4 fail broken_4.py
check 5 fail broken_5.py
check 6 runs-wrong broken_6.py
echo "== fixed files (Qiskit 2.5 / runtime 0.49 APIs, run with -W error::DeprecationWarning) =="
for n in 1 2 3 4 5 6; do check $n pass fixed_$n.py; done
echo "== summary: $fails unexpected result(s) =="
exit $fails
