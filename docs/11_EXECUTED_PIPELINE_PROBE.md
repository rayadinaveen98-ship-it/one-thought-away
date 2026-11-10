# Executed Blender pipeline probe — v0.1
Date: 2026-11-11 (Asia/Calcutta).
Status: GENERIC ENGINEERING TEST PASSED; ANU CHARACTER GATES REMAIN OPEN.

## Delivered work
A real saved Blender scene with a 17-bone FK rig, keyed motion over frames 1–96 at 24 fps, one continuous two-bone weighted sleeve, and a rigid head attachment marker.
The figure is a deliberately generic mechanical proxy, not Anu, not a character proposal and not a final model.
Four 800×640 pose renders and a four-second 400×320 motion preview were generated. The preview samples every fourth animation frame (6 distinct samples/second) and is encoded at 24 fps with repeated frames; it is not real-time playback evidence.
A second .blend links the asset collection from the first using a relative library path. It is an asset reuse test, without a presentation camera.

## Verified results
Verification ran in a separate Blender process and exited 0.
- All 96 frames: finite sleeve and marker coordinates.
- Head attachment error below 1e-5 world units; observed maximum 4.777820964108429e-7.
- Sleeve vertices move under the armature; maximum neutral-to-reach displacement 0.797495 world units.
- Frames 1 and 96: matching visible-mesh geometry signatures.
- Original versus linked scene: matching visible-mesh signatures at frames 1, 25, 49, 73 and 96.
- Copy both .blend files into another folder, reopen linked scene: matching signatures at those same five poses.
- Original versus freshly reopened neutral render: maximum decoded channel difference 0 on this recorded build and machine.

These seven narrow checks passed. They do not imply Anu's G1–G6 production gates passed.
Visual review checked the pose stills and a contact sheet decoded from the actual video. A rigid display segment originally intersected the weighted sleeve; the final builder hides the replaced display solids.

## Measured environment and limits
Blender 5.3.0, build 02f0899d78e3; BLENDER_EEVEE.
Raw still-render observations: neutral 39.428s; reach 11.239s; lean 11.129s; head_turn 8.329s.
The first sample includes renderer initialization and was not an isolated benchmark. Subsequent samples are for a very small technical scene. No peak-memory, GPU/CPU characterization, controlled playback or representative character test was completed; no film-render budget is inferred.

## Reproduce
From repository root, with Blender 5.3 on the executable path:
```text
blender --background --factory-startup --python-exit-code 1 --python scripts/build_pipeline_probe.py -- work/pipeline_probe
blender --background --factory-startup --python-exit-code 1 --python scripts/verify_pipeline_probe.py -- work/pipeline_probe
```
The verifier creates its temporary relocation folder inside the selected writable output directory, validates that boundary, then removes that temporary folder. An initial attempt to use the system temporary directory failed because this environment denied writes there; the final workspace-based relocation test passed.
Non-fatal thumbnail/extension-cache write warnings occurred outside the workspace; actual saves, rendering and library relocation passed.
The initial material API produces a Blender 6.0 deprecation notice; testing is specific to the recorded 5.3 build.

## Evidence and artifact locations
- [Build report](evidence/pipeline_probe_v001/build_report.json)
- [Verification report](evidence/pipeline_probe_v001/verification_report.json)
- [Builder](../scripts/build_pipeline_probe.py)
- [Verifier](../scripts/verify_pipeline_probe.py)
- Owner-facing local delivery: one-thought-away-pipeline-proof-v001.zip, containing the two .blend files, pose renders, preview media, sources, reports and checksums. Binary media is delivered in the chat rather than committed as production assets.
- Master probe .blend SHA-256: `733a4c0b4b24af5e98fe3130ef68dc87998342431dd57c02f623a3b19075a981`.

## Character-specific dependency
Original Anu PNGs were not available through retrieved chat attachments, workspace/Downloads filename search, or a focused browser attempt (the browser view could not access the original conversation). No private conversation identifiers are published here.
Recover the originals, then complete R0/R1. No Anu likeness, anatomy, face rig, hair, costume, acting, cloth or production render-cost approval is claimed. No story change was introduced.
