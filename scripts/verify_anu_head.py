"""Structural checks only. These never assert visual likeness or animation readiness."""
import bpy,sys,json,math,hashlib
from pathlib import Path
args=sys.argv[sys.argv.index('--')+1:];path=Path(args[0]).resolve();out=Path(args[1]).resolve()
bpy.ops.wm.open_mainfile(filepath=str(path));scene=bpy.context.scene
meshes=[o for o in scene.objects if o.type=='MESH']
finite=all(math.isfinite(c) for o in meshes for v in o.data.vertices for c in v.co)
source=bpy.data.images['ANU_APPROVED_SHEET_v002']
source_hash=hashlib.sha256(bytes(source.packed_file.data)).hexdigest()
expected='1b19b51c7d24d44c66ea0d27404e1886ea1683b5730b7b8deb1f92154efff890'
normals={}
for side in ['L','R']:
    obj=bpy.data.objects['ANU_ORBIT_LIDS_'+side]
    normals[side]=sum(p.normal.y for p in obj.data.polygons)/len(obj.data.polygons)
clips=[o for o in meshes if o.name.startswith('ANU_CLIP_')]
clip_left=all(sum(v.co.x for v in o.data.vertices)/len(o.data.vertices)>0 for o in clips)
checks={'reopened_saved_mesh':len(meshes)>0,'all_mesh_coordinates_finite':finite,
        'packed_source_matches_approved_png':source_hash==expected,
        'hidden_orbital_reference_normals_face_forward':all(v<0 for v in normals.values()),
        'clip_geometry_on_anatomical_left':clip_left,
        'no_rig_claimed_or_present':not any(o.type=='ARMATURE' for o in scene.objects)}
report={'asset_id':'CH_ANU','stage':'LOCAL_HEAD_LIKENESS_STUDY','blender':bpy.app.version_string,
        'build_hash':bpy.app.build_hash.decode(),'blend_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
        'source_png_sha256':source_hash,'mesh_objects':len(meshes),
        'mesh_control_vertices':sum(len(o.data.vertices) for o in meshes),
        'hair_mesh_locks':sum(o.name.startswith('ANU_HAIR_') and o.name!='ANU_HAIR_main_mass' for o in meshes),
        'hair_detail_curves':sum(o.type=='CURVE' and o.name.startswith('ANU_HAIR_') for o in scene.objects),
        'orbital_mean_normal_y':normals,'structural_checks':checks,'all_structural_checks_passed':all(checks.values()),
        'likeness_gate':'NOT_PASSED','production_quality_gate':'NOT_PASSED','animation_ready':False,
        'limitations':['Bust only','Boolean-cut orbital loops and separate lip surfaces need production retopology','No mouth cavity or teeth','No facial or body rig','Physical scale unconfirmed']}
out.write_text(json.dumps(report,indent=2),encoding='utf-8');print('ANU_STRUCTURE '+json.dumps(report),flush=True)
if not all(checks.values()):raise RuntimeError('Structural check failed')
