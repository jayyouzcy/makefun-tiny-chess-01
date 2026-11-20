import json,os,sys,urllib.request
from random import Random
E=os.environ.get("MAKEFUN_ENV_URL") or sys.exit("MAKEFUN_ENV_URL is not set")
V=(0,100,320,330,500,900,20000)
NS=(-33,-31,-18,-14,14,18,31,33);KS=(-17,-16,-15,-1,1,15,16,17)
BD=(-17,-15,15,17);RD=(-16,-1,1,16)
R=Random(20261118)
Z=[R.getrandbits(64) for _ in range(13*128)]
ZS=R.getrandbits(64);ZC=[R.getrandbits(64) for _ in range(16)];ZE=[R.getrandbits(64) for _ in range(8)]
INF=10**9;MATE=100000
b=[0]*128;side=1;cast=0;ep=-1;h=0;ksq={1:4,-1:116}
N=0;LIM=120000;TT={};KIL=[[0,0] for _ in range(64)];HIST={};PATH=[];H=[0]*32768
class Ab(Exception):pass
def post(p,d):
 r=urllib.request.Request(E+p,data=json.dumps(d).encode(),headers={"content-type":"application/json"})
 try:
  with urllib.request.urlopen(r) as s:return json.load(s)
 except Exception as e:sys.exit(p+" "+str(e))
def sqn(a):return (int(a[1])-1)*16+ord(a[0])-97
def uci(m):
 f=m&127;t=(m>>7)&127;pr=(m>>14)&7
 s=chr((f&7)+97)+str((f>>4)+1)+chr((t&7)+97)+str((t>>4)+1)
 return s+("nbrq"[pr-2] if pr else "")
def parse(fen):
 global b,side,cast,ep,h,ksq
 f=fen.split();b=[0]*128;h=0;r=7;c=0
 for ch in f[0]:
  if ch=='/':r-=1;c=0
  elif ch.isdigit():c+=int(ch)
  else:
   p="PNBRQK".index(ch.upper())+1
   if ch.islower():p=-p
   q=r*16+c;b[q]=p;h^=Z[(p+6)*128+q];c+=1
 side=1 if f[1]=='w' else -1
 cast=0
 if 'K' in f[2]:cast|=1
 if 'Q' in f[2]:cast|=2
 if 'k' in f[2]:cast|=4
 if 'q' in f[2]:cast|=8
 h^=ZC[cast]
 ep=-1 if f[3]=='-' else sqn(f[3])
 if ep>=0:h^=ZE[ep&7]
 if side<0:h^=ZS
 ksq={1:0,-1:0}
 for i,p in enumerate(b):
  if p==6:ksq[1]=i
  elif p==-6:ksq[-1]=i
def atk(s,q):
 if q==1:
  for d in (-15,-17):
   t=s+d
   if not t&0x88 and b[t]==1:return 1
 else:
  for d in (15,17):
   t=s+d
   if not t&0x88 and b[t]==-1:return 1
 for d in NS:
  t=s+d
  if not t&0x88 and b[t]==2*q:return 1
 for d in KS:
  t=s+d
  if not t&0x88 and b[t]==6*q:return 1
 for d in BD:
  t=s+d
  while not t&0x88:
   p=b[t]
   if p:
    if p==3*q or p==5*q:return 1
    break
   t+=d
 for d in RD:
  t=s+d
  while not t&0x88:
   p=b[t]
   if p:
    if p==4*q or p==5*q:return 1
    break
   t+=d
 return 0
