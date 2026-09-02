import numpy as np, math
def h(e): return -e*math.log(e)-(1-e)*math.log(1-e)
print("CLAIM C: negative resolution of open:global-kl-fisher")
print("P_- = Bern(eps), P_+ = Bern(1-eps), equiprobable, M=1.  Mixture = Bern(1/2).")
print(f"{'eps':>10} {'RetKL(1)':>14} {'L_eps':>12} {'Sigma_eta':>14} {'ratio':>14} {'Sigma_F':>14} {'ratio_F':>14}")
for e in [1e-1,1e-2,1e-3,1e-5,1e-8,1e-12]:
    Ret = math.log(2)-h(e)            # I(S;Y) = H(mix) - avg H
    L = math.log((1-e)/e)
    Sig = L**2                        # eta_pm = +-L, equal weights -> var = L^2
    IF = 0.25                         # A''(eta) at pbar=1/2 is p(1-p)=1/4
    SigF = IF*Sig
    print(f"{e:10.0e} {Ret:14.8f} {L:12.4f} {Sig:14.4f} {Ret/Sig:14.3e} {SigF:14.4f} {Ret/SigF:14.3e}")
print("\nRetKL(1) <= log 2 =",math.log(2),"  bounded;  Sigma_eta -> infinity.  Ratio -> 0.  NO universal c>0.")

# brute check RetKL(1) really is the M=1 retention (only quotient is trivial, rep = mixture centroid)
def kl(p,q): return sum(a*math.log(a/b) for a,b in zip(p,q) if a>0)
for e in [1e-3,1e-6]:
    pp=[1-e,e]; pm=[e,1-e]; pbar=[0.5,0.5]
    print(f"  eps={e:g}: direct 0.5*KL(P+||mix)+0.5*KL(P-||mix) = {0.5*kl(pp,pbar)+0.5*kl(pm,pbar):.10f}"
          f"   vs log2-h(eps) = {math.log(2)-h(e):.10f}")
