"""Frozen within-word Tamil-order negative control; no Indus inference."""
from pathlib import Path
import importlib.util
import json
import hashlib
import time
import collections
import signal
import numpy as np

P = Path(__file__).resolve().parent
ROOT = P.parents[1]
OLD = ROOT / 'round15' / 'cipher'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    start = time.monotonic()
    def timeout(*args):
        raise TimeoutError('Prespecified 180-second runtime cap exceeded')
    signal.signal(signal.SIGALRM, timeout)
    signal.alarm(180)
    spec = importlib.util.spec_from_file_location('frozen_round15', OLD / 'benchmark.py')
    old = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(old)
    inputs = json.loads((OLD / 'solver_inputs.json').read_text())
    alphabet = inputs['candidate_inventory']
    ix = {s:i for i,s in enumerate(alphabet)}
    K = len(alphabet)
    ct = [tuple(int(c[1:]) for c in w) for w in inputs['cipher_training']]
    original = [tuple(ix[s] for s in w) for w in inputs['unaligned_references']['Tamil_positive_control']]
    refs = {'Tamil_original': original}
    for seed in range(20001,20006):
        rng = np.random.default_rng(seed)
        refs[f'Tamil_shuffled_{seed}'] = [tuple(int(s) for s in rng.permutation(w)) for w in original]
    counts = collections.Counter(s for w in original for s in w)
    for ref in refs.values():
        assert list(map(len,ref)) == list(map(len,original))
        assert collections.Counter(s for w in ref for s in w) == counts
    # Persist concrete solver inputs and protocol hash before any fitting.
    input_record = dict(protocol_sha256=sha(P/'protocol.md'),
        original_solver_inputs_sha256=sha(OLD/'solver_inputs.json'),
        original_solver_code_sha256=sha(OLD/'benchmark.py'),
        candidate_inventory=alphabet,cipher_training=inputs['cipher_training'],
        references={label:[[alphabet[s] for s in w] for w in ref] for label,ref in refs.items()},
        solver_seed=15104,shuffle_seeds=list(range(20001,20006)),config=old.CONFIG)
    (P/'solver-inputs.json').write_text(json.dumps(input_record,indent=2))
    fits = {}
    for label,ref in refs.items():
        fits[label] = old.solve(ct,ref,K,15104)
    fitting_done = time.monotonic()-start
    # Explicit evaluation barrier: answers first read here, after all six fits.
    answers = json.loads((OLD/'evaluation_answers.json').read_text())
    inv = np.array([ix[answers['key'][f'C{i:03}']] for i in range(K)])
    ce = [tuple(int(c[1:]) for c in w) for w in answers['heldout_cipher']]
    plain = [tuple(ix[s] for s in w) for w in answers['heldout_plaintext']]
    out = dict(protocol_sha256=input_record['protocol_sha256'],
        solver_inputs_sha256=sha(P/'solver-inputs.json'),
        evaluation_answers_sha256=sha(OLD/'evaluation_answers.json'),
        fit_finished_before_answers_loaded=True,
        fitting_seconds=fitting_done,conditions={})
    for label,f in fits.items():
        ref=refs[label]
        out['conditions'][label]=dict(
            reference_words=len(ref),reference_distinct_words=len(set(ref)),
            words_unchanged_from_original=sum(a==b for a,b in zip(original,ref)),
            heldout_plaintext_strings_present=sum(w in set(ref) for w in plain),
            evaluations={name:old.evaluate(f[name],inv,ct,ce,plain)
                         for name in ['recovered','frequency','random_best_score']},
            trace=f['trace'],training_score=f['training_score'],
            runtime_seconds=f['runtime_seconds'],
            recovered_mapping={f'C{i:03}':alphabet[int(f['recovered'][i])] for i in range(K)})
    out['total_seconds']=time.monotonic()-start
    signal.alarm(0)
    (P/'results.json').write_text(json.dumps(out,indent=2,default=lambda x:x.item()))
    for label,row in out['conditions'].items():
        e=row['evaluations']['recovered']
        print(label,e['heldout_exact_words'],e['heldout_correct_tokens'],e['training_seen_key_correct'],
              'unchanged',row['words_unchanged_from_original'],'teststrings',row['heldout_plaintext_strings_present'])
    print('seconds',out['total_seconds'])

if __name__=='__main__':
    main()
