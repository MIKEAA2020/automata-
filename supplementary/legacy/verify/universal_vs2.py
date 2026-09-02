"""Is the version-space strategy a genuine UNIVERSAL tree, and does it
actually terminate at the def:output-aware-sync objective?

Simulate it against EVERY machine in a small H_M, driving the input choice
purely from the transcript (via the version space), never from the true A.
Then compare its worst-case depth to the claimed bound (M-1)(N_M-1).
"""
import itertools
from collections import deque

def sep_word(M,nI,tau,lam,q,qp):
    if q==qp: return None
    seen={(min(q,qp),max(q,qp))}; dq=deque([(q,qp,())])
    while dq:
        a,b,w=dq.popleft()
        for x in range(nI):
            if lam[a][x]!=lam[b][x]: return w+(x,)
        for x in range(nI):
            na,nb=tau[a][x],tau[b][x]
            k=(min(na,nb),max(na,nb))
            if na!=nb and k not in seen: seen.add(k); dq.append((na,nb,w+(x,)))
    return None

def classes(M,nI,tau,lam):
    part={s:tuple(lam[s]) for s in range(M)}
    c={}; part={s:c.setdefault(part[s],len(c)) for s in range(M)}
    for _ in range(M+1):
        new={s:(part[s],tuple(part[tau[s][a]] for a in range(nI))) for s in range(M)}
        c2={}; new={s:c2.setdefault(new[s],len(c2)) for s in range(M)}
        if len(set(new.values()))==len(set(part.values())): break
        part=new
    return part

def build_H(M,nI,nO):
    H=[]
    for tau in itertools.product(itertools.product(range(M),repeat=nI),repeat=M):
        for lam in itertools.product(itertools.product(range(nO),repeat=nI),repeat=M):
            cls=classes(M,nI,tau,lam)
            if len(set(cls.values()))==M: H.append((tau,lam,cls))
    return H

for (M,nI,nO) in [(2,1,2),(2,2,2),(3,1,2)]:
    H=build_H(M,nI,nO)
    NM=sum(M for _ in H)
    print("="*76)
    print(f"M={M}, |I|={nI}, |O|={nO}:  |H_M|={len(H)} minimal machines, N_M={NM}")
    print(f"  claimed bound (M-1)(N_M-1) = {(M-1)*(NM-1)}")
    # universal simulation: V determined by transcript ONLY
    worst=0
    for ti,(TAU,LAM,CLS) in enumerate(H):
        for q0 in range(M):
            V=[(i,q) for i in range(len(H)) for q in range(M)]
            cur=q0; steps=0; hist=()
            while steps < 5*NM:
                # objective: no consistent machine carries 2 obs-distinct cands
                bym={}
                for (i,q) in V: bym.setdefault(i,set()).add(q)
                target=None
                for i,qs in bym.items():
                    cls=H[i][2]
                    reps={cls[q] for q in qs}
                    if len(reps)>1:
                        qq=sorted(qs)
                        for a in range(len(qq)):
                            for b in range(a+1,len(qq)):
                                if cls[qq[a]]!=cls[qq[b]]:
                                    target=(i,qq[a],qq[b]); break
                            if target: break
                    if target: break
                if target is None: break
                i,q,qp=target
                w=sep_word(M,nI,H[i][0],H[i][1],q,qp)
                if w is None: break
                for x in w:
                    obs=LAM[cur][x]; cur=TAU[cur][x]; steps+=1
                    V=[(j,s) for (j,s) in V if H[j][1][s][x]==obs]
                    V=[(j,H[j][0][s][x]) for (j,s) in V]
            worst=max(worst,steps)
    print(f"  observed worst-case universal depth = {worst}   (bound holds: {worst<=(M-1)*(NM-1)})")
