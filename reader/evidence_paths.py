"""Keep the current release checks separate from the accepted six-paper reports."""
import hashlib
from pathlib import Path

WORK = Path(__file__).resolve().parent
EVIDENCE = WORK / 'evidence' / 'twelve-paper-20261001'
EVIDENCE.mkdir(parents=True, exist_ok=True)

def input_hashes(*paths):
    """Bind a check to the actual project inputs and implementation it consumed."""
    root=WORK.parent
    return {Path(path).resolve().relative_to(root).as_posix():hashlib.sha256(Path(path).read_bytes()).hexdigest() for path in paths}
