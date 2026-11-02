from search_background import *
rng=random.Random(171771)
best_pot=Fraction(1000);best_reg=Fraction(1000)
for trial in range(3000):
 q,r=7,5
 weights={mask:rng.randrange(1,13) for mask in rng.sample(range(1,1<<q),rng.randrange(7,25))}
 prefix=[0]*q
 for _ in range(rng.randrange(0,9)):prefix[rng.randrange(q)]+=1
 sol=BackgroundSolver(q,r,prefix,weights)
 bgmask=0
 for a in range(q):
  if prefix[a]:bgmask|=1<<a
 def new(c):return sum(w for mask,w in weights.items() if not mask&bgmask and any(c[a] and mask>>a&1 for a in range(q)))
 maxnew=max(new(c)for c in sol.terminals)
 optcover=max(sum(w for mask,w in weights.items()if any(c[a]and mask>>a&1 for a in range(q)))for c in sol.terminals)
 out=sol.out
 while out:
  bit=out&-out;i=bit.bit_length()-1;out-=bit;c=sol.terminals[i]
  gap=sol.profits[i]+new(c)-maxnew
  if gap<best_reg:
   best_reg=gap
   if gap<0:
    obj={'trial':trial,'q':q,'r':r,'weights':weights,'prefix':prefix,'actual':c,'gap':str(gap),'maxnew':maxnew,'R':str(sol.profits[i]),'actualnew':new(c)}
    print('regret failure',obj);(ROOT/'regret_counterexample.json').write_text(json.dumps(obj,indent=2));raise SystemExit
  if not any(prefix):
   pot=sum(w*sum(Fraction(1,j)for j in range(1,1+sum(c[a]for a in range(q)if mask>>a&1)))for mask,w in weights.items())
   if pot<optcover:
    obj={'trial':trial,'q':q,'r':r,'weights':weights,'actual':c,'pot':str(pot),'opt':optcover}
    print('potential failure',obj);(ROOT/'potential_counterexample.json').write_text(json.dumps(obj,indent=2));raise SystemExit
 if trial%100==0:print(trial,'regret min',best_reg,flush=True)
