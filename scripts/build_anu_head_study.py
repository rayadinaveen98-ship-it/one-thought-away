"""Local Anu likeness study. Editable 3D geometry; not a final model or facial rig."""
import bpy, math, json, sys, hashlib, time
from pathlib import Path
from mathutils import Vector
from math import sin, cos, pi, exp, sqrt
args=sys.argv[sys.argv.index('--')+1:]
out=Path(args[0]).resolve();out.mkdir(parents=True,exist_ok=True)
reference=Path(args[1]).resolve()
assert hashlib.sha256(reference.read_bytes()).hexdigest()=='1b19b51c7d24d44c66ea0d27404e1886ea1683b5730b7b8deb1f92154efff890'
bpy.context.preferences.filepaths.save_version=0
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene
scene.name='ANU_HEAD_LIKENESS_STUDY_v007'
scene['status']='WORK IN PROGRESS; LIKENESS NOT YET ACCEPTED; NOT A FACIAL RIG'
scene['source_sha256']='1b19b51c7d24d44c66ea0d27404e1886ea1683b5730b7b8deb1f92154efff890'
scene['construction']='Parametric surface sculpt with separate orbital patches and sculptable hair locks. Retopology required before animation.'

def material(name,color,rough=.5):
    m=bpy.data.materials.new(name);m.use_nodes=True;m.diffuse_color=(*color,1)
    p=m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough
    p.inputs['Specular IOR Level'].default_value=.32
    return m,p
skin,sp=material('ANU_SKIN_study',(.37,.175,.082),.53)
sp.inputs['Subsurface Weight'].default_value=.10
sp.inputs['Subsurface Radius'].default_value=(.12,.06,.035)
sp.inputs['Subsurface Scale'].default_value=.10
lip,lp=material('ANU_LIPS_natural',(.32,.13,.079),.64)
crease,_=material('ANU_CREASE_warm',(.12,.041,.025),.75)
hair,hp=material('ANU_HAIR_dark_brown',(.026,.012,.007),.57)
hp.inputs['Specular IOR Level'].default_value=.12
if 'Anisotropic IOR Level' in hp.inputs:hp.inputs['Anisotropic IOR Level'].default_value=.5
hair_light,_=material('ANU_HAIR_warm_lock',(.039,.020,.011),.57)
hair_shadow,_=material('ANU_HAIR_deep_lock',(.015,.007,.004),.59)
for hm in [hair,hair_light,hair_shadow]:
    hm.node_tree.nodes.get('Principled BSDF').inputs['Roughness'].default_value=.66
    hm.node_tree.nodes.get('Principled BSDF').inputs['Specular IOR Level'].default_value=.12
    nodes=hm.node_tree.nodes;links=hm.node_tree.links
    noise=nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=150
    noise.inputs['Detail'].default_value=2
    bump=nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.16;bump.inputs['Distance'].default_value=.003
    links.new(noise.outputs['Fac'],bump.inputs['Height']);links.new(bump.outputs['Normal'],nodes.get('Principled BSDF').inputs['Normal'])
eye_white,_=material('ANU_EYE_sclera',(.70,.66,.57),.24)
iris,ip=material('ANU_EYE_brown_iris',(.038,.013,.004),.27)
ip.inputs['Coat Weight'].default_value=.25;ip.inputs['Coat Roughness'].default_value=.09
ip.inputs['Specular IOR Level'].default_value=.25
pupil,pp=material('ANU_EYE_pupil',(.003,.0015,.001),.18)
pp.inputs['Coat Weight'].default_value=.35;pp.inputs['Coat Roughness'].default_value=.06
clip,cp=material('ANU_CLIP_butterfly_yellow',(.95,.53,.035),.38)
dress,dp=material('ANU_DRESS_yellow_cotton',(.70,.37,.045),.77)
dp.inputs['Sheen Weight'].default_value=.22
inner_ear,_=material('ANU_EAR_concha',(.30,.117,.065),.65)