def gen(caponly):
 ms=[];s=side
 for i,p in enumerate(b):
  if p*s<=0 or i&0x88:continue
  a=p if p>0 else -p
  if a==1:
   d=16*s;f=i+d
   if not caponly and not f&0x88 and not b[f]:
    r=f>>4
    if r==0 or r==7:
     for pr in (5,4,3,2):ms.append(i|f<<7|pr<<14)
    else:
     ms.append(i|f<<7)
     if (i>>4)==(1 if s==1 else 6):
      g=i+2*d
      if not b[g]:ms.append(i|g<<7)
   elif caponly and not f&0x88 and not b[f] and (f>>4 in (0,7)):
    for pr in (5,4,3,2):ms.append(i|f<<7|pr<<14)
   for dd in (d-1,d+1):
    t=i+dd
    if t&0x88:continue
    q=b[t]
    if q and q*s<0:
     r=t>>4
     if r==0 or r==7:
      for pr in (5,4,3,2):ms.append(i|t<<7|pr<<14)
     else:ms.append(i|t<<7)
    elif t==ep and q==0:
     ms.append(i|t<<7)
  elif a==2 or a==6:
   for d in NS if a==2 else KS:
    t=i+d
    if t&0x88:continue
    q=b[t]
    if (not q and not caponly) or (q and q*s<0):ms.append(i|t<<7)
  else:
   for d in BD if a==3 else RD if a==4 else BD+RD:
    t=i+d
    while not t&0x88:
     q=b[t]
     if not q:
      if not caponly:ms.append(i|t<<7)
     else:
      if q*s<0:ms.append(i|t<<7)
      break
     t+=d
 if not caponly:
  if s==1:
   if cast&1 and not b[5] and not b[6] and b[7]==4 and not atk(4,-1) and not atk(5,-1) and not atk(6,-1):ms.append(4|6<<7)
   if cast&2 and not b[3] and not b[2] and not b[1] and b[0]==4 and not atk(4,-1) and not atk(3,-1) and not atk(2,-1):ms.append(4|2<<7)
  else:
   if cast&4 and not b[117] and not b[118] and b[119]==-4 and not atk(116,1) and not atk(117,1) and not atk(118,1):ms.append(116|118<<7)
   if cast&8 and not b[115] and not b[114] and not b[113] and b[112]==-4 and not atk(116,1) and not atk(115,1) and not atk(114,1):ms.append(116|114<<7)
 return ms
def make(m):
 global side,cast,ep,h
 f=m&127;t=(m>>7)&127;pr=(m>>14)&7;p=b[f];cap=b[t];oc=cast;oe=ep;oh=h
 h^=Z[(p+6)*128+f]
 if cap:h^=Z[(cap+6)*128+t]
 epc=-1;rf=-1;rt=-1
 if abs(p)==1 and t==ep and not cap:
  epc=t-16*side;cap=b[epc];b[epc]=0;h^=Z[(cap+6)*128+epc]
 b[f]=0;b[t]=pr*side if pr else p
 h^=Z[(b[t]+6)*128+t]
 if abs(p)==6:
  ksq[side]=t
  if t==f+2:rf,rt=f+3,f+1
  elif t==f-2:rf,rt=f-4,f-1
  if rf>=0:
   rp=b[rf];b[rf]=0;b[rt]=rp;h^=Z[(rp+6)*128+rf]^Z[(rp+6)*128+rt]
 h^=ZC[cast]
 if p==6:cast&=~3
 elif p==-6:cast&=~12
 elif f==7 or t==7:cast&=~1
 elif f==0 or t==0:cast&=~2
 elif f==119 or t==119:cast&=~4
 elif f==112 or t==112:cast&=~8
 h^=ZC[cast]
 if oe>=0:h^=ZE[oe&7]
 ep=-1
 if abs(p)==1 and t==f+32*side and ((t-1>=0 and b[t-1]==-side) or (t+1<128 and b[t+1]==-side)):
  ep=f+16*side;h^=ZE[ep&7]
 side=-side;h^=ZS
 return (m,cap,oc,oe,oh,epc,rf,rt)
