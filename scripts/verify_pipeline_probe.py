"""Run in a new Blender process, independently of the build process."""
import bpy,sys,json,hashlib,math,time,shutil,tempfile
from pathlib import Path
from mathutils import Vector
out=Path(sys.argv[sys.argv.index('--')+1]).resolve()
path=out/'movement_pipeline_probe_v001.blend'
bpy.ops.wm.open_mainfile(filepath=str(path))
scene=bpy.context.scene
rig=bpy.data.objects['TECH_PROBE_RIG']
marker=bpy.data.objects['Head_attachment_marker']
sleeve=bpy.data.objects['Continuous_weighted_sleeve.L']

def coords(obj):
    deps=bpy.context.evaluated_depsgraph_get()
    ev=obj.evaluated_get(deps);mesh=ev.to_mesh()
    result=[tuple(ev.matrix_world@v.co) for v in mesh.vertices]
    ev.to_mesh_clear();return result

def signature():
    result={}
    for o in bpy.data.collections['TECH_PROBE_ASSET'].all_objects:
        if o.type=='MESH' and not o.hide_render:result[o.name]=[[round(x,6) for x in p] for p in coords(o)]
    return hashlib.sha256(json.dumps(result,sort_keys=True).encode()).hexdigest()

signatures={};marker_errors=[];finite=True
scene.frame_set(1)
initial=coords(marker)
head_rest=rig.pose.bones['head'].matrix.copy()
head_inverse=head_rest.inverted()
local_points=[head_inverse@Vector(p) for p in initial]
neutral_sleeve=coords(sleeve)
for frame in range(1,97):
    scene.frame_set(frame)
    pts=coords(marker)
    expected=[rig.pose.bones['head'].matrix@p for p in local_points]
    marker_errors.append(max((Vector(p)-q).length for p,q in zip(pts,expected)))
    finite=finite and all(math.isfinite(x) for obj in [marker,sleeve] for p in coords(obj) for x in p)
    if frame in [1,25,49,73,96]:signatures[str(frame)]=signature()
scene.frame_set(25)
reach=coords(sleeve)
max_deformation=max((Vector(a)-Vector(b)).length for a,b in zip(neutral_sleeve,reach))
scene.frame_set(1)
scene.render.filepath=str(out/'reopened_neutral.png')
t=time.perf_counter();bpy.ops.render.render(write_still=True);reopen_seconds=time.perf_counter()-t

def image_pixels(path):
    img=bpy.data.images.load(str(path),check_existing=False)
    vals=list(img.pixels[:]);bpy.data.images.remove(img);return vals
a=image_pixels(out/'neutral.png');b=image_pixels(out/'reopened_neutral.png')
pixel_error=max(abs(x-y) for x,y in zip(a,b)) if len(a)==len(b) else None

# Reuse the library collection in a genuinely fresh file and scene.
bpy.ops.wm.read_factory_settings(use_empty=True)
with bpy.data.libraries.load(str(path),link=True) as (source,target):
    assert 'TECH_PROBE_ASSET' in source.collections
    target.collections=['TECH_PROBE_ASSET']
collection=target.collections[0]
bpy.context.scene.collection.children.link(collection)
scene=bpy.context.scene
scene.render.fps=24
linked_signatures={}
for frame in [1,25,49,73,96]:
    scene.frame_set(frame);linked_signatures[str(frame)]=signature()
collection.library.filepath='//movement_pipeline_probe_v001.blend'
bpy.ops.wm.save_as_mainfile(filepath=str(out/'linked_reuse_probe_v001.blend'),relative_remap=False)
# Copy both files away from the original folder and reopen the dependent scene.
temp_dir=tempfile.TemporaryDirectory(prefix='.ota_probe_relocation_',dir=str(out))
relocated=Path(temp_dir.name).resolve()
assert relocated.is_relative_to(out), 'Scratch location must remain inside the selected output folder'
for name in ['movement_pipeline_probe_v001.blend','linked_reuse_probe_v001.blend']:
    shutil.copy2(out/name,relocated/name)
bpy.ops.wm.open_mainfile(filepath=str(relocated/'linked_reuse_probe_v001.blend'))
scene=bpy.context.scene
relocated_signatures={}
for frame in [1,25,49,73,96]:
    scene.frame_set(frame);relocated_signatures[str(frame)]=signature()
checks={
    'all_96_sampled_frames_finite':finite,
    'head_marker_max_error_below_1e-5':max(marker_errors)<1e-5,
    'weighted_sleeve_moves':max_deformation>0.05,
    'neutral_return_geometry_matches':signatures['1']==signatures['96'],
    'linked_asset_pose_geometry_matches':signatures==linked_signatures,
    'relocated_relative_library_geometry_matches':signatures==relocated_signatures,
    'reopened_render_pixels_match':pixel_error is not None and pixel_error<1e-6,
}
report={'checks':checks,'all_passed':all(checks.values()),
        'marker_max_world_error':max(marker_errors),'sleeve_max_vertex_displacement':max_deformation,
        'reopened_render_max_channel_error':pixel_error,'reopened_render_seconds':round(reopen_seconds,3),
        'original_geometry_signatures':signatures,'linked_geometry_signatures':linked_signatures,
        'relocated_geometry_signatures':relocated_signatures,
        'scope':'Generic engineering probe only; no Anu likeness, smooth-joint approval, facial acting or production performance validation.'}
(out/'verification_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('OTA_VERIFY '+json.dumps(report),flush=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
temp_dir.cleanup()
if not report['all_passed']:raise RuntimeError('Probe verification failed; inspect report')
