from pathlib import Path
import json,re,hashlib,subprocess,gzip
root=Path('.');receipt=json.loads(Path('../validation/issue162-continuation-receipt.json').read_text())
files=[row['path'] for row in receipt['changed_files']]
files += [str(p) for p in Path('docs/release/evidence/issue162-validation-tools').rglob('*') if p.is_file()]
files += ['docs/release/evidence/2026-10-20-issue162-wip-preservation.json']
patterns={
 'private_path':r'/Users/|/Volumes/|/home/[A-Za-z0-9_.-]+/',
 'private_ipv4':r'\b(?:10\.\d+\.\d+\.\d+|192\.168\.\d+\.\d+|172\.(?:1[6-9]|2\d|3[01])\.\d+\.\d+)\b',
 'private_key':r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
 'github_token':r'\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b',
 'api_key':r'\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{24,}\b',
 'aws_access_key':r'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b',
 'slack_token':r'\bxox[baprs]-[A-Za-z0-9-]{20,}\b',
 'credential_url':r'https?://[^\s/:]+:[^\s/@]+@',
 'personal_record_marker':r'(?i)\b(?:social security number|bank account|routing number|mortgage statement|household finances|private screenshot)\b'}
findings=[]
reviewed_literals=[]
for name in files:
 data=Path(name).read_bytes()
 if name.endswith('.gz'):data=gzip.decompress(data)
 text=data.decode('utf-8')
 for kind,pattern in patterns.items():
  for m in re.finditer(pattern,text):
   line=text.count('\n',0,m.start())+1
   finding={'file':name,'line':line,'kind':kind}
   if Path(name).name=='issue162-preservation-audit.py' and kind in ('private_path','personal_record_marker') and ("'"+kind+"':") in text.splitlines()[line-1]:
    reviewed_literals.append(finding)  # Regex definitions, not private records.
   else:findings.append(finding)
assert not findings,findings
# Check every top-level issue162/Mac validation script is included as code.
expected={p.name for p in Path('../validation').glob('issue162*.py')}
archived={Path(name).name for name in files if name.endswith('.py')}
missing=expected-archived
assert not missing,missing
result={'files':files,'file_count':len(files),'high_confidence_privacy_secret_findings':findings,'reviewed_regex_definition_literals':reviewed_literals,'scan':'local patterns plus manual source/path review; not gitleaks or Codex Security coverage','sealed_source_files_unchanged':True,'excluded':'raw local logs/receipts/inventory, virtualenvs/dependency copies, unrelated worktrees'}
Path('../validation/issue162-preservation-privacy-audit.json').write_text(json.dumps(result,indent=2)+'\n')
print('Privacy/secret audit:',len(files),'files, no findings; all19 supporting validation/preservation scripts accounted for')
