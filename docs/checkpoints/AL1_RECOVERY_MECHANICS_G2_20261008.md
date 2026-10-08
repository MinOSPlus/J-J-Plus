# AL1 recovery — mechanics gate G2 (2026-10-08)

Status: **CANDIDATE / NOT CURRENT / NOT PROMOTED**.

Scope: recovery tooling only. This branch does not change canonical `src_j/` or the frozen Public Review Preview.14 compiler.

## Reference
- Public baseline: `MinOSPlus/J-J-Plus`, main commit `7dbc0866145ba0a13b2946432168ff5e45ae46cd` (Preview.14).
- Backend file: `src_j/compiler/backend/memory_transport_optimizer.j`.
- Existing validators: `jj_mto_load_shape` and `jj_mto_moved_load_shape`.
- Historical AL1: reported **174 bytes less**, Root G1=G2 SHA-256 `2584f8b964d205028a55cc882174212617a5758e3d9f524fe2bd981af6a24e19`; historical functional report 21/21 general, 4 additional graphs, 6 nearby expression checks, three lineage fixed points and cross-lineage Root rebuilds. These are **historical report values**, not newly rerun gates.
- Recovered candidate: replaces exactly two repeated x86 load-shape validations, **226 bytes less** on the source test fixture, not the exact historical AL1 patch.

## Tooling
- `tools/al1_recovery/AL1_recovery_apply.py`: applies candidate to a separate destination; refuses in-place change, missing or non-unique patterns, and unexpected byte delta.
- `tools/al1_recovery/al1_patch_tests.py`: offline self-contained fixture tests.

Run from repository root:

```sh
python3 tools/al1_recovery/al1_patch_tests.py
python3 tools/al1_recovery/AL1_recovery_apply.py \
  src_j/compiler/backend/memory_transport_optimizer.j \
  /tmp/memory_transport_optimizer.al1-candidate.j
```

## Evidence and limitations
Mechanics tests were rerun on 2026-10-08 using the standalone recovery scripts: **4/4 PASS** for exact two-block substitution/226-byte delta; in-place refusal; altered pattern failure with no output; duplicate pattern failure. This is a fixture-level gate, **not** a compiled compiler gate.

**NOT TESTED:** full source-tree integration; compiler selfhost Root/Profile B/Diagnostic; G1=G2; cross-lineage; byte-exact outputs against AK1/AL1; negative-effect or target gates; performance.

The 226-byte candidate is **not** a reconstruction of the historical 174-byte AL1 until proven. No promotion of `CURRENT`, no performance improvement claim and no change to the compiler baseline.

## Next promotion gates
1. Apply candidate on clean independent copy and compare source hashes.
2. Rebuild all three compiler lineages G1=G2.
3. Run x86-64/AArch64/ARM32/i386 regressions, cross-lineage comparisons and safe rejection gates.
4. Compare exact produced artifacts against historical AK1 and AL1 sources if recovered.
5. Perform clean-package replay and independent review before sealing.
