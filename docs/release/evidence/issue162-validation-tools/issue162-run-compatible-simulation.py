"""Legacy regression harness: simulate compatible witnesses; retain real gates.
Not native filesystem qualification. Subprocesses inherit the same injection.
"""
import os
from pathlib import Path
import subprocess
import sys
import tempfile

root = Path(sys.argv[1]).resolve()
with tempfile.TemporaryDirectory(prefix='identity-simulation-') as td:
    Path(td, 'sitecustomize.py').write_text('''import sys
sys.path.insert(0, ''' + repr(str(root)) + ''')
import custody_identity
def simulated_compatible(fd, prefix, owned, comparator):
    return "NO_MISMATCH_OBSERVED"
custody_identity._measure_pairs = simulated_compatible
''')
    env = dict(os.environ, PYTHONPATH=td + os.pathsep + str(root))
    result = subprocess.run([sys.executable, str(root / sys.argv[2]), *sys.argv[3:]], env=env)
    sys.exit(result.returncode)
