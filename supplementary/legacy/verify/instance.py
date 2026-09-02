"""
Build a VERIFIED instance of the m-point floor in the realizable stream regime,
using the manuscript's own gated transport-readout family.

Setup: Q={0,1}^L, M=2^L, unknown g:Q->Q, family size m=M^M.
Forcing stream w = concat over v of ( w_v c d^L ), length O(M log M).
Two distinct g,g' produce DIFFERENT output strings on w (they differ at the
first readout coordinate where g,g' differ).  So the m transcript laws are
mutually singular point masses => I(V;Y) = log m = M log M exactly.

Verify by direct simulation: enumerate all g for small L, run the stream,
check the output strings are pairwise distinct.
"""
import itertools, math

def build(L):
    Q=[tuple(b) for b in itertools.product([0,1],repeat=L)]
    zero=tuple([0]*L)
    def rot(v): return v[1:]+v[:1]
    def flip(v): return v[:-1]+(1-v[-1],)
    # forcing stream: for each v, w_v = r (d e^{v_i})_i , then c, then d^L
    stream=[]
    for v in Q:
        stream.append('r')
        for i in range(L):
            stream.append('d')
            if v[i]==1: stream.append('e')
        stream.append('c')
        stream += ['d']*L
    return Q, zero, rot, flip, stream

def run(L,g,Q,zero,rot,flip,stream):
    """gated machine: (free,v) / (read,u); c is a no-op in read mode."""
    mode,st='free',zero
    out=[]
    for x in stream:
        if x=='r': mode,st,y='free',zero,0
        elif x=='e':
            y=0
            if mode=='free': st=flip(st)
        elif x=='c':
            y=0
            if mode=='free': mode,st='read',g[st]
        else: # d
            y=st[0]; st=rot(st)
        out.append(y)
    return tuple(out)

print("="*74)
print("PAIRWISE DISTINCT TRANSCRIPTS  =>  MUTUALLY SINGULAR LAWS  =>  I = log m")
print("="*74)
print(f"{'L':>3}{'M':>5}{'m = M^M':>10}{'stream len':>12}{'distinct transcripts':>22}{'= m?':>7}")
for L in (1,2):
    Q,zero,rot,flip,stream = build(L)
    M=2**L
    outs=set()
    for vals in itertools.product(Q,repeat=M):
        g={Q[i]:vals[i] for i in range(M)}
        outs.add(run(L,g,Q,zero,rot,flip,stream))
    m=M**M
    print(f"{L:>3}{M:>5}{m:>10}{len(stream):>12}{len(outs):>22}{str(len(outs)==m):>7}")
    assert len(outs)==m, (len(outs),m)

print()
print("  All m transcripts distinct => the m induced laws are mutually")
print("  singular point masses on the transcript space.")
print()
print("="*74)
print("RESULTING FLOOR")
print("="*74)
for L in (1,2,3,4,5):
    M=2**L; m=M**M
    I=M*math.log(M)     # nats
    print(f"  L={L}  M={M:3d}:  I(V;Y) = log m = {I:9.3f} nats = {I/math.log(2):9.3f} bits"
          f"   (M log2 M = {M*math.log2(M):9.3f})")
print()
print("  I(V;Y) = M ln M nats = M log2 M bits, matching Est_M(T) = Theta(M log M).")
print("  So the m-point floor is SATISFIED with Delta_M = Theta(M log M),")
print("  by an explicit family already in the manuscript.")
