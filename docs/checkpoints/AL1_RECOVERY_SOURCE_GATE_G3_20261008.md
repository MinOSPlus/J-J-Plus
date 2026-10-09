# AL1 Recovery G3 — source-pattern admission (2026-10-08)

Status: **CANDIDATE / NOT CURRENT**. No modification of production compiler modules.

## Checked against actual repository source

Branch: `checkpoint/al1-recovery-mechanics-g2-20261008`
Reference file: `src_j/compiler/backend/memory_transport_optimizer.j`

The recovery tool's first and second original fragments each match **exactly once** in the actual repository source, not only in a synthetic fixture. Replacing these with the existing validators `jj_mto_load_shape` and `jj_mto_moved_load_shape` produces a text delta of **-226 characters**; both replacement fragments are ASCII, so the modified portion has **-226 bytes**.

Existing validators are already declared in the same source module. The transformation preserves the separate explicit `base_slot == index_slot` refusal.

## Isolated executable tool checks

Local `python3 al1_patch_tests.py` gate: **4/4 PASS**, with:
1. Two-block replacement and -226-byte delta.
2. Refusal of source=destination.
3. Refusal of altered source match with no output.
4. Refusal of a non-unique match.

`python3 -m py_compile` of the two recovery scripts: PASS.

Direct container GitHub clone/ls-remote could not connect because DNS resolution for github.com failed. Source-pattern inspection was performed through the connected GitHub API instead.

## Not proven

This is not the historical -174-byte AL1 delta, whose exact patch is missing. No full-tree replay, compiler build, selfhost G1=G2, cross-lineage comparison, x86/ARM/i386 test suite, or performance test has been executed for the -226-byte candidate. Historical gates cannot be transferred to this candidate.

## Next

Fetch a full immutable compiler tree into an executable environment; apply the candidate only on a copy; run the full Root/Profile B/Diagnostic selfhost, negative and target regressions, and compare against the historical baseline. Keep both canonical `main` and `src_j/` untouched until independently gated.
