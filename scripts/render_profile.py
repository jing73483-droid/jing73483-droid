"""Deterministic profile artwork. Python 3 + Pillow; no network or live metrics."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import math, random
ROOT=Path(__file__).resolve().parents[1]
W,H=960,1180
TOP,BOTTOM=40,920
CX,CY=-650,480
RI,RO=1015,1215
PINK='#ec62cf'; CYAN='#80e8ee'; DIM='#79617f'; WHITE='#ebd9eb'
FONT='/System/Library/Fonts/Menlo.ttc'
fonts={s:ImageFont.truetype(FONT,s) for s in (7,8,9,10,11,12,14,16,20,24)}
rng=random.Random(73483)
def txt(d,xy,s,c=DIM,size=10):d.text(xy,s,font=fonts[size],fill=c)
def pt(r,a):return (CX+r*math.cos(a),CY+r*math.sin(a))
def line(d,p,c,w=1):d.line(p,fill=c,width=w)
def dot(d,x,y,r,c):d.ellipse((x-r,y-r,x+r,y+r),fill=c)
def arc(d,r,c,w=1):d.arc((CX-r,CY-r,CX+r,CY+r),-32,32,fill=c,width=w)
base=Image.new('RGB',(W,H),'#110b18');d=ImageDraw.Draw(base)
for y in range(TOP,BOTTOM):
 shade=int(5*(1-abs(y-480)/480));line(d,[(0,y),(W,y)],(23+shade,12,30+shade))
# A fine, irregular web fills the clipped inner disc.
web=Image.new('RGB',(W,H),'#160d20');wd=ImageDraw.Draw(web)
nodes=[(rng.uniform(-130,390),rng.uniform(80,950)) for _ in range(260)]
for i,p in enumerate(nodes):
 for q in rng.sample(nodes,3):
  dist=math.dist(p,q)
  if dist<420:line(wd,[p,q],rng.choice(['#23172d','#2b1c34','#20152a','#302039']))
 dot(wd,*p,1,'#48304f')
mask=Image.new('L',(W,H));md=ImageDraw.Draw(mask);md.ellipse((CX-RI,CY-RI,CX+RI,CY+RI),fill=255)
base.paste(web,(0,0),mask);d=ImageDraw.Draw(base)
# Dark curved ledger, two concentric boundaries and fine scale marks.
d.ellipse((CX-RO,CY-RO,CX+RO,CY+RO),outline='#443047',width=2)
for r,c in [(RI,'#a74388'),(RI+4,'#51243f'),(RO-23,'#3a293c'),(RO-6,'#4e3352')]:arc(d,r,c)
for i in range(430):
 a=-.47+i*.0022
 line(d,[pt(RO-19,a),pt(RO-(29 if i%5==0 else 24),a)],'#634b66')
labels=['user research','agent workflows','product strategy','AIPM workbench','market signals','prototype lab','design systems','BRD / MRD / PRD','emotion companion','voice pipeline','model evaluation','content automation','product discovery','human feedback','MVP experiments','prompt engineering','interface craft','AI applications','interaction design','roadmap planning','creative tools','knowledge systems','user interviews','workflow design','writing / sharing','build & iterate','multimodal AI','product validation','independent projects','from idea to product','research notes','experience design','agent orchestration','design handoff','systems thinking','small experiments','product practice']
for i,label in enumerate(labels):
 a=-.433+i*.024
 x,y=pt(RI+16,a)
 tile=Image.new('RGBA',(186,20));td=ImageDraw.Draw(tile)
 txt(td,(0,3),label,WHITE if i%4 else '#ad7b9b',9)
 txt(td,(151,3),'keep' if i%3 else 'run', '#bb688e',8)
 tile=tile.rotate(-a*180/math.pi,resample=Image.Resampling.BICUBIC,expand=True)
 base.paste(tile,(int(x),int(y-9)),tile)
# Header and top-left caption.
d=ImageDraw.Draw(base);d.rectangle((0,0,W,TOP),fill='#0c0911');line(d,[(0,39),(W,39)],'#713051')
txt(d,(12,13),'SHIRLEY  ->  AI PRODUCTS',WHITE,12)
for x,t,v,c in [(290,'FOCUS','AI / PM',WHITE),(435,'PROJECTS','04',PINK),(550,'WORKFLOW','08 STAGES',PINK),(705,'MODE','EXPLORING','#e7cf79')]:
 txt(d,(x,5),t,DIM,7);txt(d,(x,20),v,c,10)
d.rectangle((852,10,946,30),fill='#bd409b');txt(d,(866,15),'BUILD / LEARN','#160b1b',8)
d.rectangle((0,46,245,140),fill='#160d20')
txt(d,(12,57),'01  EXPLORING',WHITE,14)
txt(d,(12,85),'Ideas into useful products.',WHITE,12)
txt(d,(12,110),'research / design / build', '#b28da9',9)
txt(d,(12,127),'AI PRODUCT DESIGN & PRACTICE', '#c15a9f',8)
# Bottom terminal dashboard, echoing the six narrow columns in the reference.
d.rectangle((0,BOTTOM,W,H),fill='#0c0912');line(d,[(0,BOTTOM),(W,BOTTOM)],'#58304e')
for i,c in enumerate([PINK,'#e7cd75','#70d7b1']):dot(d,12+11*i,BOTTOM+12,3,c)
txt(d,(55,BOTTOM+7),'Shirley  -  product exploration console',WHITE,8)
txt(d,(652,BOTTOM+7),'state: exploring','#e2ca78',9)
cols=['research','workflow','projects','build log','agent lab','notes']
for n,title in enumerate(cols):
 x=n*160;d.rectangle((x+3,944,x+157,1166),outline='#392338')
 dot(d,x+14,956,2,[CYAN,PINK,'#aa86ed','#e6cd7c',CYAN,PINK][n]);txt(d,(x+23,951),title,WHITE,10)
if True:
 for i,(label,l) in enumerate([('insights',72),('needs',43),('market',29),('users',22),('tests',16),('signals',12)]):
  y=980+i*16;txt(d,(12,y),label,DIM,8);d.rectangle((72,y+2,72+l,y+6),fill=CYAN if i%2==0 else PINK)
 txt(d,(12,1090),'DISCOVER',DIM,8);txt(d,(12,1105),'HUMAN',PINK,24)
 for i in range(28):
  x=14+i%14*9;y=1144+i//14*9;d.rectangle((x,y,x+6,y+6),fill=rng.choice([PINK,CYAN,'#573563']))
 for i in range(8):
  for j in range(max(1,6-i)):
   x=174+i*13;y=1067-j*9;d.rectangle((x,y,x+8,y+5),fill=PINK)
 txt(d,(173,1090),'FROM DISCOVERY TO DELIVERY',DIM,7);txt(d,(173,1110),'08',PINK,24);txt(d,(220,1120),'/ stages',WHITE,10)
 for i in range(4):
  y=984+i*37;txt(d,(333,y),'0'+str(i+1),PINK,11);txt(d,(359,y),['AIPM workspace','Emotion companion','Audio pipeline','Content tools'][i],WHITE,8)
 txt(d,(333,1146),'DOCUMENT / PROTOTYPE / TEST',DIM,7)
 for i,t in enumerate(['> understand the need','  research.collect()','> define the problem','  product.plan()','> make it tangible','  prototype.build()','> learn from feedback','  iterate(next_step)','', '  ideas -> experiences']):
  txt(d,(492,981+i*17),t, PINK if i%2==0 else CYAN,8)
 txt(d,(654,984),'WORKFLOWS',DIM,8);txt(d,(654,1005),'AI + PM',CYAN,20)
 for i,t in enumerate(['context + reasoning','tools + orchestration','human in the loop']):txt(d,(654,1067+i*20),t,DIM,8)
 txt(d,(654,1146),'BUILD WITH INTENTION',WHITE,8)
 txt(d,(814,984),'CURRENT DIRECTION',DIM,8);txt(d,(814,1008),'CREATE', '#e8ce79',24)
 for i,t in enumerate(['AI product design','Applied exploration','Writing & sharing']):txt(d,(814,1067+i*20),t,WHITE,8)
 txt(d,(814,1146),'jing73483-droid',PINK,9)
txt(d,(12,1170),'PERSONAL PORTFOLIO / GENERATIVE VISUAL / NOT LIVE TELEMETRY',DIM,7)
# Ray lengths remain deterministic; only the scanning highlight changes.
rays=[]
for i in range(390):
 a=-.48+i*.0025
 length=rng.uniform(110,410)*(0.82+0.18*math.sin(i*.041))
 rays.append((a,length,rng.choice(['#92519a','#c34fa8','#dc58bc','#8e61bb','#713c7e'])))

def render(frame,total=100):
 t=frame/total*math.tau
 im=base.copy();d=ImageDraw.Draw(im)
 scan=.35*math.sin(t)
 for i,(a,length,col) in enumerate(rays):
  if abs(a-scan)<.055:col='#eb69cd'
  elif a>scan+.18:col='#58405e'
  line(d,[pt(RO+3,a),pt(RO+length,a)],col,3 if i%3 else 2)
  if i%19==0:dot(d,*pt(RO+length,a),1,'#ed94d6')
 # A pair of golden discovery bands occasionally pulses through the pink rays.
 strength=max(0,math.sin(t-1))
 if strength>.3:
  for a in [-.29,.15,.28]:
   for j in range(9):line(d,[pt(RO+3,a+j*.0013),pt(RO+250+35*math.sin(j),a+j*.0013)],'#c4a45f')
 # Delicate moving breadcrumb chain in the left web.
 for j in range(18):
  x=24+j*17;y=235+j*6+14*math.sin(j*.55+t)
  d.ellipse((x-5,y-5,x+5,y+5),outline='#74597f');dot(d,x,y,1,'#c99bc5')
 # Spider: eight three-segment articulated legs, luminous joints, narrow abdomen.
 a=scan; sx,sy=pt(RI+91,a)
 layer=Image.new('RGBA',(W,H));ld=ImageDraw.Draw(layer)
 def sp(x,y):
  # Body points along the curved climbing path.
  return (sx+x*math.cos(a)-y*math.sin(a),sy+x*math.sin(a)+y*math.cos(a))
 for side in [-1,1]:
  for j in range(4):
   gait=math.sin(t*10+j*1.8+(math.pi if side<0 else 0))
   root=sp(side*4,-15+j*8)
   knee=sp(side*(21+5*math.sin(j)), -37+j*21+gait*4)
   ankle=sp(side*(39+(2-j)*3),-49+j*31+gait*7)
   toe=sp(side*(45+(1-j)*6),-65+j*41+gait*8)
   ld.line([root,knee,ankle,toe],fill='#e36abf',width=2)
   for p in [knee,ankle]:dot(ld,*p,2,'#f5b6e7')
   dot(ld,*toe,1,CYAN)
 # Ovoid, tapered spider body built in its local coordinates.
 ld.polygon([sp(-6,-18),sp(5,-18),sp(9,-3),sp(5,21),sp(0,28),sp(-6,18),sp(-9,-2)],fill='#bc428e',outline='#f38ed8')
 ld.line([sp(0,-16),sp(1,22)],fill='#ffe4fb',width=3)
 dot(ld,*sp(0,-22),5,'#e16cbb');dot(ld,*sp(-3,-24),1,'#fff0f9');dot(ld,*sp(3,-24),1,'#fff0f9')
 glow=layer.filter(ImageFilter.GaussianBlur(9));im=Image.alpha_composite(im.convert('RGBA'),glow);im=Image.alpha_composite(im,layer)
 d=ImageDraw.Draw(im);txt(d,(int(sx)-139,int(sy)-6),'3x crawler', '#b787ad',8)
 # Animated locator on inner arc.
 for j in range(9):line(d,[pt(RI-2,a-.008+j*.0015),pt(RI+3,a-.008+j*.0015)],'#ffe6f8',2)
 # Cyan terminal scanner at lower right.
 x,y=882,856
 for r in [18,23,29]:d.ellipse((x-r,y-r,x+r,y+r),outline='#37616c')
 d.arc((x-26,y-26,x+26,y+26),frame*9,frame*9+115,fill=CYAN,width=2)
 dot(d,x,y,3,CYAN);txt(d,(839,895),'SCANNING',CYAN,8)
 # Clip artwork to main viewport so rays do not cover the header/footer.
 im.paste(base.crop((0,0,W,TOP)),(0,0));im.paste(base.crop((0,BOTTOM,W,H)),(0,BOTTOM))
 return im.convert('RGB')
if __name__=='__main__':
 frames=[render(i) for i in range(100)]
 frames[10].save(ROOT/'assets/spider-preview.png')
 # A shared palette prevents color flicker between frames.
 palette=frames[10].quantize(colors=128)
 frames=[f.quantize(palette=palette,dither=Image.Dither.NONE) for f in frames]
 frames[0].save(ROOT/'assets/spider-profile.gif',save_all=True,append_images=frames[1:],duration=80,loop=0,optimize=True,disposal=1)
 print(ROOT/'assets/spider-profile.gif')
 print('bytes:',(ROOT/'assets/spider-profile.gif').stat().st_size)
