"""Compare one declared 24-fit reproduction with recovered follow-up artifacts."""
import argparse,hashlib,json
from pathlib import Path
import numpy as np

def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
p=argparse.ArgumentParser();p.add_argument('--followup-root',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
if a.output.exists():raise FileExistsError(a.output)
oldroot=a.followup_root/'thesis_extension/deepening/breadth';newroot=a.followup_root/'runs/20261008-refit'
rows=[]
for partition in ['sales','remaining','final_item']:
    for old in sorted((oldroot/partition).glob('*_seed*.json')):
        m=json.loads(old.read_text());new=newroot/old.name;n=json.loads(new.read_text())
        for key in ['task','seed','K','feature_names','params','best_iteration','q_exact','q_legacy','C_native','importance','metrics','support','partition_n']:
            assert m[key]==n[key],(old.name,key)
        op=old.parent/'cache'/f'{old.stem}.npz';npth=newroot/'cache'/f'{old.stem}.npz'
        with np.load(op,allow_pickle=False) as x,np.load(npth,allow_pickle=False) as y:
            assert set(x.files)==set(y.files)
            for key in x.files:assert np.array_equal(x[key],y[key]),(old.name,key)
            arrays=len(x.files)
        om=op.with_suffix('.model.txt');nm=npth.with_suffix('.model.txt')
        old_text, new_text = om.read_text(), nm.read_text()
        # Observed CPU-wheel serialization difference, not a numerical tolerance:
        # allow only omission of this exact empty GPU-list parameter line.
        old_gpu = old_text.count('[gpu_device_id_list: ]\n')
        new_gpu = new_text.count('[gpu_device_id_list: ]\n')
        assert old_text.replace('[gpu_device_id_list: ]\n','') == new_text.replace('[gpu_device_id_list: ]\n','')
        rows.append(dict(task=m['task'],seed=m['seed'],model_sha256=sha(nm),cache_sha256=sha(npth),metadata_sha256=sha(new),arrays_exactly_equal=arrays,model_bytes_exactly_equal=sha(om)==sha(nm),recovered_model_sha256=sha(om),empty_gpu_field_counts=[old_gpu,new_gpu],trees_and_other_parameters_exactly_equal=True,scientific_metadata_exactly_equal=True))
assert len(rows)==24
result=dict(scope='Fresh fixed-protocol refit of recovered follow-up panel; not original historical 50-seed reproduction',
 model_count=24,total_arrays_exactly_equal=sum(r['arrays_exactly_equal'] for r in rows),script_sha256=sha(Path(__file__)),
 training_script_sha256=sha(oldroot/'run_breadth.py'),all_scientific_results_exactly_equal=True,rows=rows)
a.output.write_text(json.dumps(result,indent=2)+'\n');print('24 fits: 528 arrays and scientific metadata exactly equal; model text differs only by recorded empty GPU field')
