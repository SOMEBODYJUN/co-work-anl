"""Exact rational checks for the two-realized-coverage proof.

Checks the exceptional local slack identity on every one-client membership atom
of (A,B,T,S), then verifies every multiplicity coefficient and all62 binary
coverage words. This is an algebra audit, not a finite search or a proof of SPE.
"""
from fractions import Fraction as F
from itertools import product
from math import comb
import json


def u(chosen, profile, atom):
    if not atom[chosen]: return F(0)
    return F(1,sum(atom[x] for x in profile))

failures=[]
for atom in product([0,1],repeat=4):
    A,B,T,S=range(4)
    a=atom[A]*(1-atom[B]); c=atom[A]*atom[B]
    p=atom[T]*a; q=atom[T]*atom[B]*(1-atom[A])
    r=atom[T]*c; z=atom[T]*(1-atom[A])*(1-atom[B])
    f5=u(A,[A]*5+[B],atom)-u(T,[A]*4+[T,S],atom)
    f6old=u(B,[A]*5+[B],atom)-u(S,[A]*5+[S],atom)
    f6new=u(S,[A]*4+[T,S],atom)-u(B,[A]*4+[T,B],atom)
    target=F(7,30)*a+F(1,6)*c-F(1,5)*p-F(1,2)*q-F(1,6)*r-z
    identity_rhs=f5+f6old+f6new+F(1,30)*atom[A]*(1-atom[S])
    if target!=identity_rhs:failures.append({'atom':atom,'difference':str(target-identity_rhs)})
assert not failures
R=F(137,70);table=[]
for k in range(1,5):
    ell=6-k
    alpha=F(k,k+1);beta=1+F(5,ell);rmax=F(ell+1,k)
    assert beta>alpha
    private_ratio=(alpha+beta*rmax)/(1+rmax)
    bound=max(private_ratio,F(11,6))
    assert bound<=R<2
    # Exact affine decomposition: R W - (alpha*a+beta*b+11*c/6)
    # = (beta-R)*(rmax*a-b) + residual_a*a + residual_c*c.
    residual_a=R-alpha-(beta-R)*rmax
    residual_c=R-F(11,6)
    assert beta-R>=0 and residual_a>=0 and residual_c>=0
    half_margin=2-alpha-(beta-2)*rmax
    assert half_margin>0
    table.append({'k_A':k,'ell_B':ell,'canonical_words_last_B':comb(5,k),'b_over_a_upper':str(rmax),'last_node_private_ratio_upper':str(private_ratio),'including_intersection_ratio_upper':str(bound),'half_margin_a':str(half_margin),'uniform_bound_decomposition':{'coefficient_of_rmax_a_minus_b':str(beta-R),'coefficient_of_a':str(residual_a),'coefficient_of_c':str(residual_c)}})
# Exceptional F2=11a/5+b/2+11c/6. Identity below uses b>=a/6.
factor_b=F(51,35);factor_c=F(13,105)
assert R-F(11,5)==-factor_b/F(6)
assert R-F(1,2)==factor_b
assert R-F(11,6)==factor_c
words=[]
for word in product('AB',repeat=6):
    if len(set(word))<2:continue
    final=word[-1];other='A' if final=='B' else 'B';k=word.count(other)
    route='generic_last_node' if k<=4 else 'exceptional_three_slacks'
    if k==5:assert word==tuple(other*5+final)
    words.append((''.join(word),route))
assert len(words)==62
out={'arithmetic':'fractions.Fraction exact rational','exceptional_identity_atoms_checked':16,'exceptional_identity_failures':failures,'uniform_OPT_over_W_bound':str(R),'uniform_half_gap':str(2-R),'multiplicity_table':table,'exceptional_uniform_decomposition':{'coefficient_of_b_minus_a_over_6':str(factor_b),'coefficient_of_c':str(factor_c)},'binary_words_checked':len(words),'generic_words':sum(route=='generic_last_node' for _,route in words),'exceptional_words':[word for word,route in words if route=='exceptional_three_slacks'],'scope':'Algebraic identity and coverage-word audit only. The written proof derives the nonnegative SPE slacks at genuine histories of one complete strategy. No numerical search is promoted to a theorem.'}
print(json.dumps(out,indent=2,sort_keys=True))
