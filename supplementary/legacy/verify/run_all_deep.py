#!/usr/bin/env python3
"""Master runner: execute every deep verification suite and summarize."""
import subprocess, sys, time, os
SUITES = [
 ('deep_kl_sharp.py',        'thm:global-kl-simplex constant 1 + sharpness'),
 ('deep_kl_infimum.py',      'infimum KL/||.||_2^2 = 1, exact arithmetic'),
 ('deep_apx.py',             'cor:full-kl-apx approximation preservation'),
 ('deep_csiszar.py',         'lem:csiszar-representation repaired proof'),
 ('deep_automata.py',        'EsyncSI, stream LB, halving, Moore separation'),
 ('deep_interior_fisher.py', 'thm:global-interior-fisher, correct m_K'),
 ('deep_packing.py',         'packing criterion, two-point disproof, floors'),
 ('deep_misc.py',            'Fisher no-go, sandwich, centroid, zero-retention'),
 ('ib_identity.py',          'thm:predictive-info exact identity'),
 ('sum_vs_min.py',           'sandwich converts min-floor to sum-envelope'),
]
BAD = ('VIOLATION','MISMATCH','FAILS      (excluded)'[:0],'Traceback','Error','FAIL')
root=os.path.dirname(os.path.abspath(__file__))
rows=[]
for f,desc in SUITES:
    p=os.path.join(root,f)
    if not os.path.exists(p):
        rows.append((f,desc,'MISSING',0.0)); continue
    t0=time.time()
    r=subprocess.run([sys.executable,p],capture_output=True,text=True,timeout=1700)
    dt=time.time()-t0
    out=r.stdout+r.stderr
    status='OK'
    if r.returncode!=0: status='CRASH'
    elif 'VIOLATION' in out or 'MISMATCH' in out or 'Traceback' in out: status='FLAG'
    rows.append((f,desc,status,dt))
w=max(len(f) for f,_,_,_ in rows)
print('='*92); print('DEEP VERIFICATION SUITE'); print('='*92)
for f,desc,st,dt in rows:
    print(f'  {st:<6} {f:<{w}}  {desc:<52} {dt:6.1f}s')
print('='*92)
nbad=sum(1 for _,_,st,_ in rows if st not in ('OK',))
print(f'{len(rows)-nbad}/{len(rows)} suites clean')
sys.exit(1 if nbad else 0)
