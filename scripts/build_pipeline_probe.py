"""Blender 5.3 engineering probe. No Anu likeness or production proportions."""
import bpy, math, json, time, sys, hashlib
from pathlib import Path
from mathutils import Vector

OUT = Path(sys.argv[sys.argv.index('--')+1]).resolve()
OUT.mkdir(parents=True, exist_ok=True)
bpy.context.preferences.filepaths.save_version=0
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene
scene.render.engine='BLENDER_EEVEE'
scene.render.resolution_x=800
scene.render.resolution_y=640
scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
scene.render.fps=24
scene.frame_start=1
scene.frame_end=96
scene.world.color=(0.15,0.15,0.15)
scene.view_settings.view_transform='AgX'

def mat(name,color,metal=0):
    m=bpy.data.materials.new(name); m.diffuse_color=(*color,1)
    m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value=(*color,1)
    p.inputs['Roughness'].default_value=0.62
    p.inputs['Metallic'].default_value=metal
    return m
teal=mat('Probe teal',(0.06,0.38,0.4))
dark=mat('Joints',(0.045,0.08,0.12))
gold=mat('Attachment marker',(0.95,0.5,0.08))
floor=mat('Stage',(0.12,0.16,0.21))
white=mat('Lettering',(0.82,0.9,0.93))

arm=bpy.data.armatures.new('PROBE_SKELETON')
rig=bpy.data.objects.new('TECH_PROBE_RIG',arm)
scene.collection.objects.link(rig)
bpy.context.view_layer.objects.active=rig
rig.select_set(True)
bpy.ops.object.mode_set(mode='EDIT')
spec=[('root',(0,0,0),(0,0,0.3),None),
('pelvis',(0,0,0.92),(0,0,1.12),'root'),
('spine',(0,0,1.12),(0,0,1.65),'pelvis'),
('neck',(0,0,1.65),(0,0,1.8),'spine'),
('head',(0,0,1.8),(0,0,2.12),'neck')]
for side,s in [('L',1),('R',-1)]:
    spec += [(f'upper_arm.{side}',(s*.24,0,1.58),(s*.63,0,1.38),'spine'),
             (f'forearm.{side}',(s*.63,0,1.38),(s*.94,0,1.18),f'upper_arm.{side}'),
             (f'hand.{side}',(s*.94,0,1.18),(s*1.08,0,1.10),f'forearm.{side}'),
             (f'thigh.{side}',(s*.16,0,.96),(s*.18,-.015,.53),'pelvis'),
             (f'shin.{side}',(s*.18,-.015,.53),(s*.18,0,.12),f'thigh.{side}'),
             (f'foot.{side}',(s*.18,0,.12),(s*.18,-.23,.09),f'shin.{side}')]
for name,h,t,parent in spec:
    b=arm.edit_bones.new(name);b.head=h;b.tail=t
    if parent:b.parent=arm.edit_bones[parent]
bpy.ops.object.mode_set(mode='OBJECT')
rig['purpose']='Generic articulated engineering probe. NOT ANU. No approved character design.'
rig['release_status']='TECHNICAL TEST ONLY'
rig.show_in_front=True

def bind(obj,bone):
    # Vertices are in rest-world coordinates; armature modifier applies pose.
    bpy.context.view_layer.objects.active=obj
    obj.select_set(True)
    bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
    vg=obj.vertex_groups.new(name=bone)
    vg.add(list(range(len(obj.data.vertices))),1,'REPLACE')
    mod=obj.modifiers.new('Probe armature','ARMATURE');mod.object=rig
    obj.data.materials.append(teal)
    obj.select_set(False)

def ball(name,p,scale,material,bone=None):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=20,ring_count=12,location=p)
    o=bpy.context.object;o.name=name;o.scale=scale
    for f in o.data.polygons:f.use_smooth=True
    if bone:bind(o,bone);o.data.materials.clear()
    o.data.materials.append(material)
    return o