def mesh_obj(name,verts,faces,mat):
    m=bpy.data.meshes.new(name+'_mesh');m.from_pydata(verts,[],faces);m.update()
    o=bpy.data.objects.new(name,m);scene.collection.objects.link(o)
    o.data.materials.append(mat)
    for p in m.polygons:p.use_smooth=True
    return o

def uv(name,loc,scale,mat,seg=48,rings=32):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg,ring_count=rings,location=loc)
    o=bpy.context.object;o.name=name;o.scale=scale;o.data.materials.append(mat)
    for p in o.data.polygons:p.use_smooth=True
    return o

def curve(name,points,radius,mat,radii=None):
    c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.resolution_u=16
    c.bevel_depth=radius;c.bevel_resolution=4;c.resolution_u=24
    s=c.splines.new('NURBS');s.points.add(len(points)-1)
    for i,(p,v) in enumerate(zip(s.points,points)):
        p.co=(*v,1)
        if radii:p.radius=radii[i]
    s.order_u=min(4,len(points));s.use_endpoint_u=True
    o=bpy.data.objects.new(name,c);scene.collection.objects.link(o);o.data.materials.append(mat);return o

def interp(z,knots):
    if z<=knots[0][0]:return knots[0][1]
    for k,((a,u),(b,v)) in enumerate(zip(knots,knots[1:])):
        if z<=b:
            t=(z-a)/(b-a)
            prev=knots[max(0,k-1)];nxt=knots[min(len(knots)-1,k+2)]
            m0=(v-prev[1])/(b-prev[0])
            m1=(nxt[1]-u)/(nxt[0]-a)
            value=(2*t**3-3*t*t+1)*u+(t**3-2*t*t+t)*(b-a)*m0+(-2*t**3+3*t*t)*v+(t**3-t*t)*(b-a)*m1
            return max(min(u,v),min(max(u,v),value))
    return knots[-1][1]
width=[(-.02,.015),(.02,.12),(.09,.26),(.20,.37),(.35,.44),(.50,.46),(.65,.465),(.80,.45),(.95,.37),(1.065,.20),(1.12,.012)]
depth=[(-.02,.02),(.06,.24),(.19,.365),(.35,.405),(.55,.395),(.72,.37),(.90,.33),(1.04,.21),(1.12,.012)]
back_depth=[(-.02,.02),(.13,.25),(.4,.39),(.7,.42),(.95,.33),(1.12,.012)]

def gauss(x,z,cx,cz,sx,sz):return exp(-((x-cx)/sx)**2-((z-cz)/sz)**2)
def facial_offset(x,z):
    y=0
    # Integrated cheek, nose, muzzle and chin volumes on a continuous head mesh.
    y-=.048*(gauss(x,z,.275,.35,.13,.15)+gauss(x,z,-.275,.35,.13,.15))
    y+=.010*(gauss(x,z,.195,.60,.145,.105)+gauss(x,z,-.195,.60,.145,.105))
    y-=.018*gauss(x,z,0,.58,.065,.19)
    y-=.068*gauss(x,z,0,.425,.055,.072)
    y-=.025*(gauss(x,z,.045,.395,.035,.042)+gauss(x,z,-.045,.395,.035,.042))
    y-=.018*gauss(x,z,0,.27,.15,.07)
    y-=.020*gauss(x,z,0,.105,.13,.075)
    return y
def face_y(x,z):
    w=interp(z,width);d=interp(z,depth)
    base=-d*sqrt(max(0,1-min(.9999,(x/max(w,.001))**2)))+facial_offset(x,z)
    # Integrate the orbital form into the continuous face. The eyelid opening
    # is cut below; there is no visible floating skin annulus in this revision.
    for side in [-1,1]:
        dx=x-side*.195;dz=z-.60
        height=.072 if dz>=0 else .055
        radius=sqrt((dx/.115)**2+(dz/height)**2)
        if .001<radius<2.15:
            ix=dx/radius;iz=dz/radius
            inner=-.290-sqrt(max(.00001,.120**2-ix*ix-iz*iz))-.006
            t=max(0,min(1,(radius-1)/1.15));t=t*t*(3-2*t)
            base=inner*(1-t)+base*t
    return base