def unmake(u):
 global side,cast,ep,h
 m,cap,oc,oe,oh,epc,rf,rt=u
 f=m&127;t=(m>>7)&127;pr=(m>>14)&7
 side=-side
 p=b[t]
 b[t]=0 if epc>=0 else cap
 b[f]=(side*1) if pr else p
 if epc>=0:b[epc]=-side
 if rf>=0:
  rp=b[rt];b[rt]=0;b[rf]=rp
 if abs(p)==6:ksq[side]=f
 cast=oc;ep=oe;h=oh
def ev():
 s=0;mat=0;wb=0;bb=0;wq=0;bq=0;wkc=0;bkc=0;wps=[];bps=[];wks=0;bks=0;wrs=[];brs=[]
 for i,p in enumerate(b):
  if not p or i&0x88:continue
  a=p if p>0 else -p;r=i>>4;f=i&7
  cen=(3-abs(f-3))+(3-abs(r-3));v=V[a]
  if a==1:
   v+=(r*7 if p>0 else (7-r)*7)+(2 if 2<=f<=5 else 0);(wps if p>0 else bps).append(i)
  elif a==2:v+=cen*9;mat+=320
  elif a==3:
   v+=cen*6;mat+=330
   if p>0:wb+=1
   else:bb+=1
  elif a==4:v+=cen*2;mat+=500;(wrs if p>0 else brs).append(i)
  elif a==5:
   v+=cen*2;mat+=900
   if p>0:wq+=1
   else:bq+=1
  elif a==6:
   if p>0:wkc=cen;wks=i
   else:bkc=cen;bks=i
   continue
  s+=v if p>0 else -v
 if wb>=2:s+=30
 if bb>=2:s-=30
 for i in wps:
  if all(abs((j&7)-(i&7))>1 or (j>>4)<=(i>>4) for j in bps):s+=(i>>4)*12
 for j in bps:
  if all(abs((i&7)-(j&7))>1 or (i>>4)>=(j>>4) for i in wps):s-=(7-(j>>4))*12
 wf=0
 for i in wps:wf|=1<<(i&7)
 bf=0
 for j in bps:bf|=1<<(j&7)
 for i in wrs:
  if not (wf>>(i&7))&1:s+=12
  if not (bf>>(i&7))&1:s+=6
  if (i>>4)==6:s+=20
 for j in brs:
  if not (bf>>(j&7))&1:s-=12
  if not (wf>>(j&7))&1:s-=6
  if (j>>4)==1:s-=20
 s+=12*sum(1 for p in wps if abs((p&7)-(wks&7))<=1 and (p>>4)==(wks>>4)+1)
 s-=12*sum(1 for p in bps if abs((p&7)-(bks&7))<=1 and (p>>4)==(bks>>4)-1)
 eg=1 if mat<=1400 else 0
 s+=(wkc-bkc)*(10 if eg else -5)
 return s
