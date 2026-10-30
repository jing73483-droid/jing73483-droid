"""Render a 1920x920 profile banner from vector geometry and 2x type.
Pillow required. Eight-second loop, original ten gait cycles per loop.
Dashboard describes portfolio projects; bars are decorative, not live metrics.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import math,random
ROOT=Path(__file__).resolve().parents[1]
S=2; W,H=960,460; TOP,BOTTOM=32,300
PINK='#ec62cf'; CYAN='#80e8ee'; DIM='#a188a9'; WHITE='#ebd9eb'
FONT='/System/Library/Fonts/Menlo.ttc'
fonts={s:ImageFont.truetype(FONT,s*S) for s in range(6,25)}
def coords(v):
 return [coords(a) if isinstance(a,(list,tuple)) else a*S for a in v]
class Draw:
 def __init__(self,im):self.d=ImageDraw.Draw(im)
 def line(self,p,c,w=1):self.d.line(coords(p),fill=c,width=max(1,round(w*S)))
 def rect(self,b,c=None,o=None,w=1):self.d.rectangle(coords(b),fill=c,outline=o,width=max(1,round(w*S)))
 def ellipse(self,b,c=None,o=None,w=1):self.d.ellipse(coords(b),fill=c,outline=o,width=max(1,round(w*S)))
 def text(self,p,t,c=DIM,s=8):self.d.text(coords(p),t,font=fonts[s],fill=c)
 def dot(self,p,r,c):self.ellipse((p[0]-r,p[1]-r,p[0]+r,p[1]+r),c)
 def poly(self,p,c,o=None):self.d.polygon(coords(p),fill=c,outline=o)
def new(mode='RGB',c='#140c1c'):return Image.new(mode,(W*S,H*S),c)
# Elliptical radii preserve the curved ledger while fitting the complete dashboard.
CX,CY=-190,164
def pt(r,a):return (CX+r*math.cos(a),CY+r*.40*math.sin(a))
RI,RO=580,740
rng=random.Random(73483)
base=new();d=Draw(base)
nodes=[(rng.uniform(-80,400),rng.uniform(35,305)) for _ in range(190)]
for p in nodes:
 for q in rng.sample(nodes,3):
  if math.dist(p,q)<240:d.line([p,q],rng.choice(['#291c33','#30203b','#23192e']),.45)
 d.dot(p,.6,'#48304f')
# Solid ring masks the irregular network.
outer=[pt(RO,-1+i*.002) for i in range(1001)]
inner=[pt(RI,1-i*.002) for i in range(1001)]
d.poly(outer+inner,'#100b17')
for r,c in [(RI,'#b24b94'),(RI+4,'#51243f'),(RO-17,'#3a293c'),(RO-4,'#604168')]:
 d.line([pt(r,-1+i*.002) for i in range(1001)],c,.6)
for i in range(230):
 a=-.65+i*.0057;d.line([pt(RO-13,a),pt(RO-(21 if i%5==0 else 17),a)],'#715778',.5)
labels=['user research','agent workflows','product strategy','AIPM workbench','market signals','prototype lab','BRD / MRD / PRD','emotion companion','audio pipeline','content automation','product discovery','human feedback','MVP experiments','prompt engineering','interface craft','AI applications','workflow design','build & iterate','product validation','design handoff','systems thinking','product practice']
for i,label in enumerate(labels):
 a=-.60+i*.057;x,y=pt(RI+12,a)
 tile=Image.new('RGBA',(150*S,16*S));td=ImageDraw.Draw(tile)
 td.text((0,2*S),label,font=fonts[7],fill=WHITE if i%4 else '#b48ba9')
 td.text((128*S,2*S),'run' if i%3==0 else 'keep',font=fonts[6],fill='#b86c96')
 tile=tile.rotate(-a*26,resample=Image.Resampling.BICUBIC,expand=True)
 base.paste(tile,(int(x*S),int((y-5)*S)),tile)
d=Draw(base)
# Compact header.
d.rect((0,0,W,TOP),'#0c0911');d.line([(0,31),(W,31)],'#713051',.7)
d.text((12,11),'SHIRLEY  ->  AI PRODUCTS',WHITE,10)
for x,t,v,c in [(289,'FOCUS','AI / PM',WHITE),(432,'PROJECTS','04',PINK),(549,'WORKFLOW','08 STAGES',PINK),(704,'MODE','EXPLORING','#e7cf79')]:
 d.text((x,3),t,DIM,6);d.text((x,16),v,c,8)
d.rect((852,8,946,25),'#bd409b');d.text((865,12),'BUILD / LEARN','#160b1b',7)
d.rect((0,38,245,104),'#160d20')
d.text((12,43),'01  EXPLORING',WHITE,11);d.text((12,63),'Ideas into useful products.',WHITE,10)
d.text((12,82),'research / design / build',DIM,7);d.text((12,96),'AI PRODUCT DESIGN & PRACTICE','#c15a9f',6)
# All six project panels, laid out afresh at readable native font sizes.
d.rect((0,BOTTOM,W,H),'#0c0912');d.line([(0,BOTTOM),(W,BOTTOM)],'#683656',.7)
for i,c in enumerate([PINK,'#e7cd75','#70d7b1']):d.dot((12+i*10,309),2.5,c)
d.text((50,305),'Shirley - product exploration console',WHITE,7)
d.text((745,305),'state: exploring','#e2ca78',7)
for n,title in enumerate(['research','workflow','projects','build log','agent lab','notes']):
 x=n*160;d.rect((x+3,319,x+157,449),o='#49304b',w=.65)
 d.dot((x+12,328),2,[CYAN,PINK,'#b49adb','#e6cd7c',CYAN,PINK][n]);d.text((x+21,323),title,WHITE,9)
for i,(label,l) in enumerate([('insights',72),('needs',43),('market',29),('users',22),('tests',16),('signals',12)]):
 y=341+i*10;d.text((12,y),label,DIM,6);d.rect((72,y+2,72+l,y+5),CYAN if i%2==0 else PINK)
d.text((12,405),'DISCOVER',DIM,6);d.text((12,416),'HUMAN',PINK,17)
for i in range(28):
 x=14+i%14*9;y=438+i//14*5;d.rect((x,y,x+6,y+3),rng.choice([PINK,CYAN,'#573563']))
for i in range(8):
 for j in range(max(1,6-i)):
  x=174+i*13;y=394-j*7;d.rect((x,y,x+8,y+4),PINK)
d.text((173,406),'FROM DISCOVERY TO DELIVERY',DIM,6);d.text((173,419),'08',PINK,20);d.text((208,429),'/ stages',WHITE,8)
for i,t in enumerate(['AIPM workspace','Emotion companion','Audio pipeline','Content tools']):
 y=345+i*22;d.text((332,y),'0'+str(i+1),PINK,8);d.text((351,y),t,WHITE,7)
d.text((332,438),'DOCUMENT / PROTOTYPE / TEST',DIM,6)
for i,t in enumerate(['> understand the need','  research.collect()','> define the problem','  product.plan()','> make it tangible','  prototype.build()','> learn from feedback','  iterate(next_step)']):d.text((491,341+i*11),t,PINK if i%2==0 else CYAN,7)
d.text((491,438),'ideas -> experiences',WHITE,6)
d.text((651,345),'WORKFLOWS',DIM,6);d.text((651,362),'AI + PM',CYAN,19)
for i,t in enumerate(['context + reasoning','tools + orchestration','human in the loop']):d.text((651,398+i*12),t,DIM,7)
d.text((651,439),'BUILD WITH INTENTION',WHITE,6)
d.text((812,345),'CURRENT DIRECTION',DIM,6);d.text((812,362),'CREATE','#e8ce79',19)
for i,t in enumerate(['AI product design','Applied exploration','Writing & sharing']):d.text((812,398+i*12),t,WHITE,7)
d.text((812,439),'jing73483-droid',PINK,7)
d.text((12,452),'PERSONAL PORTFOLIO / GENERATIVE VISUAL / NOT LIVE TELEMETRY',DIM,6)
rays=[]
for i in range(350):
 a=-.65+i*.0038;length=rng.uniform(110,410)*(.82+.18*math.sin(i*.041))
 rays.append((a,length,rng.choice(['#92519a','#c34fa8','#dc58bc','#8e61bb','#713c7e'])))
def render(frame,total=200):
 t=frame/total*math.tau;im=base.copy();d=Draw(im)
 # Restore the original angular excursion, loop duration and gait timing.
 scan=.35*math.sin(t)
 for i,(a,length,col) in enumerate(rays):
  if abs(a-scan)<.055:col='#eb69cd'
  elif a>scan+.18:col='#58405e'
  d.line([pt(RO+3,a),pt(RO+length,a)],col,.75 if i%3 else 1)
 if math.sin(t-1)>.3:
  for a in [-.29,.15,.28]:
   for j in range(5):d.line([pt(RO+3,a+j*.002),pt(RO+250+35*math.sin(j),a+j*.002)],'#c4a45f',.7)
 for j in range(18):
  x=24+j*17;y=170+j*2+5*math.sin(j*.55+t)
  d.ellipse((x-3,y-3,x+3,y+3),o='#74597f',w=.6);d.dot((x,y),.6,'#c99bc5')
 a=scan;sx,sy=pt(RI+70,a);layer=new('RGBA',(0,0,0,0));ld=Draw(layer)
 def sp(x,y):
  x*=.50;y*=.50
  return (sx+x*math.cos(a)-y*math.sin(a),sy+x*math.sin(a)+y*math.cos(a))
 for side in [-1,1]:
  for j in range(4):
   gait=math.sin(t*10+j*1.8+(math.pi if side<0 else 0))
   root=sp(side*4,-15+j*8);knee=sp(side*(21+5*math.sin(j)),-37+j*21+gait*4)
   ankle=sp(side*(39+(2-j)*3),-49+j*31+gait*7);toe=sp(side*(45+(1-j)*6),-65+j*41+gait*8)
   ld.line([root,knee,ankle,toe],'#e36abf',.85)
   for p in [knee,ankle]:ld.dot(p,1,'#f5b6e7')
   ld.dot(toe,.7,CYAN)
 ld.poly([sp(-6,-18),sp(5,-18),sp(9,-3),sp(5,21),sp(0,28),sp(-6,18),sp(-9,-2)],'#bc428e','#f38ed8')
 ld.line([sp(0,-16),sp(1,22)],'#ffe4fb',1.2);ld.dot(sp(0,-22),2.5,'#e16cbb')
 for x in [-3,3]:ld.dot(sp(x,-24),.6,'#fff0f9')
 im=Image.alpha_composite(im.convert('RGBA'),layer.filter(ImageFilter.GaussianBlur(5*S)));im=Image.alpha_composite(im,layer)
 d=Draw(im);d.text((sx-100,sy-3),'3x crawler','#b787ad',6)
 for j in range(7):d.line([pt(RI-2,a-.008+j*.002),pt(RI+3,a-.008+j*.002)],'#ffe6f8',1)
 x,y=895,262
 for r in [12,17,21]:d.ellipse((x-r,y-r,x+r,y+r),o='#37616c',w=.65)
 d.d.arc(coords((x-19,y-19,x+19,y+19)),t*180/math.pi*2.5,t*180/math.pi*2.5+115,fill=CYAN,width=2)
 d.dot((x,y),2,CYAN);d.text((870,287),'SCANNING',CYAN,6)
 im.paste(base.crop((0,0,W*S,TOP*S)),(0,0))
 im.paste(base.crop((0,BOTTOM*S,W*S,H*S)),(0,BOTTOM*S))
 return im.convert('RGB')
if __name__=='__main__':
 first=render(20);first.save(ROOT/'assets/spider-preview.png')
 palette=first.quantize(colors=256)
 frames=[]
 for i in range(200):
  frames.append(render(i).quantize(palette=palette,dither=Image.Dither.NONE))
  if i%50==0:print('frame',i,flush=True)
 path=ROOT/'assets/spider-profile-hd.gif'
 frames[0].save(path,save_all=True,append_images=frames[1:],duration=40,loop=0,optimize=True,disposal=1)
 print(path, path.stat().st_size,flush=True)
