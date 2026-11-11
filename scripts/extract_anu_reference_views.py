"""Lossless source-view extraction; requires ffmpeg on PATH. No image generation."""
import argparse,hashlib,json,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('output',type=Path)
a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
expected='1b19b51c7d24d44c66ea0d27404e1886ea1683b5730b7b8deb1f92154efff890'
assert hashlib.sha256(a.source.read_bytes()).hexdigest()==expected,'Unexpected source image'
rects=[('front',145,82,282,552,'c9ed6d9ecae205083adb17646154827156be862df46a659693c9863587021a9c'),
       ('left_profile',821,82,252,552,'5c8e2a696690be628599bede12060493a4abc3c814d734cf2238aed0fc5dfc2e'),
       ('back',1115,82,292,552,'aa6e00922df38d0969e7180f90af98b0ada473e638f9da70651149245d31c471'),
       ('threequarter',485,82,282,552,None)]
records=[]
for view,x,y,w,h,pixel_hash in rects:
    dest=a.output/f'anu_{view}_exact_crop.png'
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(a.source),'-vf',f'crop={w}:{h}:{x}:{y}','-frames:v','1',str(dest)],check=True)
    raw=subprocess.check_output(['ffmpeg','-hide_banner','-loglevel','error','-i',str(dest),'-pix_fmt','rgb24','-f','hash','-hash','sha256','-'],text=True).strip().split('=')[-1]
    if pixel_hash:assert raw==pixel_hash,f'Pixel mismatch for {view}'
    records.append({'view':view,'filename':dest.name,'crop_xywh':[x,y,w,h],
                    'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'rgb_pixel_sha256':raw})
receipt={'asset_id':'CH_ANU','source_sha256':expected,'method':'Exact rectangular crop; no scaling, repainting or AI regeneration','views':records}
(a.output/'crop_receipt.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
print(json.dumps(receipt,indent=2))
