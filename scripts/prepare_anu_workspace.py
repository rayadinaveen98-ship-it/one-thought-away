"""Prepare a packed Anu reference workspace. This does not create a character mesh."""
import bpy, sys, json, math, hashlib
from pathlib import Path
from mathutils import Vector
args=sys.argv[sys.argv.index('--')+1:]
source=Path(args[0]).resolve();out=Path(args[1]).resolve();out.mkdir(parents=True,exist_ok=True)
bpy.context.preferences.filepaths.save_version=0
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene
scene.name='ANU_MODELING_WORKSPACE_v001'
scene.unit_settings.system='NONE'
scene['asset_id']='CH_ANU'
scene['approved_reference_sha256']='1b19b51c7d24d44c66ea0d27404e1886ea1683b5730b7b8deb1f92154efff890'
scene['status']='REFERENCE WORKSPACE ONLY; NO CHARACTER MESH OR RIG'
scene['scale_note']='Reference height normalized to one unit. Physical height is not locked.'
scene['forward_axis']='-Y; anatomical left is +X; up is +Z'
scene.render.engine='CYCLES';scene.cycles.samples=256
scene.cycles.use_adaptive_sampling=True;scene.cycles.adaptive_threshold=.01
scene.cycles.use_denoising=True
scene.render.resolution_x=2048;scene.render.resolution_y=2048
scene.render.resolution_percentage=100;scene.render.fps=24
scene.render.image_settings.file_format='OPEN_EXR'
scene.render.image_settings.color_depth='16'
scene.view_settings.view_transform='AgX'
scene.world.color=(.08,.08,.08)
refs=bpy.data.collections.new('ANU_APPROVED_REFERENCE_IMAGES');scene.collection.children.link(refs)
model=bpy.data.collections.new('ANU_MODEL_WORK_EMPTY');scene.collection.children.link(model)
review=bpy.data.collections.new('ANU_REVIEW_CAMERAS_LIGHTS');scene.collection.children.link(review)

def image_empty(name,filename,loc,rot):
    img=bpy.data.images.load(str(source/filename),check_existing=False);img.pack()
    o=bpy.data.objects.new(name,None);refs.objects.link(o)
    o.empty_display_type='IMAGE';o.data=img
    # empty_display_size is the maximum image dimension; these crops are taller.
    o.empty_display_size=1.0;o.location=loc;o.rotation_euler=rot
    o.color[3]=.65;o.empty_image_depth='BACK'
    if hasattr(o,'show_empty_image_perspective'):o.show_empty_image_perspective=False
    if hasattr(o,'show_empty_image_only_axis_aligned'):o.show_empty_image_only_axis_aligned=True
    o.hide_render=True
    o['source_filename']=filename
    o['image_sha256']=hashlib.sha256((source/filename).read_bytes()).hexdigest()
    o['role']='Approved concept crop; alignment aid, not an exact orthographic blueprint'
    return o
image_empty('REF_FRONT','anu_front_exact_crop.png',(0,.35,.5),(math.pi/2,0,0))
image_empty('REF_LEFT_PROFILE','anu_left_profile_exact_crop.png',(-.35,0,.5),(math.pi/2,0,math.pi/2))
image_empty('REF_BACK','anu_back_exact_crop.png',(0,-.35,.5),(math.pi/2,0,math.pi))
# A separate archived source card can be enabled for free-angle inspection.
gallery=image_empty('REF_THREEQUARTER_ARCHIVE','anu_threequarter_exact_crop.png',(1.4,.35,.5),(math.pi/2,0,0))
gallery.hide_set(True)

def cam(name,loc,target,scale):
    d=bpy.data.cameras.new(name);o=bpy.data.objects.new(name,d);review.objects.link(o)
    o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
    d.type='ORTHO';d.ortho_scale=scale;d.lens=70
    o['purpose']='Identity comparison after an actual model is imported';return o
front=cam('REVIEW_FRONT',(0,-3,.5),(0,0,.5),1.12)
cam('REVIEW_LEFT_PROFILE',(3,0,.5),(0,0,.5),1.12)
cam('REVIEW_BACK',(0,3,.5),(0,0,.5),1.12)
cam('REVIEW_THREEQUARTER',(1.6,-3,.9),(0,0,.52),1.16)
cam('REVIEW_FACE_CLOSEUP',(.5,-3,1.0),(0,0,.85),.48)
scene.camera=front
for name,loc,energy,size in [('KEY',(-1.5,-2,2.2),65,2),('FILL',(1.7,-1.2,1.5),25,2),('RIM',(.5,1.8,2),55,1.5)]:
    d=bpy.data.lights.new('NEUTRAL_'+name,'AREA');d.energy=energy;d.size=size
    o=bpy.data.objects.new(d.name,d);review.objects.link(o);o.location=loc
    o.rotation_euler=(Vector((0,0,.65))-o.location).to_track_quat('-Z','Y').to_euler()
text=bpy.data.texts.new('READ_ME_FIRST')
text.write('ANU APPROVED REFERENCE WORKSPACE\n\nNo character mesh or rig is present.\nThe approved reference pixels are packed inside this file.\nUse front/profile/back orthographic views for construction, while resolving the concept sheet\'s pose/proportion discrepancies explicitly.\nThe one-unit reference height is normalized, not a physical height decision.\nThe Cycles 2048-square/256-sample settings are a proposed review target, not a completed render or benchmark.\nDo not render this empty scene and present it as a character.\n')
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type=='VIEW_3D':
            space=area.spaces.active;space.region_3d.view_distance=1.5
            space.region_3d.view_location=(0,0,.5)
            space.region_3d.view_rotation=front.rotation_euler.to_quaternion()
            space.region_3d.view_perspective='ORTHO'
blend=out/'anu_reference_workspace_v001.blend'
bpy.ops.wm.save_as_mainfile(filepath=str(blend))
# Reopen in-process to verify packed references survive saving. No render is claimed.
bpy.ops.wm.open_mainfile(filepath=str(blend))
packed=[{'name':im.name,'size':list(im.size),'packed':bool(im.packed_file)} for im in bpy.data.images if im.name.endswith('.png')]
assert len(packed)==4 and all(x['packed'] for x in packed)
assert not any(o.type=='MESH' for o in bpy.context.scene.objects)
report={'asset_id':'CH_ANU','status':'REFERENCE_WORKSPACE_ONLY','blender':bpy.app.version_string,
        'build_hash':bpy.app.build_hash.decode(),'packed_references':packed,
        'no_mesh_present':True,'no_rig_present':True,'render_executed':False,
        'normalized_reference_height':1.0,'physical_scale_locked':False,
        'blend_sha256':hashlib.sha256(blend.read_bytes()).hexdigest(),
        'checks':{'saved_and_reopened':True,'four_reference_images_packed':True,'no_placeholder_character_mesh':True}}
(out/'workspace_verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('ANU_WORKSPACE '+json.dumps(report),flush=True)
