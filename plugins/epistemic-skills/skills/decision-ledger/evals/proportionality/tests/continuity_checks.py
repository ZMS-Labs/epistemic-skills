"""Synthetic continuation and outcome records; not empirical agent runs."""
import copy
import json

def check(scorer,root):
    fixtures=json.loads((root/'continuity-fixtures.json').read_text())
    rows=json.loads((root/'examples/continuity-balanced.json').read_text())
    good=scorer.score(fixtures,rows)
    assert good['pass'],good
    for index,patch in [(0,{'asked_authority_again':True}),(0,{'task_complete':True}),(0,{'answer':'change API'}),(1,{'revision':'r1'}),(1,{'rechecked':['authority']}),(2,{'prediction':'two errors in ten runs'}),(2,{'standing_guidance':True}),(3,{'reanchored':False}),(3,{'claims_jsonl_validation':True})]:
        bad=copy.deepcopy(rows);bad[index].update(patch)
        assert not scorer.score(fixtures,bad)['pass'],patch
    print('Decision Ledger synthetic continuation/outcome checks: PASS')