# Dense ring construction makes a continuous, editable face/head surface.
verts=[];faces=[];nz=128;na=192
for i in range(nz):
    z=-.02+1.14*i/(nz-1);w=interp(z,width);df=interp(z,depth);db=interp(z,back_depth)
    for j in range(na):
        a=2*pi*j/na;x=w*sin(a);co=cos(a)
        y=-(df if co>=0 else db)*co
        if co>0:y=face_y(x,z)
        verts.append((x,y,z))
for i in range(nz-1):
    for j in range(na):
        k=i*na+j;n=i*na+(j+1)%na;faces.append((k,n,n+na,k+na))
faces.append(tuple(range(na-1,-1,-1)));faces.append(tuple((nz-1)*na+j for j in range(na)))
head=mesh_obj('ANU_HEAD_continuous_surface',verts,faces,skin)
sub=head.modifiers.new('Sculpt surface refinement','SUBSURF');sub.levels=1;sub.render_levels=1
# Evaluate the smooth surface before cutting two clean almond openings.
bpy.context.view_layer.objects.active=head;head.select_set(True)
bpy.ops.object.modifier_apply(modifier=sub.name)
for side in [-1,1]:
    cv=[];cf=[];count=128
    for yy in [-.85,.08]:
        for j in range(count):
            angle=2*pi*j/count;dx=.115*cos(angle)
            dz=(.072 if sin(angle)>=0 else .055)*sin(angle)+side*.013*cos(angle)
            cv.append((side*.195+dx,yy,.60+dz))
    for j in range(count):cf.append((j,(j+1)%count,(j+1)%count+count,j+count))
    cf.append(tuple(range(count-1,-1,-1)));cf.append(tuple(count+j for j in range(count)))
    cutter=mesh_obj('TEMP_eye_opening',cv,cf,skin)
    import bmesh
    bm=bmesh.new();bm.from_mesh(cutter.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(cutter.data);bm.free()
    boolean=head.modifiers.new('Integrated eye opening','BOOLEAN');boolean.operation='DIFFERENCE';boolean.solver='EXACT';boolean.object=cutter
    bpy.context.view_layer.objects.active=head
    bpy.ops.object.modifier_apply(modifier=boolean.name)
    bpy.data.objects.remove(cutter,do_unlink=True)

# Neck and shoulder bust, intentionally stopping before a full body claim.
uv('ANU_NECK',(0,.065,-.145),(.17,.155,.30),skin)
v=[];f=[];rows=32;cols=96
for i in range(rows):
    t=i/(rows-1);z=-.62+.42*t
    rx=interp(z,[(-.62,.45),(-.36,.51),(-.29,.48),(-.25,.36),(-.20,.19)])
    ry=interp(z,[(-.62,.25),(-.30,.23),(-.20,.16)])
    for j in range(cols):
        a=2*pi*j/cols
        zz=z+.04*sin(a)**2*t
        v.append((rx*sin(a),.065-ry*cos(a),zz))
for i in range(rows-1):
    for j in range(cols):
        k=i*cols+j;n=i*cols+(j+1)%cols;f.append((k,n,n+cols,k+cols))
mesh_obj('ANU_DRESS_shoulder_study',v,f,dress)
curve('ANU_DRESS_neckline',[(.19*sin(a),.065-.16*cos(a),-.20+.04*sin(a)**2) for a in [2*pi*i/64 for i in range(65)]],.012,dress)

eye_cz=.60;eye_r=.120;eye_y=-.290
for s,side in [(-1,'R'),(1,'L')]:
    cx=s*.195
    eyeball=uv('ANU_EYE_'+side,(cx,eye_y,eye_cz),(eye_r,eye_r,eye_r),eye_white,64,48)
    eyeball.hide_render=True
    # Show only the spherical surface within the lid opening, avoiding overlap
    # between the display eye shell and the separate sculpt-stage orbital patch.
    sv=[(cx,eye_y-eye_r,eye_cz)];sf=[];sr=20;ss=128
    for i in range(1,sr+1):
        t=i/sr
        for j in range(ss):
            angle=2*pi*j/ss;dx=.115*t*cos(angle)
            dz=(.072 if sin(angle)>=0 else .055)*t*sin(angle)+s*.013*t*cos(angle)
            sv.append((cx+dx,eye_y-sqrt(max(.00001,eye_r**2-dx**2-dz**2)),eye_cz+dz))
    for j in range(ss):sf.append((0,1+j,1+(j+1)%ss))
    for i in range(sr-1):
        a=1+i*ss;b=a+ss
        for j in range(ss):sf.append((a+j,b+j,b+(j+1)%ss,a+(j+1)%ss))
    mesh_obj('ANU_SCLERA_OPENING_'+side,sv,sf,eye_white)
    # Curved iris and pupil patches on the spherical eye surface.
    for label,radius,mat,offset in [('IRIS',.066,iris,.0018),('PUPIL',.030,pupil,.0028)]:
        vv=[(cx,eye_y-eye_r-offset,eye_cz)];ff=[];rr=14;ss=96
        for i in range(1,rr+1):
            r=radius*i/rr
            for j in range(ss):
                a=2*pi*j/ss;dx=r*cos(a);dz=r*sin(a)
                yy=eye_y-sqrt(max(.0001,eye_r**2-dx**2-dz**2))-offset
                vv.append((cx+dx,yy,eye_cz+dz))
        for j in range(ss):ff.append((0,1+j,1+(j+1)%ss))
        for i in range(rr-1):
            a=1+i*ss;b=a+ss
            for j in range(ss):ff.append((a+j,b+j,b+(j+1)%ss,a+(j+1)%ss))
        mesh_obj('ANU_'+label+'_'+side,vv,ff,mat)
    # Skin annulus hides the eye outside an almond-shaped opening.
    vv=[];ff=[];rings=14;segments=128;upper=[];lower=[];fold=[]
    for i in range(rings):
        t=i/(rings-1);rx=.115+.085*t
        for j in range(segments):
            a=2*pi*j/segments;inner_h=(.072 if sin(a)>=0 else .055);h=inner_h+.10*t
            x=cx+rx*cos(a);z=eye_cz+h*sin(a)+s*.013*cos(a)
            ix=.115*cos(a);iz=inner_h*sin(a)+s*.013*cos(a)
            base=face_y(x,z)-.002
            inner=eye_y-sqrt(max(.00001,eye_r**2-ix*ix-iz*iz))-.006
            # The hidden eyeball does not need a raised circular skin cover.
            # Blend the actual lid edge smoothly into the surrounding face.
            blend=t*t*(3-2*t)
            y=inner*(1-blend)+base*blend-.003*sin(pi*t)
            vv.append((x,y,z))
            if i==0:
                (upper if sin(a)>=0 else lower).append((x,y-.001,z))
    for i in range(rings-1):
        for j in range(segments):
            k=i*segments+j;n=i*segments+(j+1)%segments;ff.append((k,n,n+segments,k+segments))
    orbital_reference=mesh_obj('ANU_ORBIT_LIDS_'+side,vv,[tuple(reversed(face)) for face in ff],skin)
    orbital_reference.hide_render=True;orbital_reference.hide_set(True)
    curve('ANU_UPPER_LID_EDGE_'+side,upper,.0022,hair_shadow)
    curve('ANU_LOWER_LID_EDGE_'+side,lower,.0018,lip)
    # Thick but natural brows, built as tapered sculptable locks.
    pts=[];radii=[]
    for i in range(13):
        t=i/12;x=s*(.090+.25*t);z=.750+.028*sin(pi*t)-.025*t
        pts.append((x,face_y(x,z)-.009,z));radii.append(.12+.88*(1-t)**.4)
    curve('ANU_BROW_'+side,pts,.014,hair_shadow,radii)
    # Small nostrils on the integrated nose surface.
    pts=[]
    for i in range(13):
        a=pi*i/12;x=s*(.042+.014*cos(a));z=.390-.007*sin(a)
        pts.append((x,face_y(x,z)-.002,z))
    curve('ANU_NOSTRIL_'+side,pts,.004,crease)
    # Ear pinna and helix; joins sit behind the side locks.
    uv('ANU_EAR_'+side,(s*.444,-.13,.48),(.085,.06,.145),skin)
    uv('ANU_EAR_INNER_'+side,(s*.488,-.173,.48),(.026,.019,.085),inner_ear)
    pts=[]
    for i in range(30):
        a=2*pi*i/29;pts.append((s*(.48+.025*cos(a)),-.181-.006*cos(a),.48+.105*sin(a)))
    curve('ANU_EAR_HELIX_'+side,pts,.010,skin)

# Closed natural lips, with a subtle smile. No teeth asset/acting claim yet.
for upper in [True,False]:
    vv=[];ff=[];nx=64;ny=10
    for i in range(nx):
        x=-.145+.29*i/(nx-1);q=x/.145;fall=max(0,1-q*q)
        line=.222+.014*q*q
        for j in range(ny):
            t=j/(ny-1)
            extent=(.022*(.8+.2*cos(q*2*pi)) if upper else -.028)*fall
            z=line+extent*t
            y=face_y(x,z)-.002-.006*sin(pi*t)*fall-.003*fall
            vv.append((x,y,z))
    for i in range(nx-1):
        for j in range(ny-1):
            a=i*ny+j;ff.append((a,a+ny,a+ny+1,a+1))
    mesh_obj('ANU_LIP_'+('UPPER' if upper else 'LOWER'),vv,ff if upper else [tuple(reversed(face)) for face in ff],lip)
pts=[]
for i in range(49):
    x=-.145+.29*i/48;z=.222+.014*(x/.145)**2
    pts.append((x,face_y(x,z)-.008,z))
curve('ANU_MOUTH_CONTACT',pts,.0029,crease,[.15+.85*sin(pi*i/48) for i in range(49)])

# Sculptable hair shell, opened at the forehead. No opaque helmet over the face.
hair_w=[(-.13,.37),(.02,.53),(.30,.59),(.60,.56),(.85,.50),(1.04,.36),(1.16,.15),(1.20,.02)]
hair_d=[(-.13,.32),(.02,.40),(.4,.47),(.75,.46),(1.0,.37),(1.16,.16),(1.20,.02)]
vv=[];ff=[];nr=55;ns=160
for i in range(nr):
    t=i/(nr-1)
    for j in range(ns):
        a=2*pi*j/ns;c=cos(a)
        weight=max(0,min(1,(c-.05)/.40))
        weight=weight*weight*(3-2*weight)
        front_hairline=.98-.07*sin(2*a)**2
        bottom=front_hairline*weight-.07*(1-weight)
        z=1.20*(1-t)+bottom*t
        w=interp(z,hair_w);d=interp(z,hair_d)
        wave=(.012*sin(7*a+z*10)+.009*sin(13*a-z*7))*sin(pi*t/2)
        vv.append(((w+wave)*sin(a),.035-(d+wave)*cos(a),z))
for i in range(nr-1):
    for j in range(ns):
        a=i*ns+j;b=i*ns+(j+1)%ns;ff.append((a,b,b+ns,a+ns))
ff.append(tuple(range(ns-1,-1,-1)))
mesh_obj('ANU_HAIR_main_mass',vv,[tuple(reversed(face)) for face in ff],hair)

def catmull(points,t):
    p=[Vector(points[0])]+[Vector(x) for x in points]+[Vector(points[-1])]
    n=len(points)-1;u=min(n-1,int(t*n));f=min(1,t*n-u)
    a,b,c,d=p[u:u+4]
    return .5*((2*b)+(-a+c)*f+(2*a-5*b+4*c-d)*f*f+(-a+3*b-3*c+d)*f*f*f)
def lock(name,points,width,thickness,mat):
    vv=[];ff=[];steps=40;sides=12
    for i in range(steps):
        t=i/(steps-1);c=catmull(points,t)
        prev=catmull(points,max(0,t-.005));nxt=catmull(points,min(1,t+.005));tangent=(nxt-prev).normalized()
        # Orient the wide dimension tangentially to the head, not arbitrarily.
        outward=Vector((c.x,c.y-.035,.10)).normalized()
        u=tangent.cross(outward).normalized()
        if u.length<.1:u=Vector((1,0,0))
        v=tangent.cross(u).normalized()
        taper=(.25+.75*sin(pi*(.12+.82*t)))*max(.035,(1-t)**.32)
        for j in range(sides):
            a=2*pi*j/sides
            rib=1+.055*cos(4*a+2*t)
            vv.append(c+u*(width*taper*cos(a)*rib)+v*(thickness*taper*sin(a)))
    for i in range(steps-1):
        for j in range(sides):
            a=i*sides+j;b=i*sides+(j+1)%sides;ff.append((a,b,b+sides,a+sides))
    ff.append(tuple(range(sides-1,-1,-1)));ff.append(tuple((steps-1)*sides+j for j in range(sides)))
    o=mesh_obj(name,vv,ff,mat)
    sub=o.modifiers.new('Lock refinement','SUBSURF');sub.levels=1;sub.render_levels=1
    # Sparse modeled strand accents add readable surface flow without a groom
    # dependency or simulation. They remain editable curve objects.
    for strand,offset in enumerate([-.48,0,.48]):
        line=[]
        for k in range(18):
            t=.04+.90*k/17;c=catmull(points,t)
            tangent=(catmull(points,min(1,t+.005))-catmull(points,max(0,t-.005))).normalized()
            outward=Vector((c.x,c.y-.035,.10)).normalized();u=tangent.cross(outward).normalized()
            v=tangent.cross(u).normalized()
            if v.dot(outward)<0:v=-v
            taper=(.25+.75*sin(pi*(.12+.82*t)))*max(.035,(1-t)**.32)
            line.append(c+u*(width*taper*offset)+v*(thickness*taper*sqrt(1-offset*offset)+.001))
        curve(name+'_strand_%d'%strand,line,.0009,hair_shadow if strand!=1 else hair_light)
    return o
# Asymmetric fringe sweeps from the part toward her anatomical right.
fringes=[[(.17,-.30,1.15),(-.02,-.42,1.10),(-.24,-.46,.98),(-.37,-.43,.80)],
[(.22,-.28,1.13),(.02,-.46,1.03),(-.16,-.48,.93),(-.29,-.46,.86)],
[(.10,-.35,1.12),(-.11,-.46,1.04),(-.31,-.47,.91),(-.39,-.43,.74)],
[(.23,-.29,1.12),(.34,-.40,1.01),(.41,-.42,.85),(.44,-.36,.73)]]
for i,ps in enumerate(fringes):lock('ANU_HAIR_fringe_%02d'%i,ps,.09 if i<3 else .075,.018,[hair,hair_light,hair_shadow,hair][i])
for k in range(7):
    points=[(.20-.02*k,-.36,1.14-.012*k),(.02-.03*k,-.48,1.03-.015*k),
            (-.16-.025*k,-.49,.94-.020*k),(-.24-.022*k,-.47,.86-.018*k)]
    lock('ANU_HAIR_fine_fringe_%02d'%k,points,.025-.0015*k,.008,hair)
# Layered shoulder-length side and back locks; broad volumes retain a modelable silhouette.
for side,s in [('L',1),('R',-1)]:
    for k in range(8):
        a=.72+k*.19
        x=s*(.53+.045*sin(k*1.7));yy=-.24+k*.075
        ps=[(s*.29,yy*.6,1.04-k*.016),(x,yy,.73),
            (s*(.59+.045*sin(k*1.5)),yy+.025,.53),
            (s*(.52+.035*cos(k*2)),yy-.035,.32),
            (s*(.59+.035*cos(k*2)),yy+.035,.13),
            (s*(.41+.05*sin(k)),yy-.01,-.055-.035*cos(k))]
        lock('ANU_HAIR_side_'+side+'_%02d'%k,ps,.077+.007*(k%3),.022,[hair,hair_light,hair_shadow][k%3])
for k in range(11):
    a=1.25+3.78*k/10
    ps=[(.26*sin(a),.035-.28*cos(a),1.09),
        (.49*sin(a),.035-.43*cos(a),.78),
        (.52*sin(a+.06),.035-.47*cos(a+.06),.42),
        (.49*sin(a-.06),.035-.44*cos(a-.06),.13),
        (.39*sin(a),.035-.36*cos(a),-.09+.035*sin(k*2))]
    lock('ANU_HAIR_back_%02d'%k,ps,.09,.023,[hair_shadow,hair,hair_light][k%3])

# Real separate butterfly clip geometry, on the approved anatomical left side.
center=Vector((.45,-.41,.86));normal=Vector((.45,-.89,.10)).normalized()
u=Vector((.89,.45,0)).normalized();v=normal.cross(u).normalized()
def butterfly_wing(name,outline):
    verts=[center+u*x+v*z for x,z in outline]
    o=mesh_obj(name,verts,[tuple(range(len(verts)))],clip)
    so=o.modifiers.new('Clip thickness','SOLIDIFY');so.thickness=.012
    be=o.modifiers.new('Soft molded edge','BEVEL');be.width=.008;be.segments=4
    return o
wing=[(0,0),(-.025,.055),(-.060,.09),(-.085,.08),(-.095,.055),(-.075,.020),(-.038,0),(-.060,-.030),(-.052,-.060),(-.030,-.062),(-.013,-.04)]
butterfly_wing('ANU_CLIP_left_wing',wing)
butterfly_wing('ANU_CLIP_right_wing',[(-x,z) for x,z in reversed(wing)])
curve('ANU_CLIP_body',[center+v*z+normal*.009 for z in [-.045,0,.06]],.012,clip)

# Keep source pixels available inside the editable .blend.
img=bpy.data.images.load(str(reference),check_existing=False);img.name='ANU_APPROVED_SHEET_v002';img.use_fake_user=True;img.pack()
img.filepath='//reference/anu_approved_sheet_v002.png'
notes=bpy.data.texts.new('ANU_STUDY_README')
notes.write('Approved source: v0.2 sheet, SHA-256 recorded on scene.\nThis is a local 3D head likeness study, not an exact-match claim or final animation asset.\nHead and orbital forms are one sculpt-stage mesh, with Boolean-cut eye openings. Older orbital reference surfaces are hidden.\nThe cut edge loops and lip surfaces need production retopology before facial rigging; no animation controls, mouth cavity or teeth are supplied.\nPhysical scale and unseen forms are interpretation. Compare face proportions and hair silhouette before approving.\nNo paid external 3D generation succeeded.\n')

def area(name,loc,energy,size,color):
    d=bpy.data.lights.new(name,'AREA');d.energy=energy;d.shape='DISK';d.size=size;d.color=color
    o=bpy.data.objects.new(name,d);scene.collection.objects.link(o);o.location=loc
    o.rotation_euler=(Vector((0,0,.5))-o.location).to_track_quat('-Z','Y').to_euler()
area('Portrait soft key',(-1.8,-2.8,2.7),240,1.8,(1,.95,.90))
area('Portrait fill',(2.0,-1.7,1.4),110,2.3,(.84,.91,1))
area('Hair edge',(.5,1.8,2.3),80,2,(1,.88,.75))
world=bpy.data.worlds.new('Anu neutral studio') if not scene.world else scene.world
scene.world=world;world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.19,.17,.145,1);world.node_tree.nodes['Background'].inputs[1].default_value=.6
bg,_=material('Portrait backdrop',(.18,.16,.135),.9)
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,2,-.62));o=bpy.context.object;o.name='Studio ground';o.data.materials.append(bg)

