"""Bisect the drag-gap-1944 B-vs-range in-band counts across src/arty history.

Consumer: experiment/fragmentation-field/updates/one-home-rewire/triage-105mm-count.md
(the per-commit count table and the 105mm per-row ratios).

For each listed commit, extracts that commit's src/arty into a temp dir and
re-runs the CURRENT per-caliber check modules (CARD data unchanged since
a01eb33) at AOF_PRIMARY_DEG and the shipped default DragParams(), counting
model/card ratios in the inclusive [0.5, 2.0] band.

Run: uv run python experiment/fragmentation-field/updates/one-home-rewire/checks/b-vs-range-count-bisect.py
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
CHECKS = ROOT / "experiment/fragmentation-field/challenges/drag-gap-1944/checks"
COMMITS = ["a01eb33", "2c34812", "cf402a8", "3a5d800", "74abdd7",
           "5d742b4", "630dac8", "18cd069", "HEAD"]

CHILD = r"""
import importlib.util, json, sys
from pathlib import Path
from arty.shells import SHELLS
from arty.zones import DragParams, compute_shell_zones
checks = Path(sys.argv[1])
out = {}
for cal in ["75mm", "105mm", "155mm"]:
    spec = importlib.util.spec_from_file_location("m" + cal, checks / f"b-vs-range-{cal}.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    shell = SHELLS[mod.SHELL_NAME]; zones = compute_shell_zones(shell); drag = DragParams()
    r = [mod.b_model_at_range(zones, drag, shell.steel.rho, rf, mod.AOF_PRIMARY_DEG) / bc
         for rf, bc in zip(mod.CARD_R_FT, mod.CARD_B)]
    r = [float(x) for x in r]
    out[cal] = dict(r_ft=list(map(float, mod.CARD_R_FT)), ratio=r,
                    n=int(sum(0.5 <= x <= 2.0 for x in r)), total=len(r))
print(json.dumps(out))
"""


def run(commit):
    """Return per-caliber ratios/counts [-] with src/arty taken from one commit."""
    # Extract inside the repo's staging area, not /tmp: a worktree-isolated
    # session prompts on paths outside the worktree.
    with tempfile.TemporaryDirectory(dir=ROOT / "experiment" / "_scratch") as tmp:
        arch = subprocess.run(["git", "-C", str(ROOT), "archive", commit, "src/arty"],
                              check=True, capture_output=True).stdout
        subprocess.run(["tar", "-x", "-C", tmp], input=arch, check=True)
        res = subprocess.run([sys.executable, "-c", CHILD, str(CHECKS)],
                             env={"PYTHONPATH": f"{tmp}/src", "PATH": "/usr/bin:/bin"},
                             capture_output=True, text=True)
        if res.returncode:
            return {"error": res.stderr.strip().splitlines()[-1]}
        return json.loads(res.stdout.strip().splitlines()[-1])


if __name__ == "__main__":
    for c in COMMITS:
        o = run(c)
        if "error" in o:
            print(f"{c:>8}: ERROR {o['error']}")
            continue
        counts = "  ".join(f"{k} {v['n']}/{v['total']} ({min(v['ratio']):.2f}-{max(v['ratio']):.2f})"
                           for k, v in o.items())
        print(f"{c:>8}: {counts}")
        for cal in ("75mm", "105mm"):
            print(" " * 10 + f"{cal} ratios: " + " ".join(
                f"{r:.0f}:{x:.3f}" for r, x in zip(o[cal]['r_ft'], o[cal]['ratio'])))
