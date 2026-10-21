"""Definition-level audit of the specified repeated reciprocal punishment failure."""
from fractions import Fraction as F
import json

def unit_payoff(themes,history,player):
    chosen=themes[history[player]]
    return sum((F(1,sum(x in themes[a] for a in history)) for x in chosen),F(0))

def main():
    checked=[]
    for t in range(1,101):
        x,a=F(7),F(11)
        gap=(x+a)/2-x/(t+1)-a/t
        formula=F(t-1,2*(t+1))*x+F(t-2,2*t)*a
        assert gap==formula
        if t>=2:assert gap>0
        upper=F(3-t,2*(t+1))*x
        bupper=F(t,t+1)*x
        assert x/(t+1)+bupper/t-x/2==upper
        checked.append({'tail':t,'omission_upper_over_x':str(F(3-t,2*(t+1)))})
    x0={('x0',i) for i in range(3)};x1={('x1',i) for i in range(3)}
    a0={('a0',i) for i in range(2)};a1={('a1',i) for i in range(2)}
    b={('b',i) for i in range(2)}
    themes=(x0|a0,x1|a1,x0|b)
    actual=(2,1,0,0);deviation=(2,1,0,1)
    u=unit_payoff(themes,actual,3);v=unit_payoff(themes,deviation,3)
    assert u==2 and v==F(5,2) and v>u
    print(json.dumps({'scope':'specified reciprocal-tail mechanism only','coefficient_identities_checked':len(checked),'unit_customer_last_node':{'history':['B0','A1','A0'],'specified':'A0','specified_payoff':str(u),'profitable_alternative':'A1','alternative_payoff':str(v)},'tail_omission_bounds':checked[:5]},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
