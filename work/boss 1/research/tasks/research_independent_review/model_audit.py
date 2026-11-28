"""Independently reconstruct historical labels, splits and metrics; never modify the study inputs."""
import csv
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.linalg import lstsq
from scipy.optimize import minimize
from scipy.special import expit, logit
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler
from threadpoolctl import threadpool_limits

HERE = Path(__file__).resolve().parent
W = HERE.parents[2]
ROOT = HERE.parents[4]
EXAMPLE = ROOT / "research/models/jst_example"
FILES = W / "compute/outputs"
ACTIVITY = W / "research/models/activity"


def read(file):
    return json.loads(file.read_text())


def sha(file):
    return hashlib.sha256(file.read_bytes()).hexdigest()


def measures(y, score, ids, cutoff):
    alarms = score > cutoff
    positives = y == 1
    negatives = ~positives
    positive_scores, negative_scores = score[positives], score[negatives]
    pairs = positive_scores[:, None] - negative_scores[None, :]
    # Pairwise concordance treats exact ties as half; group detections by actual country episode.
    observed = set(ids[positives])
    flag = set(ids[positives & alarms])
    return dict(rows=len(y), positives=int(positives.sum()), distinct_events=len(observed),
                detected=sorted(flag), missed=sorted(observed - flag),
                brier=float(np.average((y-score)**2)),
                auc=float(np.average((pairs > 0) + 0.5 * (pairs == 0))),
                false_alarms=int(alarms[negatives].sum()), negatives=int(negatives.sum()),
                false_alarm_share=float(alarms[negatives].mean()))


def read_candidate_trainings():
    rows = pd.read_csv(EXAMPLE / "panel.csv", dtype={"as_of": str, "horizon_end": str})
    meta = read(EXAMPLE / "experiment.json")
    raw = pd.read_stata(EXAMPLE / "JSTdatasetR6.dta", convert_categoricals=False)
    by_country = raw.set_index(["iso","year"]).sort_index()
    unknown, no_features, mismatch = [], [], []
    for row in rows.itertuples():
        t = int(row.as_of[:4])
        observations = by_country.loc[row.country]
        target = observations.loc[t+1:t+3,"crisisJST"]
        known_events = target.index[target.eq(1)].tolist()
        if target.isna().any() or len(target) != 3:
            unknown.append((row.country,t))
        if not known_events and row.event or known_events and row.event_id != f"{row.country}-{known_events[0]}":
            mismatch.append((row.country,t))
        if not any(pd.notna(getattr(row, f)) for f in meta["features"]):
            no_features.append((row.country,t))
    assert not mismatch
    train = (rows.as_of <= '1984-12-31') & (rows.horizon_end < '1985-01-01')
    cal = rows.as_of.between('1985-01-01','1999-12-31') & (rows.horizon_end < '2003-01-01')
    test = rows.as_of.between('2003-01-01','2016-12-31') & (rows.horizon_end <= '2020-12-31')
    bad = [(c,int(t[:4])) for c,t in zip(rows.country,rows.as_of)]
    bset, empty = set(unknown), set(no_features)
    clean = np.array([i not in bset and i not in empty for i in bad])
    splits = [rows.loc[train], rows.loc[cal], rows.loc[test]]
    eventsets = [set(q.loc[q.event.eq(1),"event_id"]) for q in splits]
    assert all(not (eventsets[i]&eventsets[j]) for i,j in [(0,1),(0,2),(1,2)])
    diagnostic = dict(source_rows=len(raw), source_onsets=int(raw.crisisJST.eq(1).sum()),
                      source_label_nas_by_country={str(k):int(v) for k,v in raw.crisisJST.isna().groupby(raw.iso).sum().items() if v},
                      unknown_label_rows=unknown, zero_observed_feature_rows=no_features,
                      reported_labels_disagreeing_with_an_observed_onset=mismatch,
                      original_split=[dict(rows=len(q),positive_rows=int(q.event.sum()),
                                           eligible_episodes=len(e),last_mature=q.horizon_end.max())
                                      for q,e in zip(splits,eventsets)])
    return meta, rows, splits, [rows.loc[mask & clean] for mask in (train,cal,test)], diagnostic


