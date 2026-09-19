"""Synthetic relay closure responses, not a published external exchange."""
import copy
import json

def check(scorer, root):
    fixtures=json.loads((root/'completion-fixtures.json').read_text())
    rows=json.loads((root/'examples/completion-balanced.json').read_text())
    assert scorer.score(fixtures,rows)['pass']
    for patch in [{'prompt_emitted':True},{'outbound_created':True},{'caller_task_complete':True}, {'open_requirements':['OUT-001']},{'relay_closed':False},{'relay_verified':False},{'caller_next_action':'NONE'}]:
        bad=copy.deepcopy(rows);bad[0].update(patch)
        assert not scorer.score(fixtures,bad)['pass'], patch
    print('outsource synthetic terminal return: PASS')
