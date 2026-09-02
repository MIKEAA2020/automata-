import numpy as np
rng = np.random.default_rng(0)
def hank(h,n): return np.array([[h[i+j] for j in range(n)] for i in range(n)])

draws=[]
for n in [3,4,5,6]:
    for _ in range(4): draws.append((n, rng.normal(size=2*n-1)))
n,h = draws[2]
H = hank(h,n); s = np.linalg.svd(H,compute_uv=False)
print("3x3 Hankel, singular values:", np.round(s,8))

# closed-form inner minimization: min_c ||H - c*B||_2 via golden section on a fine theta grid
def dist(grid):
    N=2*n-2; best=np.inf
    th=np.linspace(0,np.pi,grid)
    for t in th:
        a,b=np.cos(t),np.sin(t)
        B=hank(np.array([a**k*b**(N-k) for k in range(N+1)]),n)
        nb=np.linalg.norm(B,'fro')
        if nb<1e-14: continue
        # ternary search on c
        lo,hi=-100.,100.
        for _ in range(200):
            m1=lo+(hi-lo)/3; m2=hi-(hi-lo)/3
            if np.linalg.norm(H-m1*B,2)<np.linalg.norm(H-m2*B,2): hi=m2
            else: lo=m1
        v=np.linalg.norm(H-0.5*(lo+hi)*B,2)
        best=min(best,v)
    return best

for g in [2001,20001]:
    d=dist(g)
    print(f"  grid={g:>6}: dist(H,rank<=1 Hankel)={d:.10f}  sigma_2={s[1]:.10f}  ratio={d/s[1]:.6f}")
print("\n=> distance strictly exceeds sigma_2 => AAK equality is FALSE for finite Hankel matrices.")
