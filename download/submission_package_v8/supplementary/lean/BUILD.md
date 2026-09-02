# Reproducing the build

The `.lake/` directory (~7.6 GB of Mathlib artefacts) is NOT part of the
workspace snapshot and must be regenerated:

```sh
curl -sSfL https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh | sh -s -- -y
export PATH="$HOME/.elan/bin:$PATH"
cd lean4/BST
lake update          # fetches Mathlib + prebuilt cache (~2 min)
lake build           # ~1 min
python3 ../../tools/lean_check.py
```

Toolchain is pinned by `lean-toolchain` (v4.33.0-rc2, set by `lake update`
to match the Mathlib revision).
