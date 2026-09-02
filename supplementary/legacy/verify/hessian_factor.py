from mpmath import mp,mpf,log as mlog
mp.dps=50
# Claim: J_C = d*delta^2 * sum w ||z-zbar||_2^2 + O(delta^3),
# because Hessian of negentropy at u=(1/2d,...) is diag(1/u_j)=2d*I, and KL~ (1/2) x^T H x.
# => (1/2)(2d)||delta z||^2 = d delta^2 ||z||^2.  Verify.
for d in [1,2,3,5]:
    n=4
    import random; random.seed(d)
    Z=[]
    for i in range(n):
        a=[mpf(random.randint(-4,4)) for _ in range(d)]
        z=[]
        for x in a: z+=[x,-x]
        Z.append(z)
    w=[mpf(1)/n]*n
    zbar=[sum(w[i]*Z[i][j] for i in range(n)) for j in range(2*d)]
    quadsum=sum(w[i]*sum((Z[i][j]-zbar[j])**2 for j in range(2*d)) for i in range(n))
    if quadsum==0: continue
    delta=mpf(10)**-9
    P=[[mpf(1)/(2*d)+delta*Z[i][j] for j in range(2*d)] for i in range(n)]
    pb=[mpf(1)/(2*d)+delta*zbar[j] for j in range(2*d)]
    J=sum(w[i]*sum(P[i][j]*mlog(P[i][j]/pb[j]) for j in range(2*d)) for i in range(n))
    pred=d*delta**2*quadsum
    print(f"d={d}: J={mp.nstr(J,12)}  d*delta^2*Q={mp.nstr(pred,12)}  ratio={mp.nstr(J/pred,12)}")
print("ratio -> 1 confirms the factor 'd' (Hessian 2d*I, halved) is correct.")
