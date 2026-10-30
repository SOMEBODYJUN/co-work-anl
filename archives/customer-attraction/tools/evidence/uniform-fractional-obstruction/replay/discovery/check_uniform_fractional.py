import sys
sys.argv=['fractional_root_cutting.py','--rounds','0']
exec(open('research/workspaces/customer-attraction/R-077c0cacfba24288be91dee1acf6d484/security/aggregate_attack/fractional_root_cutting.py').read().split('rng=np.random')[0])
q=np.ones(k)/k
for a in range(k):
 c=X[:,a]/(1+(r-1)*(X@q))-root
 sol=linprog(-c,A_ub=-Gamma,b_ub=np.zeros(len(Gamma)),A_eq=[root],b_eq=[1],bounds=[(0,3)]*(len(types)-1)+[(0,0)])
 print(a,-sol.fun,{int(t):float(v) for t,v in zip(types,sol.x) if v>1e-7})
