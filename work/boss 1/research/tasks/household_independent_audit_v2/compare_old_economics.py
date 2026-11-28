"""Compare all old monetary observations in addition to rerunning the original assertions."""
import ast
import gzip
import hashlib
import json
import math
from pathlib import Path

HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'household_independent_audit'

def load(directory, filename):
    raw=(directory/filename).read_bytes()
    return json.loads(gzip.decompress(raw) if filename.endswith('.gz') else raw)

def ast_of_verify(directory):
    module=ast.parse((directory/'independent_numeric.py').read_text())
    return ast.dump(next(n for n in module.body if isinstance(n,ast.FunctionDef) and n.name=='verify'))


def check():
    v1=load(OLD,'observed_engine_output.json.gz');v2=load(HERE,'observed_engine_output.json.gz')
    old_report=load(OLD,'numeric_report.json');new_report=load(HERE,'numeric_report.json')
    inputs=load(HERE,'independent_input.json');methods={r['id']:r['op'] for r in inputs}
    totals={'monthlyRows':0,'numericAndStateValues':0,'strategyScenarioTraces':0,'regressionCheckNames':len(new_report['checks'])}
    changes=[];max_abs=0.0;cases=[]
    def compare(x,y,label):
        nonlocal max_abs
        if isinstance(x,dict):
            for k,v in x.items():
                if k not in y:
                    changes.append([label,k,'missing']);continue
                compare(v,y[k],label+'/'+k)
        elif isinstance(x,list):
            if len(x)!=len(y):changes.append([label,'length',len(x),len(y)]);return
            for i,(u,v) in enumerate(zip(x,y)):compare(u,v,label+'/'+str(i))
        elif isinstance(x,bool) or x is None:
            totals['numericAndStateValues']+=1
            if x is not y:changes.append([label,x,y])
        elif isinstance(x,(int,float)):
            totals['numericAndStateValues']+=1
            if not isinstance(y,(int,float)):
                changes.append([label,x,y]);return
            difference=abs(x-y);max_abs=max(difference,max_abs)
            if difference>max(1e-7,abs(x)*1e-11):changes.append([label,x,y])
    for id,x in v1.items():
        y=v2[id];method=methods[id];before=len(changes)
        if 'error' in x:
            if 'error' not in y:changes.append([id,'earlier invalid data was accepted'])
        elif method=='simulate':
            totals['monthlyRows']+=len(x['rows']);compare(x['rows'],y['rows'],id+'/months')
            for k in ['points','completed','firstFailure','supportMonths','endDebt','interestTotal','rentNet','saleNet','terminalReal','worstGap']:
                compare(x['summary'][k],y['summary'][k],id+'/'+k)
        elif method=='assess':
            old_actions={json.dumps(r['actions'],sort_keys=True):r for r in x['all']}
            new_actions={json.dumps(r['actions'],sort_keys=True):r for r in y['all']}
            if old_actions.keys()!=new_actions.keys():changes.append([id,'candidate action space changed',len(old_actions),len(new_actions)])
            for acts in old_actions.keys()&new_actions.keys():
                for scenario,old_path in old_actions[acts]['scenarios'].items():
                    q=new_actions[acts]['scenarios'][scenario];totals['strategyScenarioTraces']+=1
                    if old_path['hash']!=q['hash']:changes.append([id,acts,scenario,'cent-level monthly path differs'])
                    compare({k:old_path[k] for k in ['completed','feasible','rows','firstFailure','terminalReal','terminalNominal','minCash120','interest','rentNet','saleNet','peakDsr','peakDsrInfinite']},q,id+'/'+old_actions[acts]['id']+'/'+scenario)
        elif method=='reverse':
            for k in ['grid','affordablePrepay','breakEven','liquidation','payoff']:
                compare(x[k],y[k],id+'/'+k)
        else:compare(x,y,id)
        cases.append({'case':id,'method':method,'unexpectedDifferences':len(changes)-before})
    same_names=[c['check'] for c in old_report['checks']]==[c['check'] for c in new_report['checks']]
    same_math=ast_of_verify(OLD)==ast_of_verify(HERE)
    assert set(v1)==set(v2)==set(methods)
    result={'unchangedEconomicAssertionsFunctionAST':same_math,'same179CheckNamesAndOrder':same_names,'caseCount':len(cases),
            'originalCasesAndErrorStagesPreserved':len(changes)==0,'scope':'Every original monthly row field that was numeric, boolean or null; all old sampled policy/scenario paths matched by actions; old reverse thresholds and monetary outputs. Text and newly introduced diagnostics are outside the value comparison.',
            'totals':totals,'maximumAbsoluteNumericDifference':max_abs,'differences':changes,'cases':cases,
            'oldOutputSha256':old_report['uncompressedOutputSHA256'],'newOutputSha256':new_report['uncompressedOutputSHA256']}
    (HERE/'legacy_equivalence.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print({k:v for k,v in result.items() if k not in ['scope','cases','differences']});print('unexpected',changes[:8]);return 0 if same_math and same_names and not changes else 1

if __name__=='__main__':raise SystemExit(check())
