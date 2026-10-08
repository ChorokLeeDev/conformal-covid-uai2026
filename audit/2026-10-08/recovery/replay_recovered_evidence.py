#!/usr/bin/env python3
"""Read-only recovery verification, not historical model reconstruction.

Requires the owner's private continuation checkout and verified release payload.
Writes only aggregate diagnostics; no row-level private data leave that checkout.
Uses the independent public APS reference. No fitting or hyperparameter search.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
import lightgbm as lgb
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
import yaml
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'src'))
from aps_reference import all_scores


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def metrics(p, y, q, rule):
    score = all_scores(p)
    if rule == 'inclusive':
        sets = score <= q
    else:
        order = np.argsort(-p, axis=1, kind='stable')
        cumulative = np.minimum(np.take_along_axis(p, order, axis=1).cumsum(1), 1.)
        count = np.minimum((cumulative < q).sum(1) + 1, p.shape[1])
        sets = np.zeros(p.shape, dtype=bool)
        np.put_along_axis(sets, order, np.arange(p.shape[1])[None, :] < count[:, None], axis=1)
    known = y >= 0
    hits = np.zeros(len(y), dtype=bool)
    hits[known] = sets[np.flatnonzero(known), y[known]]
    return dict(n=len(y), covered=int(hits.sum()), coverage=float(hits.mean()),
                mean_size=float(sets.sum(1).mean()), unknown=int((~known).sum()))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--followup-root', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    root = args.followup_root / 'thesis_extension'
    data = root / 'external_inputs/rel-salt'
    breadth = root / 'deepening/breadth'
    manifest = yaml.safe_load((data / 'manifest.yaml').read_text())
    entities = {t: pd.read_parquet(data / 'db' / f'{t}.parquet') for t in ['salesdocument', 'salesdocumentitem']}
    joins, inputs, rows, inference = [], [], [], []
    for file in sorted(data.rglob('*.parquet')):
        inputs.append(dict(path=str(file.relative_to(root)), sha256=sha(file)))
    for folder in ['sales', 'remaining', 'final_item']:
        for meta_path in sorted((breadth / folder).glob('*_seed*.json')):
            m = json.loads(meta_path.read_text())
            task, seed = m['task'], m['seed']
            task_dir = data / 'tasks' / task
            spec = yaml.safe_load((task_dir / 'manifest.yaml').read_text())
            entity = entities[spec['entity_table']]
            key = manifest['tables'][spec['entity_table']]['pkey']
            target = spec['target_col']
            if seed == 42:
                full_ids = set(entity[key])
                cut_ids = set(entity.loc[entity.CREATIONTIMESTAMP <= pd.Timestamp(manifest['test_timestamp']), key])
                for split in ['train', 'val', 'test']:
                    labels = pd.read_parquet(task_dir / f'{split}.parquet')
                    joins.append(dict(task=task, split=split, n=len(labels),
                        truncated_missing=int((~labels[key].isin(cut_ids)).sum()),
                        full_missing=int((~labels[key].isin(full_ids)).sum())))
            cache = meta_path.parent / 'cache' / (meta_path.stem + '.npz')
            model_path = cache.with_suffix('.model.txt')
            assert sha(cache) == m['cache_sha256'] and sha(model_path) == m['model_sha256']
            inputs += [dict(path=str(p.relative_to(root)), sha256=sha(p)) for p in [meta_path, cache, model_path]]
            with np.load(cache, allow_pickle=False) as z:
                features = list(z['features'])
                assert features == m['feature_names'] and target not in features
                forbidden = {c for t, c in spec['remove_columns'] if t == spec['entity_table']}
                assert not forbidden.intersection(features)
                # Rebuild train-only dictionaries from frozen IDs, independently
                # of the producer's random sampling and preprocessing functions.
                frame = entity.set_index(key, drop=False)
                train = frame.loc[z['ids_train'], features]
                maps = {c: {v: i for i, v in enumerate(sorted(train[c].fillna('__MISSING__').astype(str).unique()))}
                        for c in features if not pd.api.types.is_numeric_dtype(train[c])}
                def encode(split):
                    f = frame.loc[z[f'ids_{split}'], features].copy()
                    for c, mapping in maps.items():
                        f[c] = f[c].fillna('__MISSING__').astype(str).map(mapping).fillna(-1)
                    for c in features:
                        f[c] = pd.to_numeric(f[c], errors='coerce').fillna(-999)
                    return f.to_numpy(dtype=np.float32)
                model = lgb.Booster(model_file=str(model_path))
                inference_row = dict(task=task, seed=seed, prediction_max_absolute_error={})
                for split in ['cal', 'audit', 'test']:
                    pred = model.predict(encode(split), num_threads=2)
                    inference_row['prediction_max_absolute_error'][split] = float(np.abs(pred-z[f'probs_{split}']).max())
                    if not np.allclose(pred, z[f'probs_{split}'], rtol=0, atol=1e-12):
                        raise AssertionError(f'{task}/{seed}/{split} frozen model probabilities differ')
                phi = np.asarray(model.predict(encode('cal')[:128], pred_contrib=True, num_threads=2))
                phi = phi.reshape(128, len(z['class_labels']), len(features)+1)
                imp = abs(phi[:, :, :-1]).mean(axis=(0, 1))
                concentration = float(imp.max()/imp.sum())
                inference_row['concentration_recomputed'] = concentration
                inference_row['concentration_absolute_error'] = abs(concentration-m['C_native'])
                assert inference_row['concentration_absolute_error'] < 1e-12
                inference.append(inference_row)
                pc, yc = z['probs_cal'], z['y_cal']
                scores = np.full(len(yc), np.inf)
                known = yc >= 0
                scores[known] = all_scores(pc)[np.flatnonzero(known), yc[known]]
                k = math.ceil((len(yc)+1)*.9)
                q = float(np.sort(scores)[k-1]) if k <= len(yc) else math.inf
                assert q == m['q_exact']
                for rule in ['inclusive', 'crossing']:
                    measures = {s: metrics(z[f'probs_{s}'], z[f'y_{s}'], q, rule) for s in ['audit', 'test']}
                    rows.append(dict(task=task, seed=seed, rule=rule, C=concentration, q=q,
                        metrics=measures, drop_pp=100*(measures['audit']['coverage']-measures['test']['coverage'])))
            print(task, seed, 'verified', flush=True)
    assert len(inference) == 24 and len(joins) == 24
    means = []
    for task in sorted({r['task'] for r in rows}):
        for rule in ['inclusive', 'crossing']:
            subset = [r for r in rows if r['task']==task and r['rule']==rule]
            assert len(subset)==3
            means.append(dict(task=task, rule=rule, C=float(np.mean([r['C'] for r in subset])),
                drop_pp=float(np.mean([r['drop_pp'] for r in subset]))))
    associations = []
    for rule in ['inclusive', 'crossing']:
        subset=[r for r in means if r['rule']==rule]
        result=spearmanr([r['C'] for r in subset], [r['drop_pp'] for r in subset])
        associations.append(dict(rule=rule,n_tasks=len(subset),rho=float(result.statistic),p_asymptotic=float(result.pvalue)))
    result=dict(scope='Recovered follow-up models, not original historical 50-seed reconstruction; no models refitted',
        assumptions='Chronological splits do not establish exchangeability; shared-domain tasks and seeds are not independent replication; nominal p-values descriptive',
        source_revision='e2eb3e38f072745f0f60bd67425cffbd68f7ab9e',
        archive_sha256='d31e4522bf8050d1447547c1ae58eb4da582600f764a24f40f6a95da2d963559',
        script_sha256=sha(__file__),lightgbm=lgb.__version__,numpy=np.__version__,
        input_hashes=inputs,join_audit=joins,frozen_model_inference=inference,
        model_metrics=rows,task_means=means,associations=associations)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps(associations), flush=True)

if __name__=='__main__':
    main()
