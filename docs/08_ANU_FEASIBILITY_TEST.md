# Anu reproducibility and rig feasibility — v0.1
Date: 2026-11-11. Deliverable: bounded technical test specification, NOT an executed rig test.
All construction choices below are proposals for testing, not changes to story or approved appearance.

## Entry and stop conditions
R0 reference ingest and R1 modeling packet in 07_ANU_REFERENCE_LOCK.md must pass before character-specific construction. A generic proxy can test software only and cannot prove Anu's likeness.
Do not start full sets, supporting character designs, production animation or expensive simulation to work around a failed character gate.
Blender 5.3 in older docs is a proposed target, not a verified installed runtime. Record actual executable build and hardware before choosing a production version.

## Smallest useful asset
One neutral test scene; one Anu head/body proxy matched to the packet; one camera set; no story staging.
Proposed construction: deformable head mesh with eye/lid/mouth loops; separate eyeballs; simple internal mouth and complete front teeth; large hair masses with a few controlled strands; rigid butterfly clip parented to the head. Start hair with bones and costume with weights/correctives. Test simulation only if the approved silhouette or action cannot be met.
Costume and accessories remain pending: a plain deformation proxy is labeled temporary and cannot lock the yellow dress or bunny bag.

## Test sequence (24 fps proposal; technical exercises, not film shots)
| Frames | Exercise | Evidence required |
| --- | --- | --- |
| 1–24 | neutral hold, fixed camera | front/profile/three-quarter likeness and scale |
| 25–72 | blink, gaze left/right/up/down, small head turn | lid contact; no eye popping; clip stays attached |
| 73–144 | curiosity → delight → neutral → tentative hope → quiet hurt | stable identity; brows/lids/lips support restrained acting |
| 145–216 | crouch/stand, reach, object grip | shoulder/hip/knee/hand deformation and foot contact |
| 217–288 | lean toward a static hug proxy, settle | neck/shoulder collapse, hair/cloth intersection and return to rest |

Use fixed key poses plus slow interpolation; do not hide deformation problems with edits, motion blur or dramatic lighting. No dialogue or lip-sync claim from this test.
Additional release pose sheet must cover mischief, focus, confusion, disappointment and comfort as required by look-dev v0.1.

## Pass/fail gates and remedy
- G1 likeness: side-by-side reference and neutral renders with shared view labels; owner accepts recognizability and all unresolved appearance decisions. No exact-match claim before review.
- G2 deformation: inspect keyed extremes and transitions close-up. No visible mesh penetration, collapsing joints, inverted lids or changing teeth. Fix weights/topology/correctives before embellishment.
- G3 shading: same asset under neutral, daylight and dim bounce setups. Hair/clip remain readable and skin avoids a plastic appearance. Store lights/exposure/color settings.
- G4 reuse: close Blender; reopen from a clean checkout plus declared dependencies; link asset into a second empty scene and render the same pose. Missing dependencies, changed identity or inconsistent output fail.
- G5 cost: record CPU/GPU/RAM/VRAM, Blender build, engine/device, resolution, samples, denoise and settings. Measure playback and render time, peak memory where available, and warm-up separately. Test 12 frames including neutral, deformation extreme and dim light; report median AND slowest, with no extrapolation presented as a guarantee.
- G6 release: all evidence paths, checksums and decisions recorded; owner accepts appearance/acting; technical reviewer records defects resolved. No unchecked gate is treated as passed.

Proposed proxy target: responsive 24 fps playback at the selected preview settings; if missed, measure simplification options before claiming feasibility. Render budget is unset until actual hardware and measured cost are known. For planning only: total render hours = frame_count × measured seconds_per_frame / 3600, before retries/compositing; 8m50s at 24 fps = 12,720 frames.
Failure may change implementation, never silently change recognizable design. Present required appearance tradeoffs for owner review.

## Required evidence package
blender/characters/anu/tests/v001/: test .blend, dependency list, build/settings record, pose/control map and repeat instructions.
renders are kept outside ordinary Git; repository records stable delivery location and SHA-256 for approved evidence.
Report: entry gate, asset/ref commits, test date/operator, each gate PASS/FAIL/NOT RUN, evidence links, defects, timing samples, unresolved decisions and release decision.

## Current result
R0 pending missing source pixels. R1 not started. G1–G6 NOT RUN.
No character model, rig, animation, successful render or performance benchmark has been created or verified by this documentation.
