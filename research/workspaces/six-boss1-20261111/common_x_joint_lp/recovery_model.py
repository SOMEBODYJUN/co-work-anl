"""Standard-library exact-recovery utilities; no numerical solver imports."""
from datetime import datetime, timezone
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from pathlib import Path
import ast
import gzip
import json
import math
import struct
import zipfile

HERE = Path(__file__).resolve().parent
ORIGINAL, AUX_END, SHARED_END, X_END, TOTAL = 4849, 15593, 20585, 20601, 21021


def digest(path): return sha256(path.read_bytes()).hexdigest()


def read(path):
    with gzip.open(path, 'rt', encoding='utf-8') if path.suffix == '.gz' else path.open() as f:
        return json.load(f)


def write(name, value):
    p = HERE / name; assert not p.exists(), ('refuse_overwrite', str(p))
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def log(event, **fields):
    line = json.dumps({'event': event, 'utc': datetime.now(timezone.utc).isoformat(), **fields}, ensure_ascii=False)
    print(line, flush=True)
    with (HERE / 'progress.jsonl').open('a') as f: f.write(line + '\n')


@lru_cache(maxsize=None)
def frac(v): return F(v)


def dot(row, x): return sum((frac(v)*x[j] for j, v in row if x[j]), F())


def load_npz(path, names=None):
    """Decode the small, plain scalar/vector NPY arrays using stdlib only.

    Refuse object, structured, multidimensional, or Fortran arrays. The exact
    arithmetic below never calls NumPy, SciPy, or any optimizer.
    """
    values = {}; shapes = {}; wanted = None if names is None else set(names)
    with zipfile.ZipFile(path) as archive:
        members = archive.namelist(); assert len(members) == len(set(members))
        for member in members:
            assert member.endswith('.npy') and '/' not in member
            if wanted is not None and member[:-4] not in wanted: continue
            raw = archive.read(member); assert raw[:6] == b'\x93NUMPY'
            version = tuple(raw[6:8]); assert version in ((1, 0), (2, 0), (3, 0))
            size = 2 if version == (1, 0) else 4
            header_size = int.from_bytes(raw[8:8+size], 'little'); start = 8+size+header_size
            header = ast.literal_eval(raw[8+size:start].decode('utf-8' if version == (3, 0) else 'latin1').strip())
            assert header['fortran_order'] is False and len(header['shape']) <= 1
            dtype = header['descr']; assert isinstance(dtype, str) and dtype[0] in ('<', '>', '|', '=')
            kind = dtype[1]; width = int(dtype[2:]); count = math.prod(header['shape'])
            body = raw[start:]; endian = '>' if dtype[0] == '>' else '<'
            if kind == 'U':
                assert len(body) == count * width * 4
                vector = [body[i*width*4:(i+1)*width*4].decode('utf-32-be' if endian == '>' else 'utf-32-le').rstrip('\x00') for i in range(count)]
            elif kind == 'S':
                assert len(body) == count * width
                vector = [body[i*width:(i+1)*width].rstrip(b'\x00').decode('ascii') for i in range(count)]
            else:
                fmt = {('f', 8): 'd', ('f', 4): 'f', ('i', 8): 'q', ('i', 4): 'i', ('i', 2): 'h',
                       ('i', 1): 'b', ('u', 8): 'Q', ('u', 4): 'I', ('u', 2): 'H', ('u', 1): 'B', ('b', 1): '?'}
                assert (kind, width) in fmt and len(body) == count * width, dtype
                vector = [t[0] for t in struct.iter_unpack(endian + fmt[kind, width], body)]
            key = member[:-4]; assert key not in values
            values[key] = vector; shapes[key] = tuple(header['shape'])
    if wanted is not None: assert set(values) == wanted
    return values, shapes
