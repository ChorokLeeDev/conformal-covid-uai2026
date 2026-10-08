"""Recheck recovered public source and rounded summaries without model fitting."""
import ast, hashlib, json, re, warnings, zipfile
from pathlib import Path
import numpy as np
from scipy.stats import spearmanr
ROOT=Path(__file__).resolve().parent
with zipfile.ZipFile(ROOT/'recovered-upstream-source.zip') as z:
    source=z.read('papers/conformal_covid/code/run_mmd_c2st_comparison.py').decode()
node=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name=='compute_psi_single_feature')
namespace={'np':np}
exec(compile(ast.Module(body=[node],type_ignores=[]),'recovered_PSI_function','exec'),namespace)
psi=namespace['compute_psi_single_feature']
psi_cases={'nonoverlapping_uniform_support':float(psi(np.linspace(0,1,1000),np.linspace(2,3,1000))),
           'constant_binary_change':float(psi(np.zeros(1000),np.ones(1000)))}
assert all(abs(v)<1e-12 for v in psi_cases.values())
logs={}
for freq in ['none','3M']:
    text=(ROOT/'retraining-logs'/f'retrain_{freq}_sales-shipcond.txt').read_text()
    rows=re.findall(r'Month \d+/\d+: (\d{4}-\d\d) \((\d+) samples\).*?Coverage: ([\d.]+)%',text,re.S)
    assert len(rows)==11
    logs[freq]=[{'month':m,'n':int(n),'coverage_pct':float(c)} for m,n,c in rows]
assert [r['month'] for r in logs['none']]==[r['month'] for r in logs['3M']]
diffs=np.array([a['coverage_pct']-b['coverage_pct'] for a,b in zip(logs['3M'],logs['none'])])
points=json.loads((ROOT/'manuscript_claims_snapshot.json').read_text())['multiclass_n16']['tasks']
bootstrap=[]
for label,pts in [('SALT8',[p for p in points if p['dataset']=='rel-salt']),('primary16',points)]:
    a=np.array([p['concentration_pct'] for p in pts]);b=np.array([p['coverage_drop_pp'] for p in pts])
    rng=np.random.default_rng(42); vals=[]
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        for _ in range(10000):
            idx=rng.integers(0,len(pts),len(pts));rho=spearmanr(a[idx],b[idx]).statistic
            if np.isfinite(rho): vals.append(float(rho))
    bootstrap.append({'subset':label,'rho':float(spearmanr(a,b).statistic),'seed':42,
         'requested_resamples':10000,'defined_resamples':len(vals),'percentile_95ci':np.percentile(vals,[2.5,97.5]).tolist(),
         'scope':'Conditional task-bootstrap arithmetic on rounded summaries; task exchangeability/dependence not justified'})
result={'source_sha256':hashlib.sha256(source.encode()).hexdigest(),'psi_counterexamples':psi_cases,
 'lipschitz_counterexample':{'score':'s(x)=0.5+x, threshold=0.5, fixed true label','source_x':-.001,'target_x':.001,'score_L':1,'joint_W2':.002,'source_coverage':1,'target_coverage':0,'claimed_lower_bound':.998,'violation':True},
 'retraining':{'source':'rounded seed42 monthly logs, no original per-row predictions','monthly_rows':logs,'eleven_month_equal_weight_improvement_pp':float(diffs.mean()),'july_december_equal_weight_improvement_pp':float(diffs[5:].mean()),'inference':'No independent-month or task assumption established; no p-value newly claimed'},
 'bootstrap':bootstrap}
(ROOT/'source-summary-recheck.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='retraining'},indent=2))
