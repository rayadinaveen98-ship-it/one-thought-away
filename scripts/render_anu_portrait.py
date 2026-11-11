"""Render an actual .blend head study; never substitutes a generated image."""
import bpy,sys,json,time
from pathlib import Path
args=sys.argv[sys.argv.index('--')+1:]
blend=Path(args[0]).resolve();out=Path(args[1]).resolve();out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(blend));scene=bpy.context.scene
scene.render.engine='CYCLES';scene.cycles.samples=32
scene.cycles.use_denoising=True;scene.cycles.use_adaptive_sampling=True
scene.cycles.adaptive_threshold=.04;scene.cycles.max_bounces=6
scene.render.resolution_x=960;scene.render.resolution_y=1200
scene.render.resolution_percentage=25
devices=[]
if '--hip' not in args:
    scene.cycles.device='CPU';devices=[{'name':'CPU','type':'CPU','enabled':True}]
else:
    p=bpy.context.preferences.addons['cycles'].preferences
    p.compute_device_type='HIP';p.get_devices()
    for d in p.devices:
        d.use=d.type=='HIP';devices.append({'name':d.name,'type':d.type,'enabled':d.use})
    scene.cycles.device='GPU' if any(d['enabled'] for d in devices) else 'CPU'
scene.camera=bpy.data.objects['ANU_THREEQUARTER_REVIEW']
if '--front' in args:scene.camera=bpy.data.objects['ANU_FRONT_REVIEW']
if '--beauty' in args:
    scene.render.resolution_percentage=100;scene.cycles.samples=128;scene.cycles.adaptive_threshold=.015
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA'
name='cycles_front' if '--front' in args else 'cycles_threequarter'
if '--beauty' not in args:name+='_device_test'
scene.render.filepath=str(out/(name+'.png'))
print('ANU_CYCLES_CONFIG '+json.dumps({'device':scene.cycles.device,'devices':devices,'samples':scene.cycles.samples,'percentage':scene.render.resolution_percentage}),flush=True)
t=time.perf_counter();bpy.ops.render.render(write_still=True);elapsed=time.perf_counter()-t
report={'source_blend':blend.name,'render_file':name+'.png','engine':'CYCLES','device':scene.cycles.device,'devices':devices,
        'seconds':round(elapsed,3),'samples':scene.cycles.samples,'resolution_percentage':scene.render.resolution_percentage,
        'resolution_base':[960,1200],'status':'WIP_LIKENESS_RENDER_NOT_FINAL_CHARACTER'}
(out/(name+'_report.json')).write_text(json.dumps(report,indent=2),encoding='utf-8')
print('ANU_CYCLES_RESULT '+json.dumps(report),flush=True)