def camera(name,loc,target,scale):
    d=bpy.data.cameras.new(name);o=bpy.data.objects.new(name,d);scene.collection.objects.link(o)
    o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
    d.type='ORTHO';d.ortho_scale=scale;return o
front=camera('ANU_FRONT_REVIEW',(0,-4,.5),(0,0,.39),1.92)
hero=camera('ANU_THREEQUARTER_REVIEW',(1.25,-4,1.0),(0,0,.39),1.95)
profile=camera('ANU_LEFT_PROFILE_REVIEW',(4,-.05,.6),(0,0,.4),1.92)
scene.camera=hero
scene.render.engine='BLENDER_EEVEE'
scene.render.resolution_x=960;scene.render.resolution_y=1200;scene.render.resolution_percentage=60
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA'
scene.view_settings.view_transform='AgX';scene.view_settings.look='AgX - Medium High Contrast'
scene.render.film_transparent=False
# Keep the construction display and review file usable when opened interactively.
for obj in list(scene.objects):
    if obj.name.startswith(('ANU_EYE_','ANU_ORBIT_LIDS_')) and obj.type=='MESH':obj.hide_set(True)
root=bpy.data.collections.new('CH_ANU_HEAD_STUDY');scene.collection.children.link(root)
groups={}
for name in ['HEAD_FACE','EYES_LIDS','HAIR_MASSES','HAIR_STRAND_DETAILS','BUTTERFLY_CLIP','BUST_WARDROBE','REVIEW_STAGE']:
    group=bpy.data.collections.new(name);root.children.link(group);groups[name]=group
