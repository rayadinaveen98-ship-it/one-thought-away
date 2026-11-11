# Anu reference control — v0.2
Date: 2026-11-11. Asset ID: CH_ANU. Status: LOOK APPROVED IN PRINCIPLE; REFERENCE INGEST PENDING; NO 3D ASSET.

## Evidence and authority
The owner approved the current Anu look in principle and requires the same character in future images and Blender shots, reproducible construction, disciplined scope and professional gates. This is not blanket approval of every incidental costume detail, inconsistent generated view, numerical proportion or final 3D performance.

Reviewed repository baseline: commit 19cda4e4dea481186b56840ff8022e0915048e02. Recursive inventory contains text documentation and folder READMEs, no image, mesh, rig or .blend file.
Source: owner's earlier character-development conversation (private identifiers omitted). The prior delivery names:
- anu_turnaround_exploration_v01.png
- anu_expressions_exploration_v01.png

The retrieved chat contains sandbox links, but returns attachments: []; those original pixels were not available for inspection or hashing in this session. Prior textual descriptions are provenance, not a substitute for inspecting images. Do not fabricate a replacement and label it the approved original.

## Source-of-truth hierarchy
1. Story canon and explicit owner decisions govern narrative and established identity.
2. Recovered original concept bytes establish the approved-in-principle visual baseline after identity confirmation.
3. A corrected, reviewed modeling packet resolves incompatible views without silently redesigning Anu.
4. After visual matching and rig approval, one versioned master Blender asset governs every production shot and rendered character reference.

Until step 2, no visual measurements, sampled colors, clip side or facial landmarks can be asserted as verified. Exact identity across independently generated AI images cannot be guaranteed by prompt or seed. Such images remain studies, require comparison, and cannot supersede the master.

## Reference ingest gate R0 — currently NOT PASSED
- Recover both original PNGs from the earlier chat/downloads or owner upload.
- Preserve original filenames and bytes under assets/characters/anu/reference/source/v001/.
- Record SHA-256, dimensions, source message, ingestion date and custodian in reference_manifest.v001.json. Never insert dummy hashes.
- Visually identify which image/view the owner approved. If multiple versions differ, ask for selection; never choose silently.
- Compare front/profile/back/expression identity; annotate conflicts in a separate review file, leaving sources intact.
- Record actual source image coordinates for eye line, chin, ears, hair silhouette and clip attachment; record left/right in character space and whether a view is mirrored.
- Record costume/bag/shoes as unresolved unless explicitly confirmed. Preserve face/hair direction; don't restart design exploration.
- Owner confirms any conflict resolution affecting recognizable appearance. R0 closes only with original pixels, provenance and review evidence.

## Modeling packet gate R1 — not started
Create corrected neutral front, both profiles, back and three-quarter views with shared eye/chin/shoulder/hip/knee/sole guides; neutral face and relaxed A-pose. Perspective concept sheets cannot supply exact orthographic depth.
Record height and head/body ratios as proposed measured construction choices, not inherited facts. Include head close-ups, hair masses, clip attachment diagram, palette/material swatches under neutral light and confirmed costume silhouette. Keep original and corrected references visibly separate.
Use one approved three-quarter view as the identity anchor; original pixels must determine which view, not this document.

## Release and shot continuity
Release IDs: CH_ANU_ref_v001, CH_ANU_model_v001, CH_ANU_rig_v001. Do not issue a release merely because a filename exists.
Store source commit, asset checksum, Blender build, packed/external dependency manifest, camera settings, color management, materials and rig version for each reviewed release.
All shots link the same approved asset version. Log deliberate overrides; no per-shot facial reshaping, clip relocation or hair redesign.
Compare neutral front/profile/three-quarter renders and expression extremes side by side with the reference packet. Fail on altered age read, head/eye spacing, hair silhouette, clip position or teeth. Lighting variation must not disguise drift.
Changes require a new version, reason, impact, comparison evidence and owner decision when appearance changes.

## Owner-authorized replacement route — 2026-11-11
The owner confirmed having no images and authorized designing Anu if the old artwork cannot be recovered. [Replacement candidate v0.2](12_ANU_REPLACEMENT_CANDIDATE.md) is now archived with original generated pixels, prompt and SHA-256. It is PENDING VISUAL APPROVAL, not a recovered original and not automatically covered by v0.1 approval in principle. Once the owner approves the specific replacement, it may serve as the R0 baseline; archive that approval against its hash and retain the missing-original registry as historical evidence. R1 and character-specific technical gates still apply.
