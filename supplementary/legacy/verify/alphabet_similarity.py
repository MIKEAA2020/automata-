"""
T45 / Item 4.  Minimal output alphabet for the tangent-space embedding.

Verifies, exactly as stated in rem:output-alphabet-2d:
 (1) d=2, |O|=3: Gram diag(2,6), disc 12 ~ 3 mod squares != 1, so NO rational
     centred similarity; confirmed by exhaustive integer search.
 (2) d=3, |O|=4: the three non-constant rows of a Hadamard matrix of order 4
     ARE zero-sum, pairwise orthogonal, equal norm 4 -> similarity with c=4.
 (3) the Hadamard construction generalises to orders 8, 16 (d = 7, 15).
 (4) the doubling map is a similarity with c=2 for every d.
"""
from itertools import product
from fractions import Fraction as F
dot=lambda a,b: sum(x*y for x,y in zip(a,b))
def sqfree(n):
    r=1;d=2
    while d*d<=n:
        e=0
        while n%d==0: n//=d; e+=1
        if e%2: r*=d
        d+=1
    return r*n

print("="*74); print("(1) d=2, |O|=3 : the discriminant obstruction"); print("="*74)
u,v=(1,-1,0),(1,1,-2)
assert sum(u)==0 and sum(v)==0 and dot(u,v)==0
g1,g2=dot(u,u),dot(v,v)
print(f"  basis {u},{v}: Gram diag({g1},{g2}), disc {g1*g2}, class {sqfree(g1*g2)} mod squares")
assert sqfree(g1*g2)==3
print("  scalar form diag(c,c) has disc c^2, class 1.  3 != 1  => no similarity")
found=None; N=40
for a in range(-N,N+1):
  for b in range(-N,N+1):
    if not (a or b): continue
    uu=(a,b,-a-b); nu=dot(uu,uu)
    for c in range(-N,N+1):
      for e in range(-N,N+1):
        if not (c or e): continue
        vv=(c,e,-c-e)
        if dot(uu,vv) or dot(vv,vv)!=nu or a*e-b*c==0: continue
        found=(uu,vv); break
      if found: break
    if found: break
  if found: break
print(f"  exhaustive integer search |coord|<={N}: {found if found else 'NONE'}")
assert found is None

print()
print("="*74); print("(2) d=3, |O|=4 : Hadamard rows give a similarity"); print("="*74)
B=[(-1,-1,1,1),(-1,1,-1,1),(-1,1,1,-1)]
for w in B: assert sum(w)==0
assert all(dot(B[i],B[j])==0 for i in range(3) for j in range(i+1,3))
assert len({dot(w,w) for w in B})==1
c=dot(B[0],B[0])
print(f"  rows {B}")
print(f"  zero-sum: yes   pairwise orthogonal: yes   common norm c = {c}")
import random
rng=random.Random(0); worst=0
for _ in range(50000):
    a=[rng.randrange(-40,40) for _ in range(3)]
    b=[rng.randrange(-40,40) for _ in range(3)]
    za=[sum(a[i]*B[i][j] for i in range(3)) for j in range(4)]
    zb=[sum(b[i]*B[i][j] for i in range(3)) for j in range(4)]
    assert sum(za)==0
    d2=sum((x-y)**2 for x,y in zip(a,b))
    if d2: worst=max(worst,abs(F(sum((x-y)**2 for x,y in zip(za,zb)),d2)-c))
print(f"  max |ratio - c| over 50000 random pairs: {worst}")
assert worst==0
print(f"  => |O| = d+1 = 4 suffices for d=3, versus 2d = 6.  Factor 2 IS slack here.")

print()
print("="*74); print("(3) Hadamard orders 8 and 16"); print("="*74)
def syl(k):
    H=[[1]]
    for _ in range(k): H=[r+r for r in H]+[r+[-x for x in r] for r in H]
    return H
for k in (2,3,4):
    n=2**k; rows=[r for r in syl(k) if sum(r)==0]
    ok=(len(rows)==n-1
        and all(dot(rows[i],rows[j])==0 for i in range(len(rows)) for j in range(i+1,len(rows)))
        and len({dot(r,r) for r in rows})==1)
    print(f"  order {n:3d}: d = {n-1:2d} embeds in |O| = {n:2d} = d+1 (vs 2d = {2*(n-1)}): {ok}")
    assert ok

print()
print("="*74); print("(4) doubling map is a similarity with c=2 for every d"); print("="*74)
for d in (1,2,3,4,5,8):
    rng=random.Random(d); w=0
    for _ in range(4000):
        a=[rng.randrange(-30,30) for _ in range(d)]
        b=[rng.randrange(-30,30) for _ in range(d)]
        za=[v for x in a for v in (x,-x)]; zb=[v for x in b for v in (x,-x)]
        assert sum(za)==0
        d2=sum((x-y)**2 for x,y in zip(a,b))
        if d2: w=max(w,abs(F(sum((x-y)**2 for x,y in zip(za,zb)),d2)-2))
    print(f"  d={d}: |O|=2d={2*d}, max |ratio - 2| = {w}")
    assert w==0
print()
print("ALL ITEM 4 CLAIMS VERIFIED")