for obj in list(scene.objects):
    name=obj.name
    key='REVIEW_STAGE'
    if name.startswith('ANU_HAIR_'):key='HAIR_MASSES' if obj.type=='MESH' else 'HAIR_STRAND_DETAILS'
    elif name.startswith('ANU_CLIP_'):key='BUTTERFLY_CLIP'
    elif name.startswith(('ANU_EYE_','ANU_SCLERA_','ANU_ORBIT_','ANU_IRIS_','ANU_PUPIL_','ANU_UPPER_LID_','ANU_LOWER_LID_')):key='EYES_LIDS'
    elif name.startswith(('ANU_DRESS_','ANU_NECK')):key='BUST_WARDROBE'
    elif name.startswith(('ANU_HEAD_','ANU_BROW_','ANU_EAR_','ANU_LIP_','ANU_MOUTH_','ANU_NOSTRIL_')):key='HEAD_FACE'
    for col in list(obj.users_collection):col.objects.unlink(obj)
    groups[key].objects.link(obj)
bpy.ops.object.select_all(action='DESELECT');head.select_set(True);bpy.context.view_layer.objects.active=head
for obj in scene.objects:
    if obj.name.startswith('ANU_EYE_') and obj.type=='MESH':obj.hide_set(True)
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type=='VIEW_3D':
            space=area.spaces.active;space.shading.type='SOLID';space.shading.color_type='MATERIAL'
            space.region_3d.view_distance=2.4;space.region_3d.view_location=(0,0,.4)
            space.region_3d.view_rotation=hero.rotation_euler.to_quaternion();space.region_3d.view_perspective='ORTHO'
