from search_background import *
rng=random.Random(3939)
for trial in range(1000):
 q,r=7,5
 weights={mask:rng.randrange(1,15) for mask in rng.sample(range(1,1<<q),rng.randrange(7,30))}
 sol=BackgroundSolver(q,r,[0]*q,weights)
 out=sol.out
 while out:
  bit=out&-out;i=bit.bit_length()-1;out-=bit;t=sol.terminals[i];W=sol.profits[i]
  states={(0,)*q}
  for depth in range(r):
   nxt=set()
   for c in states:
    for a in range(q):
     if c[a]>=t[a]:continue
     d=list(c);d[a]+=1;d=tuple(d)
     if sol.solve(d)&bit and sol.pays[i][a]>=sol.thresholds[c]:
      if depth==r-1 and Fraction(sol.pays[i][a],sol.scale)*(r-1)>W:
       obj={'trial':trial,'q':q,'r':r,'weights':weights,'actual':t,'last':a,'W':str(W),'lastpay':str(Fraction(sol.pays[i][a],sol.scale)),'prefix':c}
       print(obj);(ROOT/'last_payoff_counterexample.json').write_text(json.dumps(obj,indent=2));raise SystemExit
      nxt.add(d)
   states=nxt
print('no failure')