for name,h,t,parent in spec:
    if name in ['root','pelvis','spine','neck','head']:continue
    a,b=Vector(h),Vector(t);d=b-a
    radius=.072 if 'arm' in name else .095
    if 'hand' in name:radius=.085
    if 'foot' in name:radius=.105
    bpy.ops.mesh.primitive_cylinder_add(vertices=20,radius=radius,depth=d.length*.82,location=(a+b)/2)
    o=bpy.context.object;o.name='SEGMENT_'+name
    o.rotation_euler=d.to_track_quat('Z','Y').to_euler()
    bind(o,name)
    bevel=o.modifiers.new('Rounded edge','BEVEL');bevel.width=.025;bevel.segments=3
    for p in o.data.polygons:p.use_smooth=True
    ball('JOINT_'+name,a,(radius*.85,)*3,dark,name)
ball('Torso',(0,0,1.36),(.25,.15,.31),teal,'spine')
ball('Hip',(0,0,1.00),(.25,.15,.15),teal,'pelvis')
ball('Head_no_face',(0,0,1.99),(.19,.16,.23),teal,'head')
ball('Head_attachment_marker',(.15,-.015,2.15),(.065,.065,.065),gold,'head')
ball('Neck_joint',(0,0,1.73),(.065,.065,.12),dark,'neck')

# One continuous two-bone weighted sleeve. It is a technical deformation sample,
# not a claim about child anatomy, skinning quality or final costume feasibility.
a=Vector((.24,0,1.58));b=Vector((.94,0,1.18));axis=(b-a).normalized()
u=Vector((0,1,0));v=axis.cross(u).normalized()
verts=[];faces=[];rings=17;sides=16
for i in range(rings):
    c=a.lerp(b,i/(rings-1))
    for j in range(sides):
        angle=j*math.tau/sides
        verts.append(c+.087*(u*math.cos(angle)+v*math.sin(angle)))
for i in range(rings-1):
    for j in range(sides):
        k=i*sides+j;kn=i*sides+(j+1)%sides
        faces.append((k,kn,kn+sides,k+sides))
mesh=bpy.data.meshes.new('WeightedSleeveMesh');mesh.from_pydata(verts,[],faces);mesh.update()
sleeve=bpy.data.objects.new('Continuous_weighted_sleeve.L',mesh);scene.collection.objects.link(sleeve)
sleeve.data.materials.append(gold)
g1=sleeve.vertex_groups.new(name='upper_arm.L');g2=sleeve.vertex_groups.new(name='forearm.L')
for i in range(rings):
    t=i/(rings-1);w=max(0,min(1,(t-.40)/.3))
    ids=list(range(i*sides,(i+1)*sides));g1.add(ids,1-w,'REPLACE');g2.add(ids,w,'REPLACE')
mod=sleeve.modifiers.new('Two bone blend','ARMATURE');mod.object=rig;mod.use_deform_preserve_volume=True
for p in mesh.polygons:p.use_smooth=True
# The continuous sleeve replaces these display solids; keeping both creates
# surface intersections that would obscure inspection of the weighted mesh.
for name in ['SEGMENT_upper_arm.L','SEGMENT_forearm.L','JOINT_forearm.L']:
    bpy.data.objects[name].hide_render=True
    bpy.data.objects[name].hide_set(True)

poses={1:{},25:{'upper_arm.L':(0,0,-35),'forearm.L':(0,0,-55),'head':(0,0,12)},
       49:{'spine':(14,0,0),'neck':(-8,0,0),'upper_arm.L':(-15,0,-20),'upper_arm.R':(-15,0,20)},
       73:{'head':(0,25,0),'neck':(0,0,-8)},96:{}}
for frame,values in poses.items():
    for pb in rig.pose.bones:
        pb.rotation_mode='XYZ';pb.rotation_euler=[math.radians(x) for x in values.get(pb.name,(0,0,0))]
        pb.keyframe_insert(data_path='rotation_euler',frame=frame)

bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=1.55,depth=.08,location=(0,0,-.04))
bpy.context.object.name='Test plinth';bpy.context.object.data.materials.append(floor)
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.085))
bpy.context.object.data.materials.append(mat('Backdrop',(.035,.055,.08)))

def area(name,loc,power,size):
    d=bpy.data.lights.new(name,'AREA');d.energy=power;d.shape='DISK';d.size=size
    o=bpy.data.objects.new(name,d);scene.collection.objects.link(o);o.location=loc
    o.rotation_euler=(Vector((0,0,1.1))-o.location).to_track_quat('-Z','Y').to_euler()