if '--build-only' in args:
    scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=128
    scene.cycles.use_adaptive_sampling=True;scene.cycles.adaptive_threshold=.015;scene.cycles.use_denoising=True
    scene.render.resolution_percentage=100
scene.render.filepath='//renders/anu_head_review'
bpy.ops.wm.save_as_mainfile(filepath=str(out/'anu_head_likeness_study_v007.blend'),compress=True)
timings=[]
for cam,name in ([] if '--build-only' in args else [(hero,'head_threequarter_preview'),(front,'head_front_preview')]):
    scene.camera=cam;scene.render.filepath=str(out/(name+'.png'))
    t=time.perf_counter();bpy.ops.render.render(write_still=True);timings.append({'view':name,'seconds':time.perf_counter()-t})
report={'status':'WIP_LIKENESS_STUDY_NOT_APPROVED','blender':bpy.app.version_string,'mesh_objects':sum(o.type=='MESH' for o in scene.objects),
        'hair_mesh_locks':sum(o.name.startswith('ANU_HAIR_') and o.type=='MESH' and o.name!='ANU_HAIR_main_mass' for o in scene.objects),
        'hair_detail_curves':sum(o.name.startswith('ANU_HAIR_') and o.type=='CURVE' for o in scene.objects),'rig_present':False,'timings':timings,
        'known_limits':['No accepted likeness check yet','Boolean-cut orbital loops and lip surfaces require production retopology','No facial rig, teeth or mouth cavity','Bust only; no full body','Not a finished film render']}
(out/'study_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('ANU_HEAD_STUDY '+json.dumps(report),flush=True)
