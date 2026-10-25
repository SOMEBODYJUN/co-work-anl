"""Exact full-parameter attack on H_root(1)>=0 for 3econ x 2bank, m=4.

Parameter t=a/b>0; normalized bank value is one.  All comparisons in full
ordered-history set-valued BI are among the sixteen lines t/p+1/q, p,q=1..4.
Open-cell outcomes are frozen only inside their cell. Critical points are rerun
with actual ties. No imports from canonical/author models or solvers.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path
import json
import sys

THEMES=tuple(product(range(3),range(2)))
ACTIONS=tuple(range(len(THEMES)))
M=4
Line=tuple


def eval_line(line,t):return line[0]*t+line[1]
def plus(x,y):return (x[0]+y[0],x[1]+y[1])
def minus(x,y):return (x[0]-y[0],x[1]-y[1])
def encode_line(line):return {'slope':str(line[0]),'intercept':str(line[1])}


@lru_cache(None)
def payoff_lines(terminal):
    out=[]
    for act in terminal:
        econ,bank=THEMES[act]
        p=sum(THEMES[a][0]==econ for a in terminal)
        q=sum(THEMES[a][1]==bank for a in terminal)
        out.append((F(1,p),F(1,q)))
    return tuple(out)


def complete_BI(t):
    outcomes={};floors={};floor_lines={};forced_entries=0
    def solve(h):
        nonlocal forced_entries
        if len(h)==M:
            result=frozenset({h})
        else:
            i=len(h)
            children={a:solve(h+(a,)) for a in ACTIONS}
            least={}
            for a in ACTIONS:
                forced_entries+=1
                least[a]=min((eval_line(payoff_lines(z)[i],t),payoff_lines(z)[i])
                             for z in children[a])
            floor=max(pair[0] for pair in least.values())
            floors[h]=floor
            floor_lines[h]=min(pair[1] for pair in least.values() if pair[0]==floor)
            result=frozenset(z for a in ACTIONS for z in children[a]
                             if eval_line(payoff_lines(z)[i],t)>=floor)
            assert result
        outcomes[h]=result
        return result
    solve(())
    assert len(outcomes)==1555 and len(floors)==259 and forced_entries==1554
    return outcomes,floors,floor_lines


def root_menus(t):
    outcomes,floors,floor_lines=complete_BI(t)
    rows=[]
    for a in ACTIONS:
        theta=floors[(a,)];theta_line=floor_lines[(a,)]
        menu=[]
        for b in ACTIONS:
            for z in outcomes[(a,b)]:
                d,v=payoff_lines(z)[:2]
                value=eval_line(minus(d,v),t)+theta
                line=plus(minus(d,v),theta_line)
                menu.append((value,line,b,z))
        value,line,b,z=min(menu)
        rows.append({'A':a,'theta':theta,'theta_line':theta_line,
                     'H_A':value,'witness_B':b,'witness_terminal':z,
                     'lines':frozenset(row[1] for row in menu),
                     'grandchild_outcomes':sum(len(outcomes[(a,b)]) for b in ACTIONS)})
    # Resource relabeling is transitive on all six root themes.  Check the exact
    # coefficient multisets too, rather than only numeric equality at t.
    assert len({row['theta'] for row in rows})==1
    assert len({row['H_A'] for row in rows})==1
    assert all(row['lines']==rows[0]['lines'] for row in rows)
    return rows,outcomes,floors


def payoff_grid():
    lines=tuple((F(1,p),F(1,q)) for p,q in product(range(1,5),repeat=2))
    grid=sorted({(b2-b1)/(a1-a2) for (a1,b1),(a2,b2) in combinations(lines,2)
                 if a1!=a2 and (b2-b1)/(a1-a2)>0})
    return lines,grid


def serialize_rows(rows):
    return [{'A':r['A'],'theta':str(r['theta']),'H_A':str(r['H_A']),
             'witness_B':r['witness_B'],'witness_terminal':r['witness_terminal'],
             'd_line':encode_line(payoff_lines(r['witness_terminal'])[0]),
             'v_line':encode_line(payoff_lines(r['witness_terminal'])[1]),
             'grandchild_outcomes':r['grandchild_outcomes']} for r in rows]


def interval_counterexample(left,right,lines):
    """Produce an exact interior point if an endpoint/slope certificate is negative."""
    for line in lines:
        slope,intercept=line
        if eval_line(line,left)<0:
            sample=left+1 if right is None else (left+right)/2
            if slope>0:sample=min(sample,(left-intercept/slope)/2)
            assert sample>left and (right is None or sample<right)
            assert eval_line(line,sample)<0
            return sample
        if right is not None and eval_line(line,right)<0:
            sample=(left+right)/2
            if slope<0:sample=max(sample,(right-intercept/slope)/2)
            assert left<sample<right and eval_line(line,sample)<0
            return sample
        if right is None and slope<0:
            sample=max(left+1,-intercept/slope+1)
            assert sample>left and eval_line(line,sample)<0
            return sample
    return None


def main():
    if '--regression' in sys.argv:
        regression=[]
        for a,b in [(1,9),(1,2),(1,1),(2,1),(3,1),(9,1),(3,2)]:
            t=F(a,b)
            rows,outcomes,floors=root_menus(t)
            assert all(row['H_A']*b==F(b,2) and row['theta']*b==F(a+b,2) for row in rows)
            # Independent literal unit-client expansion at every terminal.
            clients=tuple((0,res) for res in range(3) for _ in range(a))
            clients+=tuple((1,res) for res in range(2) for _ in range(b))
            expanded_checks=0
            for terminal in product(ACTIONS,repeat=M):
                values=[0]*M
                for dim,res in clients:
                    owners=[i for i,act in enumerate(terminal) if THEMES[act][dim]==res]
                    for i in owners:values[i]+=12//len(owners)
                assert all(F(value,12)==b*eval_line(line,t)
                           for value,line in zip(values,payoff_lines(terminal)))
                expanded_checks+=1
            regression.append({'a':a,'b':b,'unit_clients':len(clients),
                               'all_terminal_unit_expansion_checks':expanded_checks,
                               'H_root_exact':str(rows[0]['H_A']*b),
                               'theta_exact':str(rows[0]['theta']*b),
                               'all_forced_root_rows_normalized':serialize_rows(rows),
                               'ordered_states':len(outcomes),
                               'decision_states':len(floors),'all_forced_BI_entries':1554})
        report={'status':'PASS: designated literal-unit Fraction regressions',
                'candidate':'four-player 3econ x 2bank has H_root(1)=b/2',
                'cases':regression,
                'scope':'Cross-check of the analytic proof, not its all-parameter justification.'}
        Path(__file__).with_name('H_one_parametric_regression.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps({'status':report['status'],'cases':len(regression)},indent=2))
        return
    lines,grid=payoff_grid()
    endpoints=[F(0)]+grid
    cells=[];negative_points=[]
    for index,left in enumerate(endpoints):
        right=grid[index] if index<len(grid) else None
        sample=(left+right)/2 if right is not None else left+1
        rows,_,_=root_menus(sample)
        # On an open payoff-order cell every BI inequality has the same sign.
        # Distinct utility lines cannot tie here; theta is one fixed line.
        theta_lines={r['theta_line'] for r in rows}
        assert len(theta_lines)==1
        expressions=rows[0]['lines']
        left_limit=min(eval_line(line,left) for line in expressions)
        right_limit=None if right is None else min(eval_line(line,right) for line in expressions)
        tail_slope=None if right is not None else min(line[0] for line in expressions)
        good=left_limit>=0 and (right_limit>=0 if right is not None else tail_slope>=0)
        exact_half=(F(0),F(1,2)) in expressions and left_limit==F(1,2)
        exact_half=exact_half and (right_limit==F(1,2) if right is not None else tail_slope>=0)
        bad=interval_counterexample(left,right,expressions)
        assert good==(bad is None)
        if bad is not None:negative_points.append(bad)
        cells.append({'left':str(left),'right':None if right is None else str(right),
                      'sample':str(sample),'theta_line':encode_line(rows[0]['theta_line']),
                      'H_concave_affine_menu':[encode_line(line) for line in sorted(expressions)],
                      'H_left_one_sided':str(left_limit),
                      'H_right_one_sided':None if right_limit is None else str(right_limit),
                      'tail_minimum_slope':None if tail_slope is None else str(tail_slope),
                      'nonnegative_certificate':good,
                      'exact_constant_one_half_certificate':exact_half,
                      'all_forced_root_rows_at_sample':serialize_rows(rows)})
    point_rows=[]
    for t in grid:
        rows,_,_=root_menus(t)
        value=max(row['H_A'] for row in rows)
        if value<0:negative_points.append(t)
        point_rows.append({'t':str(t),'H_at_actual_ties':str(value),
                           'all_forced_root_rows':serialize_rows(rows)})
    table=[]
    for j,point in enumerate(point_rows):
        table.append({'t':point['t'],
                      'H_from_left':cells[j]['H_right_one_sided'],
                      'H_at_actual_ties':point['H_at_actual_ties'],
                      'H_from_right':cells[j+1]['H_left_one_sided']})
    exact_constant=all(c['exact_constant_one_half_certificate'] for c in cells)
    exact_constant=exact_constant and all(F(p['H_at_actual_ties'])==F(1,2) for p in point_rows)
    report={'status':'NEGATIVE WITNESS' if negative_points else
                    ('EXACT: this named family has H_root(1)=b/2' if exact_constant else
                     'PASS: this entire parameter family has H_root(1)>=0'),
            'exact_candidate':'H_root(1)>=0 for four-player 3econ x 2bank, a,b>0',
            'normalization':'b=1, t=a/b>0; rational parameters clear denominators to distinct unit clients',
            'original_payoff_lines':[encode_line(line) for line in lines],
            'positive_payoff_order_grid':list(map(str,grid)),
            'open_cells':len(cells),'critical_points':len(point_rows),'BI_runs':len(cells)+len(point_rows),
            'states_per_run':1555,'decision_states_per_run':259,'all_forced_entries_per_run':1554,
            'including_own_at_every_history':True,
            'all_open_cells':cells,'all_critical_points':point_rows,'comparison_table':table,
            'negative_rational_parameters':list(map(str,negative_points)),
            'exact_constant_one_half_all_open_cells_and_critical_points':exact_constant,
            'zero_boundary_right_limit':cells[0]['H_left_one_sided'],
            'tail_slope':cells[-1]['tail_minimum_slope'],
            'scope':'Exact full-parameter diagnostic of the named family only; no general H theorem, no half bound, no expansion planned.'}
    destination=Path(__file__).with_suffix('.json')
    destination.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({key:report[key] for key in ('status','open_cells','critical_points','BI_runs',
                      'zero_boundary_right_limit','tail_slope','negative_rational_parameters')},indent=2))
    print('one-sided / actual-tie / one-sided table:')
    for row in table:print(row['t'],row['H_from_left'],row['H_at_actual_ties'],row['H_from_right'])


if __name__=='__main__':main()
