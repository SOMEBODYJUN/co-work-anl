"""Local exact-recovery utilities; deliberately contains no optimizer import."""
from datetime import datetime, timezone
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from pathlib import Path
import gzip
import json

HERE = Path(__file__).resolve().parent
ORIGINAL, M, N, NEWM, NEWN = 4849, 19662, 15593, 2635, 5428
CORE_END, OLD_COLUMNS, TOTAL = 20601, 20585, 21021


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def read(path):
    if path.suffix == '.gz':
        with gzip.open(path, 'rt', encoding='utf-8') as f:
            return json.load(f)
    return json.loads(path.read_text())


def write(name, value):
    p = HERE / name
    assert not p.exists(), ('refuse_overwrite', str(p))
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def log(event, **fields):
    line = json.dumps({'event': event, 'utc': datetime.now(timezone.utc).isoformat(), **fields}, ensure_ascii=False)
    print(line, flush=True)
    with (HERE / 'progress.jsonl').open('a') as f:
        f.write(line + '\n')


@lru_cache(maxsize=None)
def frac(value):
    return F(value)


def dot(encoded, values):
    return sum((frac(v) * values[j] for j, v in encoded if values[j]), F())
