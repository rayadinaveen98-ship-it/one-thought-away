# Local Blender readiness — evidence v0.1
Test date: 2026-11-11 (Asia/Calcutta).
Scope: executable and background startup only; not an Anu modeling, rigging or render benchmark.

## Observed result
- Installed runtime: Blender 5.3.0, Windows Release.
- Build hash: 02f0899d78e3; build date 2026-11-10.
- Version command: exit code 0.
- Background factory-startup with Python scene inspection: exit code 0; normal Blender quit.
- Returned scene engine: BLENDER_EEVEE.
- Returned factory objects: Camera, Cube, Light.
- No .blend was saved or changed. No image was rendered.

This establishes that the proposed Blender version is locally installed and can start without the UI and inspect a factory scene. It does not establish GPU support, shader appearance, render speed, playback performance, Anu likeness, deformation quality or dependency portability.

## Repeat procedure
On the selected production machine, run Blender --version, then:
```text
blender --background --factory-startup --python-expr "import bpy,json; print('OTA_RUNTIME '+json.dumps({'version':bpy.app.version_string,'build_hash':bpy.app.build_hash.decode(),'background':bpy.app.background,'engine':bpy.context.scene.render.engine,'objects':sorted(o.name for o in bpy.context.scene.objects)}))"
```
Resolve blender to that machine's actual executable; record version, build hash, stdout and exit code. This command inspects the factory scene and exits; it is not a performance test.

## Reference recovery result
A filename search for Anu-prefixed PNG/JPG/JPEG/WebP files in the local Codex workspace tree and Downloads returned no matches. This does not prove the originals do not exist elsewhere.
The retrieved earlier conversation supplied filenames but no accessible original image attachments. Original source recovery remains pending.

## Gate status
- Runtime startup check: PASS (limited scope above).
- R0 original reference ingest: PENDING.
- R1 corrected modeling packet: NOT STARTED.
- Character likeness, rig/deformation, shading, reuse and cost gates G1–G6: NOT RUN.
- Next required input: original anu_turnaround_exploration_v01.png and anu_expressions_exploration_v01.png; see 07_ANU_REFERENCE_LOCK.md.