def fit_and_check(meta, blocks, original=None):
    train, cal, test = blocks
    feat = meta['features']
    out = {}
    for name in ['hist_gradient_boosting','logit']:
        impute = SimpleImputer(strategy='median').fit(train[feat])
        matrices = [impute.transform(part[feat]) for part in blocks]
        if name=='logit':
            scale = StandardScaler().fit(matrices[0])
            matrices = [scale.transform(v) for v in matrices]
            estimator = LogisticRegression(C=1, max_iter=500)
        else:
            estimator = HistGradientBoostingClassifier(max_iter=100, max_leaf_nodes=7, min_samples_leaf=20,
                                                        l2_regularization=1, random_state=20261126)
        estimator.fit(matrices[0], train.event)
        classes = list(estimator.classes_)
        event_column = classes.index(1)
        xcal, xtest = [estimator.predict_proba(m)[:,event_column] for m in matrices[1:]]
        lcal = logit(np.clip(xcal, 1e-8, 1-1e-8))
        ltest = logit(np.clip(xtest, 1e-8, 1-1e-8))
        # Use an independently written penalized binomial likelihood as a sign and optimum check.
        def nll(pair):
            a,b = pair
            z = a+b*lcal
            return np.logaddexp(0,z).sum()-np.dot(cal.event,z)+b*b/(2e6)
        opt = minimize(nll, [0,0], method='BFGS', options={'gtol':1e-6})
        calib = LogisticRegression(C=1e6,max_iter=500).fit(lcal[:,None],cal.event)
        cc = list(calib.classes_).index(1)
        s_cal = calib.predict_proba(lcal[:,None])[:,cc]
        s_test = calib.predict_proba(ltest[:,None])[:,cc]
        assert abs(opt.x[1]-calib.coef_[0,0]) < .002
        measured = {}
        for key,xcal0,xtest0 in [('raw',xcal,xtest),('calibrated',s_cal,s_test)]:
            # Higher quantile and strictly greater alert replicate the pre-declared budget.
            negatives = sorted(xcal0[cal.event.eq(0)])
            threshold = negatives[math.ceil(.9*(len(negatives)-1))]
            measured[key]=dict(threshold=float(threshold), **measures(test.event.to_numpy(), xtest0,
                                  test.event_id.fillna('').to_numpy(), threshold))
        match = None
        if original is not None:
            original_sub = [r for r in original['test_predictions'] if r['model']==name]
            assert [(r['country'],r['as_of'],r['event']) for r in original_sub] == list(zip(test.country,test.as_of,test.event))
            assert all(r['alarm'] == (r['score'] > measured['calibrated']['threshold']) for r in original_sub)
            match = max(float(np.max(np.abs(xtest-[r['raw_score'] for r in original_sub]))),
                        float(np.max(np.abs(s_test-[r['score'] for r in original_sub]))))
            assert match < 1e-10
        out[name]=dict(positive_class_column=event_column, estimator_classes=classes,
                       calibration_classes=list(calib.classes_),calibration_logit_slope=float(calib.coef_[0,0]),
                       calibration_logit_intercept=float(calib.intercept_[0]), independent_binomial_optimum=opt.x.tolist(),
                       calibration_raw_auc=float(roc_auc_score(cal.event,xcal)),
                       mean_raw_calibration_positive=float(xcal[cal.event.eq(1)].mean()),
                       mean_raw_calibration_negative=float(xcal[cal.event.eq(0)].mean()),
                       metrics=measured,max_absolute_error_vs_frozen_predictions=match)
    y=test.event.to_numpy()
    out['baseline']=measures(y,np.full(len(y),train.event.mean()),test.event_id.fillna('').to_numpy(),1.)
    return out


