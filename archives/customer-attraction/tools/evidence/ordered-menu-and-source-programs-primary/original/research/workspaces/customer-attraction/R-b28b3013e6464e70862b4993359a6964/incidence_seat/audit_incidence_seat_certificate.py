from fractions import Fraction


def build(n):
    s=2*n
    incidence=[{(r+k)%(2*n) for k in range(n)} for r in range(2*n)]
    # maxima j contain private P_j plus x_r whenever j in incidence[r]
    p=[1]*s
    q=[sum(1 for I in incidence if j in I) for j in range(s)]
    assert q==[n]*s
    seats=[(Fraction(p[j],k)+Fraction(q[j],n),j,k) for j in range(s) for k in range(1,n+1)]
    nu=sorted((v for v,_,_ in seats),reverse=True)[n-1]
    assert nu==2
    a=[]
    for j in range(s):
        e=sum(1 for v, jj, k in seats if jj==j and v>nu)
        a.append(e+1)
    assert a==[1]*s
    y=[1]*s
    for I in incidence:
        assert sum(y[j] for j in I)>=n
    assert sum(y)<=2*n
    U=s+s
    # (4)-(6) certificate ratio; c=0
    assert Fraction(U, sum(y)*nu) == Fraction(4*n,4*n)
    return {'n':n,'s':s,'nu':str(nu),'sum_y':sum(y),'U':U,'tau_inc_lower_bound':s}

if __name__=='__main__':
    rows=[build(n) for n in range(2,9)]
    print(rows)
