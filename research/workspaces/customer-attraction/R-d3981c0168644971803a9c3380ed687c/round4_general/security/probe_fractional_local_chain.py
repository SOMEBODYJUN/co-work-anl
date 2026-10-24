"""Directed test of one all-input local δ-chain candidate on an existing
fixed full strategy cone. Root p=q uniform is certified optimal by linear KKT;
child q=(e1+e2)/2 supplies only an upper bound. Not a general proof.
"""
exec((__import__('pathlib').Path(__file__).with_name('probe_optimal_fractional_payment.py')).read_text().split("gap=[a-b")[0])
n=len(types)
qc=[Q(int(a in (1,2)),2) for a in range(k)]
h=[[Q((t>>a)&1,1)/(1+((t>>z[0])&1)+(m-2)*sum(qc[b] for b in range(k) if (t>>b)&1)) for t in types] for a in range(k)]
A=[[-x for x in row]+[Q(0)] for row in IC]+[row+[Q(-1)] for row in h]
obj=[u(t,z,0)-m*f[0][j] for j,t in enumerate(types)]+[Q(m-1)]
res=linprog(np.array(obj,dtype=float),A_ub=np.array(A,dtype=float),b_ub=np.zeros(len(A)),A_eq=np.array([row+[Q(0)] for row in eq],dtype=float),b_eq=[1.]+[0.]*(len(eq)-1),bounds=[(0,None)]*(n+1),method='highs')
report={'candidate':'u_first+(r-1)δ_child>=rδ_parent','root_saddle':'p=q uniform','child_background':'q=(e1+e2)/2','status':res.message}
if res.success:
 report.update(numerical_minimum_upper_bound_for_local_gap=res.fun,nonzero_proposal={str(t):float(x) for t,x in zip(types,res.x[:-1]) if x>1e-9},child_upper=float(res.x[-1]))
(HERE/'fractional_local_chain_probe.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