def gdps():
    audits={}
    for label,stem in [('long','long'),('single-vintage','same_vintage')]:
        panel=read(ACTIVITY / f'panel_{stem}.json')
        saved=read(next(FILES.glob(f'china-bridge-{label}-*.json')))['result']
        monthly=np.column_stack(list(panel['monthly'].values())).reshape(-1,3,2).mean(axis=1)
        design=np.column_stack([np.ones(len(monthly)),monthly])
        y=panel['quarterly_gdp']
        prediction_errors, lag_errors, max_error = [], [], 0.
        for i,r in enumerate(saved['predictions'],12):
            # Column-pivoted QR, independent of NumPy's SVD-based implementation.
            beta=lstsq(design[:i], y[:i], lapack_driver='gelsy')[0]
            p=float(np.dot(design[i],beta))
            assert r['quarter']==panel['quarterly_periods'][i] and y[i]==r['actual'] and y[i-1]==r['lag_baseline']
            max_error=max(max_error,abs(p-r['bridge']))
            prediction_errors.append(abs(y[i]-p));lag_errors.append(abs(y[i]-y[i-1]))
        assert max_error<1e-9
        audits[label]=dict(n=len(lag_errors), mae=float(np.mean(prediction_errors)), lag_mae=float(np.mean(lag_errors)),
                           common_quarters=len(lag_errors),max_error_vs_saved=max_error,
                           worst_quarter=saved['predictions'][np.argmax(prediction_errors)]['quarter'])
    old=pd.read_csv(W / 'research/data/gdp_quarterly_2022vintage.csv').set_index('quarter')
    new=pd.read_csv(W / 'research/data/gdp_quarterly_2026vintage.csv').set_index('quarter')
    q=old.index.intersection(new.index)
    audits['2021_revision_points']=(new.loc[q,'real_gdp_yoy']-old.loc[q,'real_gdp_yoy']).to_dict()
    saved=read(next(FILES.glob('china-nowcast-diagnostic-*')))['result']
    actual=float(new.loc['2026Q3','real_gdp_yoy'])
    audits['dfm']=dict(old=saved['previous_estimate'],new=saved['updated_estimate'],target=actual,
                       difference=saved['updated_estimate']-actual,
                       news_identity=saved['updated_estimate']-saved['previous_estimate']-saved['news_impact'])
    return audits


def native(v):
    if isinstance(v,np.generic):
        return v.item()
    raise TypeError(type(v))


if __name__=='__main__':
    meta, rows, original, filtered, diagnostic=read_candidate_trainings()
    saved=read(next(FILES.glob('historical-warning-v1-*')))['result']
    repaired_dir=W/'research/models/jst_audited_20261127'
    current=read(next(FILES.glob('historical-warning-audit-v2-*')))['result']
    repaired_manifest=read(repaired_dir/'data_manifest.json')
    original_unknown=set(diagnostic['unknown_label_rows'])
    original_empty=set(diagnostic['zero_observed_feature_rows'])-original_unknown
    supplied=repaired_manifest['audit_exclusions']
    assert {(r['country'],r['year']) for r in supplied if r['reason']=='unobserved_or_invalid_crisis_label'}==original_unknown
    assert {(r['country'],r['year']) for r in supplied if r['reason']=='all_predictors_unobserved'}==original_empty
    original_keys=list(zip(rows.country, rows.as_of))
    removed={(c,f'{t}-12-31') for c,t in original_unknown|original_empty}
    prepared=pd.read_csv(repaired_dir/'panel.csv')
    pd.testing.assert_frame_equal(rows.iloc[[i for i,k in enumerate(original_keys) if k not in removed]].reset_index(drop=True),prepared)
    assert current['data_sha256']==sha(repaired_dir/'panel.csv')
    with threadpool_limits(limits=2):
        results=dict(labels=diagnostic,original=fit_and_check(meta,original,saved),
                     corrected_sensitivity=fit_and_check(meta,filtered,current),corrected_split_rows=[len(x) for x in filtered],
                     repaired_panel_sha256=sha(repaired_dir/'panel.csv'),
                     verified_prep_code_sha256=sha(ROOT/'tools/prepare_jst_example.py'),
                     excluded_zero_feature_only=sorted(original_empty),
                     china_activity=gdps(), design='Re-estimation after a data-quality finding. No fresh test set or China probability.')
    (HERE/'independent_models.json').write_text(json.dumps(results,ensure_ascii=False,indent=2,default=native)+'\n')
