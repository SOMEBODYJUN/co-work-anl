# Why a zero-regret deletion switch cannot have a credible controller

2026-10-24. **Exact negative analysis of a construction attempt.** The original unit-client, common-catalogue, complete ordered-history pure-SPE model is used throughout. The argument excludes the stated switch family for arbitrary total player count; it is not a general obstruction to proving or disproving Q-CAG-HALF.

## 1. The attempted switch

Take pairwise disjoint client blocks F,P,H,Q of nonnegative integer sizes f,p,h,q, with f>0, p>0, and

    q=f+2p.

The three legal topics are

    A=F,  B=F union P union H,  T=H union Q.

Write t=h+q for the size of T. The proposed last three actual actions are `(A,B,T)`, with no earlier coverage of these four blocks. The intended controller is the player choosing A; deleting this player leaves the virtual actual path `(B,T)`.

After the original prefix A, prescribe B to the penultimate player and T to the last player. At both alternative penultimate actions A and T, also prescribe T to the last player. These last-player choices are genuine original best responses:

- After `(A,B)`, T gives `q+h/2`, exceeding B's `f/3+p/2+h/2` and A's `f/3`.
- After `(A,T)`, T and B tie at `t/2=f/2+p+h/2`; A gives `f/2`.
- After `(A,A)`, T gives `q+h`, exceeding B's `f/3+p+h` and A's `f/3`.

The original penultimate player's prescribed B payoff is `f/2+p+h/2=t/2`. Choosing T followed by the prescribed T also gives t/2, and choosing A gives f/2. Thus this entire original two-player child is a complete pure SPE.

## 2. Deletion creates an apparently harmless virtual actual path

Delete A's load but keep that child policy. Let

    b=f+p+h/2.

The surviving actual B player's payoff is b. Its virtual deviations to T and A give respectively `t/2=b-f/2` and f, both at most b. The last player on the actual path chooses T, which is still a strict best response after B: its payoff is `q+h/2`, whereas B gives `(f+p+h)/2` and A gives f/2. Therefore **both surviving actual nodes have zero one-step regret** in the retained complete strategy.

Nevertheless `(B,T)` is not the actual ordered path of any complete pure SPE in this two-player game. After a root deviation to T, the last player's unique best response is B, with payoff

    u_last(B | T)=f+p+h/2=b,

strictly greater than T's t/2 and A's f. The deviator then receives `q+h/2=b+p>b`. Every complete SPE must therefore reject B at the root.

For example, `(f,p,h,q)=(2,1,2,4)` gives surviving actual utilities `(4,5)`, zero actual-node regret under the virtual policy, and a forced credible root deviation payoff 5. These numbers illustrate the formulas; they are not a full original SPE counterexample.

## 3. The controller is never rational in the original game

The attempted original controller receives only f/2 on `(A,B,T)`. Force it instead to choose T. In **every** complete pure-SPE continuation, the subsequent two players cannot both choose T. If they did, the last player would receive t/3, but switching to B would give

    f+p+h/3 > (f+2p+h)/3 = t/3,

with strict difference `(2f+p)/3`.

Hence at most one of the two followers chooses T. Each Q-client has final load at most two, while each H-client has final load at most three. The deviating controller consequently receives at least

    q/2+h/3 = f/2+p+h/3 > f/2.

This is a strict profitable deviation against **every credible continuation**. In particular there is no missing clever choice of off-path ties that could make the controller rational. The proposed original actual path cannot occur in a complete pure SPE.

This exclusion also permits any earlier prefix and extra catalogue actions supported on a disjoint client universe. That prefix leaves the four displayed blocks unloaded, and such extra actions do not increase their final loads. The last-player deviation to B still rules out two T-followers. Thus arbitrarily many disjoint bank players before this final triple do not repair the switch. A bank that changes the four blocks or the catalogue intersections is outside the stated exclusion.

## 4. Exact conclusion

This primitive separates zero actual-node regret from full off-path credibility only for a prescribed child strategy; it does **not** realize the premise of the desired original full-SPE deletion attack. Reporting it as such a counterexample would omit the controller's profitable deviation.

Moreover B union T already equals the full catalogue union, so its welfare has no half deficit. The insurance compiler cannot extract a target counterexample from this path: even before paying any nonnegative defect cost, `OPT-2W=-W<0`. No assertion about more general switch gadgets, all possible repair theorems, or the truth of Q-CAG-HALF follows.
