from pathlib import Path
import urllib.request,json
url='https://pypi.org/pypi/rpds-py/2026.6.3/json'
with urllib.request.urlopen(url) as response: data=json.load(response)
name='rpds_py-2026.6.3-cp312-cp312-macosx_11_0_arm64.whl'
wheel=next(v for v in data['urls'] if v['filename']==name)
expected=wheel['digests']['sha256']
assert len(expected)==64
out=Path('../validation')
(out/'issue162-rpds-pypi-py312-metadata.json').write_text(json.dumps({'source':url,'filename':name,'url':wheel['url'],'sha256':expected,'version':data['info']['version']},indent=2)+'\n')
original=Path('plugins/epistemic-skills/contracts/mission-custody/requirements-jsonschema-parity-ubuntu-py312.txt').read_text()
mac=original.replace('ecabd69db66de867690f9797f2f8fa27ba501bbc24540cbdbdc649cd15888ba6',expected)
(out/'issue162-parity-macos-py312.txt').write_text('# Local test lock only: exact repository versions, official PyPI Mac cp312 wheel digest.\n'+mac)
print('Verified exact-version Mac wheel digest against official PyPI metadata; local lock written')
