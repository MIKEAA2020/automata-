#!/bin/bash
# Open-web (arXiv-full-text-class) searches for the manuscript's coinages.
# Backend: z-ai web_search. run() wraps phrases in JSON-escaped quotes.
OUT=/home/z/my-project/automata-repo/scripts/coinage_search
mkdir -p "$OUT"
run() {  # $1 = key, $2 = query, phrases auto-wrapped as "..."
  echo "=== $1 : $2 ==="
  z-ai function -n web_search -a "{\"query\": \"\\\"$2\\\"\", \"num\": 10}" -o "$OUT/web_$1.json" 2>&1 | grep -E 'saved|Error' | head -1
}

run unifilar_lumpability 'unifilar lumpability'
run unifilar_lumpable 'unifilar-lumpable'
run commitment_gap 'commitment gap'
run retention_gap 'retention gap'
run grounding_gap 'grounding gap'
run price_of_safety 'Price of Safety'
run determination_index 'determination index'
run protocol_stratification 'protocol stratification'
run commitment_corr 'commitment gap correlation gap'
run pos_bandit 'Price of Safety bandit best arm identification'
run kappa_pair 'kappa_pair determination index'
run kappa_raw 'kappa_pair'
echo "done"
