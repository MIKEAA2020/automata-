#!/usr/bin/env python3
"""Inventory theorem-like environments in v4; classify proof-bearing results.
Already-checked (Task 4, AAK family): thm:aak-multiletter, thm:aak-equality,
thm:spectral-grounding, prop:grounding-finite-section,
prop:grounding-structured-zero, cor:hankel-strict, open:hankel-multiletter.
"""
import re, json, collections

TEX = "/home/z/my-project/download/automata_unified_revised_v4.tex"

env_re = re.compile(r"\\begin\{(theorem|lemma|proposition|corollary|definition|remark|example|openproblem|conjecture|problem|fact|observation|claim|construction|heuristic|metatheorem|assumption)\}")
label_re = re.compile(r"\\label\{([^}]+)\}")

CHECKED = {
    "thm:aak-multiletter", "thm:aak-equality", "thm:spectral-grounding",
    "prop:grounding-finite-section", "prop:grounding-structured-zero",
    "cor:hankel-strict", "open:hankel-multiletter",
}
# env types that carry proofs worth checking
PROOF_TYPES = {"theorem", "lemma", "proposition", "corollary", "claim", "fact", "observation", "conjecture", "metatheorem"}

with open(TEX, encoding="utf-8") as f:
    lines = f.readlines()

items = []
cur = None
section = ""
section_re = re.compile(r"\\section\{([^}]+)\}")
for i, ln in enumerate(lines, 1):
    m = section_re.search(ln)
    if m:
        section = m.group(1)
    em = env_re.search(ln)
    if em:
        cur = {"env": em.group(1), "line": i, "label": None, "section": section,
               "has_proof": False, "title": None}
        items.append(cur)
        # title text on same line
        rest = ln[em.end():].strip()
        if rest and not rest.startswith("\\label"):
            cur["title"] = rest[:90]
    if cur is not None:
        lm = label_re.search(ln)
        if lm and cur["label"] is None:
            cur["label"] = lm.group(1)
        if r"\begin{proof}" in ln:
            cur["has_proof"] = True
            cur["proof_line"] = i
        if r"\end{" + cur["env"] + "}" in ln and i > cur["line"]:
            cur["end_line"] = i
            cur = None

# robust proof assignment: each \begin{proof} belongs to the nearest PRECEDING
# proof-type environment (proofs may follow intervening remarks, as with
# meta:boolean and lem:littlestone).
proof_types = {"theorem", "lemma", "proposition", "corollary", "claim", "fact",
               "observation", "conjecture", "metatheorem"}
proof_lines = [i for i, ln in enumerate(lines, 1) if r"\begin{proof}" in ln]
for it in items:
    it["has_proof"] = False
for pl in proof_lines:
    candidates = [it for it in items
                  if it["env"] in proof_types
                  and it.get("end_line", it["line"]) <= pl]
    if candidates:
        tgt = max(candidates, key=lambda it: it.get("end_line", it["line"]))
        if not tgt["has_proof"]:
            tgt["has_proof"] = True
            tgt["proof_line"] = pl

# section names -> numbers
secs = []
seen = set()
for it in items:
    key = it["section"]
    if key not in seen:
        seen.add(key)
        secs.append(key)
secnum = {s: k + 1 for k, s in enumerate(secs)}

counts = collections.Counter(it["env"] for it in items)
proof_counts = collections.Counter(it["env"] for it in items if it["has_proof"])

remaining = [it for it in items
             if it["env"] in PROOF_TYPES and it["label"] not in CHECKED and it["has_proof"]]
remaining_nolabel = [it for it in items if it["env"] in PROOF_TYPES and not it["label"] and it["has_proof"]]
checked_now = [it for it in items if it["label"] in CHECKED]
no_proof_results = [it for it in items if it["env"] in PROOF_TYPES and not it["has_proof"]]

print("=== TOTAL theorem-like environments:", len(items))
print("=== By type:", dict(counts))
print("=== With proofs:", dict(proof_counts))
print("=== Already checked (AAK family):", len(checked_now), sorted(it['label'] for it in checked_now))
print("=== REMAINING proof-bearing results:", len(remaining))
print("    (of which unlabelled:", len(remaining_nolabel), ")")
print("=== Proof-bearing results WITHOUT a proof env (stated sans proof):", len(no_proof_results))
print()
by_sec = collections.Counter(secnum[it["section"]] for it in remaining)
print("=== Remaining results by section number:")
for k in sorted(by_sec):
    print(f"    Sec {k} ({secs[k-1][:60]}): {by_sec[k]}")
print()
print("=== FULL LIST of remaining proof-bearing results (label, type, line):")
for it in remaining:
    tag = "NO-LABEL" if not it["label"] else it["label"]
    print(f"    L{it['line']:>6}  {it['env']:<12} {tag}  [sec {secnum[it['section']]}]")

json.dump({"items": items, "secnum": secnum, "secs": secs,
           "remaining_labels": [it["label"] for it in remaining]},
          open("/home/z/my-project/scripts/theorem_inventory_v4.json", "w"), indent=1)
print("\nSaved: /home/z/my-project/scripts/theorem_inventory_v4.json")
