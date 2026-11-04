import json, math, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
topo = json.loads((ROOT/'data/us-map.json').read_text())
sc = topo['transform']['scale']; tr = topo['transform']['translate']
arcs=[]
for a in topo['arcs']:
    x=y=0; out=[]
    for dx,dy in a:
        x+=dx; y+=dy; out.append((round(x*sc[0]+tr[0],2),round(y*sc[1]+tr[1],2)))
    arcs.append(out)

def ring(ids):
    out=[]
    for i in ids:
        a=arcs[i] if i>=0 else arcs[~i][::-1]
        out.extend(a if not out else a[1:])
    return out

def simplify(p, tol=.55):
    if len(p)<3: return p
    a,b=p[0],p[-1]; dx=b[0]-a[0]; dy=b[1]-a[1]; den=dx*dx+dy*dy
    ds=[]
    for x,y in p[1:-1]:
        t=max(0,min(1,((x-a[0])*dx+(y-a[1])*dy)/den)) if den else 0
        ds.append((x-a[0]-t*dx)**2+(y-a[1]-t*dy)**2)
    if not ds or max(ds)<=tol*tol: return [a,b]
    i=ds.index(max(ds))+1
    return simplify(p[:i+1],tol)[:-1]+simplify(p[i:],tol)

state_lines='''AL|亚拉巴马|Alabama
AZ|亚利桑那|Arizona
AR|阿肯色|Arkansas
CA|加利福尼亚|California
CO|科罗拉多|Colorado
CT|康涅狄格|Connecticut
DE|特拉华|Delaware
FL|佛罗里达|Florida
GA|佐治亚|Georgia
ID|爱达荷|Idaho
IL|伊利诺伊|Illinois
IN|印第安纳|Indiana
IA|艾奥瓦|Iowa
KS|堪萨斯|Kansas
KY|肯塔基|Kentucky
LA|路易斯安那|Louisiana
ME|缅因|Maine
MD|马里兰|Maryland
MA|马萨诸塞|Massachusetts
MI|密歇根|Michigan
MN|明尼苏达|Minnesota
MS|密西西比|Mississippi
MO|密苏里|Missouri
MT|蒙大拿|Montana
NE|内布拉斯加|Nebraska
NV|内华达|Nevada
NH|新罕布什尔|New Hampshire
NJ|新泽西|New Jersey
NM|新墨西哥|New Mexico
NY|纽约|New York
NC|北卡罗来纳|North Carolina
ND|北达科他|North Dakota
OH|俄亥俄|Ohio
OK|俄克拉何马|Oklahoma
OR|俄勒冈|Oregon
PA|宾夕法尼亚|Pennsylvania
RI|罗得岛|Rhode Island
SC|南卡罗来纳|South Carolina
SD|南达科他|South Dakota
TN|田纳西|Tennessee
TX|得克萨斯|Texas
UT|犹他|Utah
VT|佛蒙特|Vermont
VA|弗吉尼亚|Virginia
WA|华盛顿|Washington
WV|西弗吉尼亚|West Virginia
WI|威斯康星|Wisconsin
WY|怀俄明|Wyoming'''
lookup={en:(ab,zh) for ab,zh,en in [s.split('|') for s in state_lines.splitlines()]}
states=[]
for g in topo['objects']['states']['geometries']:
    name=g['properties']['name']
    if name not in lookup: continue
    ab,zh=lookup[name]
    polys=g['arcs'] if g['type']=='MultiPolygon' else [g['arcs']]
    rings=[simplify(ring(p[0])) for p in polys]
    def area(p):return abs(sum(x*v-u*y for (x,y),(u,v) in zip(p,p[1:]+p[:1]))/2)
    main=max(rings,key=area)
    a=sum(x*v-u*y for (x,y),(u,v) in zip(main,main[1:]+main[:1]))/2
    cx=sum((x+u)*(x*v-u*y) for (x,y),(u,v) in zip(main,main[1:]+main[:1]))/(6*a)
    cy=sum((y+v)*(x*v-u*y) for (x,y),(u,v) in zip(main,main[1:]+main[:1]))/(6*a)
    path=''.join('M'+'L'.join(f'{x},{y}' for x,y in p)+'Z' for p in rings)
    states.append(dict(id=ab,zh=zh,en=name,path=path,ring=main,center=[round(cx,1),round(cy,1)],area=round(area(main)),bounds=[min(p[0] for p in main),min(p[1] for p in main),max(p[0] for p in main),max(p[1] for p in main)]))

brands=[]
for i,line in enumerate((ROOT/'data/brands.txt').read_text().strip().splitlines()):
    name,zh,state,year,origin,cat,desc,domain=line.split('|')
    brands.append(dict(id=i,name=name,zh=zh,state=state,year=int(year),origin=origin,cat=cat,desc=desc,url='https://'+domain))

template=(ROOT/'src/template.html').read_text()
data=json.dumps(dict(brands=brands,states=states),ensure_ascii=False,separators=(',',':'))
out=template.replace('/*__DATA__*/',data)
target=ROOT/'public/index.html'
target.parent.mkdir(parents=True, exist_ok=True)
notice=(ROOT/'licenses/us-atlas-ISC.txt').read_text()
out=out.replace('<html lang="zh-CN">','<html lang="zh-CN">\n<!--\nMap geometry derived from US Atlas (ISC License).\n'+notice+'\n-->')
target.write_text(out, encoding='utf-8')
print(f'{len(brands)} brands, {len(states)} states, {len(out.encode()):,} bytes → {target}')
