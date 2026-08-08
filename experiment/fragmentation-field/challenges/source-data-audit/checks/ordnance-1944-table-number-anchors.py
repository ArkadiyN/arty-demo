"""The `TABLE nn` anchors are correct against source.pdf and WRONG in ordnance-1944.md.

Consumer: experiment/fragmentation-field/challenges/source-data-audit/
review-criterion-match.md section 1c, and ledger.md section 35b.

A criterion-match pass noticed that consuming documents cite "Table 43/51/59"
for the casualties series while the six `.invariant` files anchor "TABLE
38/48/56". Neither side is a transcription slip: the two surfaces number the
same tables differently.

- `source.pdf` (the retained scan) prints TABLE 38/39, 48/49, 56/57. This is
  established independently, by page geometry rather than reading order, in
  checks/ordnance-1944-page-geometry.py -- which passes on every anchor.
- `ordnance-1944.md` (the flattened vision extraction) prints TABLE 43/44,
  51/52, 59/60 above the very same rows.

This script establishes the second half and shows the data is identical, so the
discrepancy is confined to the heading. It exists because the natural repair --
"fix the invariant anchors to match the extraction" -- is the wrong repair, and
running check-table-invariants.py cannot tell you that.

The trap it documents: `TABLE nn` greps cleanly in ordnance-1944.md and lands
on a *different shell's* table, which is precisely the failure
.claude/rules/source-data-fidelity.md warns about -- "a TABLE n line is only an
anchor if the extraction kept it attached to its own rows."

Runtime: <1 s.
"""

import csv
import pathlib
import re

ROOT = next(p for p in pathlib.Path(__file__).resolve().parents
            if (p / "doc-reference").is_dir())
DOC = ROOT / "doc-reference/wound-ballistics/ordnance-dept-1944-shell-fragment-damage"
SRC = DOC / "ordnance-1944.md"
TABLES = DOC / "tables"

# slug stem -> the shell heading anchor its .invariant already carries.
# The heading is unique and is the anchor that survives the flattening.
SHELLS = {
    "75mm-m48": "# 75-MM H.E. SHELL, M48",
    "105mm-m1": "# 105-MM H.E. SHELL,'Ml",
    "155mm-m107": "# 155-MM N.E. SHELL, M107",
}

lines = SRC.read_text(encoding="utf-8").splitlines()
fails = []


def find_line(needle):
    return [i for i, ln in enumerate(lines) if needle in ln]


print(f"extraction: {SRC.relative_to(ROOT)}  ({len(lines)} lines)")
print("retained scan numbering is established by checks/ordnance-1944-page-geometry.py\n")

print("--- A. which TABLE headings does the EXTRACTION put above each shell? ---")
governing = {}
for slug, heading in SHELLS.items():
    hits = find_line(heading)
    assert len(hits) == 1, f"{heading!r} is not unique: {len(hits)} hits"
    h = hits[0]
    tabs = []
    for i in range(h, min(h + 12, len(lines))):
        m = re.match(r"^TABLE (\d+)\s*$", lines[i])
        if m:
            tabs.append(int(m.group(1)))
    governing[slug] = tabs
    print(f"  {slug:12s} heading line {h + 1:5d}   TABLE pair in extraction: {tabs}")

print("\n--- B. what do the .invariant files anchor, and where does that land? ---")
for inv in sorted(TABLES.glob("*.invariant")):
    slug = inv.stem
    shell = next(s for s in SHELLS if slug.startswith(s))
    claimed = None
    for ln in inv.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\s*anchor:\s*TABLE (\d+)", ln)
        if m:
            claimed = int(m.group(1))
    where = find_line(f"TABLE {claimed}")
    ctx = "(absent)"
    if where:
        for j in range(where[0], max(where[0] - 40, -1), -1):
            if lines[j].startswith("# "):
                ctx = lines[j].strip()[:42]
                break
    same = claimed in governing[shell]
    print(f"  {slug:34s} anchors TABLE {claimed}")
    print(f"  {'':34s}   extraction pair for this shell: {governing[shell]}"
          f"  -> {'same' if same else 'DIFFERENT'}")
    if not same:
        print(f"  {'':34s}   in the extraction TABLE {claimed} sits under {ctx!r}")
        fails.append((slug, claimed, ctx))

print("\n--- C. is it only the heading? compare the rows themselves ---")
# The extraction interleaves the two columns: casualties row, then perforation
# row, alternating. Pull every line of 5 numeric fields after the shell heading
# and check the CSV's rows appear among them verbatim.
num = re.compile(r"^[\d,.]+(?:\s+[\d,.]+){4}\s*$")
for slug, heading in SHELLS.items():
    h = find_line(heading)[0]
    block = []
    for i in range(h, min(h + 130, len(lines))):
        if num.match(lines[i].strip()):
            block.append(tuple(t.replace(",", "") for t in lines[i].split()))
    for kind in ("casualties", "perforation-1-8in"):
        csv_path = TABLES / f"{slug}-{kind}.csv"
        rows = list(csv.reader(csv_path.open(encoding="utf-8")))[1:]
        hit = 0
        for r in rows:
            want = tuple(x.lstrip("0") if x.startswith("0.") else x for x in r)
            if any(all(a.lstrip("0") == b.lstrip("0") for a, b in zip(want, cand))
                   for cand in block):
                hit += 1
        flag = "PASS" if hit == len(rows) else "PARTIAL"
        print(f"  {slug:12s} {kind:18s} {hit}/{len(rows)} CSV rows found verbatim"
              f" in the extraction   {flag}")

print(f"\nRESULT: {len(fails)}/6 invariant TABLE anchors resolve to a different"
      f" shell in the extraction.")
print("The anchors are NOT wrong -- source.pdf is the authority and geometry")
print("confirms them there. What is missing is a warning that the extraction")
print("renumbers, so `TABLE nn` must never be grepped against ordnance-1944.md.")