def order(ms,ttm,pl):
 def sc(m):
  if m==ttm:return 1<<20
  t=(m>>7)&127;cap=b[t]
  if cap or ((m>>14)&7):return 9000+10*V[abs(cap)]-V[abs(b[m&127])]//32
  if m==KIL[pl][0] or m==KIL[pl][1]:return 8000
  return min(H[(0 if side>0 else 16384)+(m&127)*128+t]//16,7000)
 return sorted(ms,key=sc,reverse=True)
def qs(a,bb,pl,chk):
 global N
 N+=1
 if N>LIM:raise Ab
 st=side*ev()
 if st>=bb:return bb
 if st>a:a=st
 ms=gen(0) if chk else gen(1)
 ms=order(ms,0,pl)
 legal=0
 for m in ms:
  u=make(m)
  if atk(ksq[-side],side):unmake(u);continue
  legal+=1
  s=-qs(-bb,-a,pl+1,atk(ksq[side],-side))
  unmake(u)
  if s>=bb:return bb
  if s>a:a=s
 if chk and not legal:return -MATE+pl
 return a
def sr(d,a,bb,pl,nm=1):
 global N,side,ep,h
 N+=1
 if N>LIM:raise Ab
 if pl>60:return side*ev()
 if h in PATH or HIST.get(h,0)>=2:return 0
 kc=ksq[side];chk=atk(kc,-side)
 if d<=0:return qs(a,bb,pl,chk)
 if chk:d+=1
 elif nm and d>=3 and side*ev()>=bb and any(p*side in (2,3,4,5) for p in b):
  oe=ep;oh=h
  if ep>=0:h^=ZE[ep&7]
  ep=-1;side=-side;h^=ZS
  s=-sr(d-3,-bb,-bb+1,pl+1,0)
  side=-side;ep=oe;h=oh
  if s>=bb:return bb
 e=TT.get(h)
 ttm=0
 if e and e[0]>=d:
  if e[2]==0:return e[1]
  if e[2]==1 and e[1]>a:a=e[1]
  elif e[2]==2 and e[1]<bb:bb=e[1]
  if a>=bb:return e[1]
  ttm=e[3]
 ms=order(gen(0),ttm,pl);ao=a
 best=-INF;bm=0;legal=0
 for m in ms:
  u=make(m)
  if atk(ksq[-side],side):unmake(u);continue
  legal+=1
  PATH.append(u[4])
  s=-sr(d-1,-bb,-a,pl+1)
  PATH.pop()
  unmake(u)
  if s>best:best=s;bm=m
  if s>a:a=s
  if a>=bb:
   if not b[(m>>7)&127] and not (m>>14)&7:
    KIL[pl][1]=KIL[pl][0];KIL[pl][0]=m
    H[(0 if side>0 else 16384)+(m&127)*128+((m>>7)&127)]+=d*d
   break
 if not legal:return -MATE+pl if chk else 0
 fl=0 if best<=a else 1 if best>=bb else 0
 TT[h]=(d,best,1 if best>=bb else 2 if best<=ao else 0,bm)
 return best
def choose(legal_uci):
 global N,PATH
 ms=gen(0);legal=[]
 for m in ms:
  u=make(m)
  if atk(ksq[-side],side):unmake(u);continue
  legal.append(m);unmake(u)
 if not legal:return legal_uci[0]
 if len(legal)==1:return uci(legal[0])
 sc={m:0 for m in legal};best=legal[0]
 N=0
 for d in range(1,11):
  PATH=[]
  try:
   a=-INF;bd=best
   for m in sorted(legal,key=lambda m:-sc[m]):
    u=make(m);PATH.append(u[4])
    s=-sr(d-1,-INF,INF,1)
    PATH.pop();unmake(u)
    sc[m]=s
    if s>a:a=s;bd=m
   best=bd
  except Ab:break
  except RecursionError:break
 # avoid repeating a game position (draw) while ahead
 bs=sc[best]
 for m in legal:
  u=make(m);rep=HIST.get(h,0)>=2;unmake(u)
  if rep and sc[m]>bs:bs=0;best=m
  elif rep and bs>0 and sc[m]==bs:pass
 adj={}
 for m in legal:
  u=make(m);rep=HIST.get(h,0)>=2;unmake(u)
  adj[m]=0 if rep else sc[m]
 best=max(legal,key=lambda m:(adj[m],sc[m]))
 u=uci(best)
 return u if u in legal_uci else legal_uci[0]
while True:
 g=post("/game",{})
 if g["status"]=="done":break
 cur=g["game"];HIST={}
 while g["status"]=="your_move":
  if g["game"]!=cur:cur=g["game"];HIST={}
  parse(g["fen"]);HIST[h]=HIST.get(h,0)+1
  mv=choose(g["legal_moves"])
  g=post("/move",{"game":g["game"],"move":mv})
 print("game "+str(g["game"])+": "+str(g.get("outcome"))+" by "+str(g.get("reason")),file=sys.stderr)
print("done: "+str(g.get("wins"))+" won, "+str(g.get("draws"))+" drawn, "+str(g.get("losses"))+" lost",file=sys.stderr)
