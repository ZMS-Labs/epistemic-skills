"""Synthetic trace/scorer polarity only; no native goal is activated."""
import copy
import json

def check(scorer, root):
    fixtures=json.loads((root/'adapter-fixtures.json').read_text(encoding='utf-8'))
    rows=json.loads((root/'examples/adapter-balanced.json').read_text(encoding='utf-8'))
    payload="A"+chr(0x1F680)
    assert len(payload)==2
    assert len(payload.encode('utf-16-le'))//2==3
    assert len(payload.encode('utf-8'))==5
    good=scorer.score_adapter(fixtures, rows)
    assert good['pass'], good
    def reject(fid, mutate, change_fixture=None):
        f=copy.deepcopy(next(f for f in fixtures if f['id']==fid))
        r=copy.deepcopy(next(r for r in rows if r['id']==fid))
        mutate(r)
        if change_fixture: change_fixture(f)
        report=scorer.score_adapter([f],[r])
        assert not report['pass'], (fid, r)
    for f in fixtures[:6]:
        reject(f['id'],lambda r:None,lambda f:f['profile'].update(limit=f['profile']['limit']-1))
    reject('ambiguous-submission',lambda r:r['events'].insert(2,copy.deepcopy(r['events'][1])))
    reject('stored-truncation',lambda r:r.update(result='active'))
    reject('omitted-optional-budget',lambda r:r['events'][1]['payload'].update(token_budget=100))
    reject('stale-profile',lambda r:r.update(profile_version='synthetic-0'))
    reject('separate-completion',lambda r:r['events'][1]['payload'].pop('completion'))
    for fid in ['draft-only','existing-active','inaccessible-reference','resume-reference-inaccessible','unsupported-persistence']:
        reject(fid,lambda r:r['events'].append({'op':'submit','payload':{'objective':'invented'},'result':'accepted'}))
    reject('acknowledgment-only',lambda r:r.update(verification='readback'))
    reject('validation-rejection',lambda r:r['events'][2]['payload'].update(objective='weaker goal'))
    reject('utf8-field',lambda r:r['events'][2].update(stored={'objective':'A'}))
    reject('escaped-prefix-wrapper',lambda r:None,lambda f:f['profile'].update(limit=f['profile']['limit']-1))
    reject('documented-newline-normalization',lambda r:r['events'][2]['stored'].update(completion='weaker proof'))
    print('write-goal synthetic adapter profiles: PASS (no native-host evidence)')