area('Key',(-3,-4,6),700,5)
area('Fill',(4,-1,3),450,4)
area('Rim',(1,3,4),900,3)
d=bpy.data.cameras.new('ReviewCamera');cam=bpy.data.objects.new('ReviewCamera',d);scene.collection.objects.link(cam)
cam.location=(3.2,-6,3.0);cam.rotation_euler=(Vector((0,0,1.03))-cam.location).to_track_quat('-Z','Y').to_euler()
d.type='ORTHO';d.ortho_scale=4.0;scene.camera=cam

def label(name,body,loc,size):
    c=bpy.data.curves.new(name,'FONT');c.body=body;c.align_x='CENTER';c.size=size
    o=bpy.data.objects.new(name,c);scene.collection.objects.link(o)
    # Camera-local offset gives fixed review labels, independent of animation.
    o.parent=cam;o.location=loc;o.rotation_euler=(0,0,0);o.data.materials.append(white)
label('Title','MOVEMENT / PIPELINE PROBE',(0,1.43,-4),.105)
label('Disclaimer','TECHNICAL TEST ONLY - NOT ANU',(0,1.26,-4),.065)
label('Footer','weighted sleeve / rigid head marker / 24 fps',(0,-1.45,-4),.065)
# Keep the labels legible regardless of the probe's lighting.
textmat=mat('Review text',(.8,.9,1))
nodes=textmat.node_tree.nodes;nodes.clear()
emit=nodes.new('ShaderNodeEmission');emit.inputs['Color'].default_value=(.8,.9,1,1)
out=nodes.new('ShaderNodeOutputMaterial');textmat.node_tree.links.new(emit.outputs[0],out.inputs[0])
for obj in scene.objects:
    if obj.type=='FONT':obj.data.materials.clear();obj.data.materials.append(textmat)

asset=bpy.data.collections.new('TECH_PROBE_ASSET');scene.collection.children.link(asset)
for obj in list(scene.objects):
    if obj==rig or (obj.type=='MESH' and any(m.type=='ARMATURE' and m.object==rig for m in obj.modifiers)):
        for col in list(obj.users_collection):col.objects.unlink(obj)
        asset.objects.link(obj)

scene['test_scope']='Generic FK bone motion, weighted sleeve, attached marker, save/reopen and preview rendering only.'
scene['limitations']='No Anu likeness; no facial rig; no IK/contact pass; no production performance claim.'
scene.frame_set(1)
bpy.context.view_layer.objects.active=rig
bpy.ops.object.select_all(action='DESELECT');rig.select_set(True)
blend=OUT/'movement_pipeline_probe_v001.blend'
bpy.ops.wm.save_as_mainfile(filepath=str(blend))
timings=[]
for frame,name in [(1,'neutral'),(25,'reach'),(49,'lean'),(73,'head_turn')]:
    scene.frame_set(frame);scene.render.filepath=str(OUT/f'{name}.png')
    t=time.perf_counter();bpy.ops.render.render(write_still=True)
    timings.append({'frame':frame,'pose':name,'seconds':round(time.perf_counter()-t,3)})
report={'schema_version':1,'asset':'GENERIC_TECH_PROBE','not_anu':True,'blender':bpy.app.version_string,
        'build_hash':bpy.app.build_hash.decode(),'engine':scene.render.engine,'resolution':[800,640],
        'fps':24,'frame_range':[1,96],'bones':len(arm.bones),'objects':len(scene.objects),
        'timings':timings,'save_sha256':hashlib.sha256(blend.read_bytes()).hexdigest(),
        'limitations':['Not character likeness evidence','Not a facial rig','FK probe; no foot contact validation','No production cost extrapolation']}
(OUT/'build_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('OTA_PROBE_BUILD '+json.dumps(report),flush=True)
# Sparse, low-resolution motion preview: 24 sampled frames over four seconds.
# This is a technical motion proxy, not film animation or a playback benchmark.
scene.render.resolution_percentage=50
frames=OUT/'preview_frames';frames.mkdir(exist_ok=True)
for frame in range(1,97,4):
    scene.frame_set(frame);scene.render.filepath=str(frames/f'frame_{frame:03d}.png')
    bpy.ops.render.render(write_still=True)
print('OTA_PREVIEW_COMPLETE',flush=True)
