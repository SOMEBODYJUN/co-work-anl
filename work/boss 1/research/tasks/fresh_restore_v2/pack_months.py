"""Pack full JS ledger vectors losslessly. Run from the clone root in the locked venv."""
from array import array
import gzip
import hashlib
import json
from pathlib import Path
import struct
import numpy as np

BASE = Path('.fresh-v2')
SOURCE = BASE / 'monthly_replay.jsonl.gz'
TARGET = BASE / 'monthly_ledgers.npz'
NULL = 0x7ff8000000000001
FALSE = 0x7ff8000000000002
TRUE = 0x7ff8000000000003


def encode(value):
    if value is None:
        return NULL
    if value is False:
        return FALSE
    if value is True:
        return TRUE
    return struct.unpack('<Q',struct.pack('<d',value))[0]


def decode(value):
    v = int(value)
    if v == NULL:
        return None
    if v == FALSE:
        return False
    if v == TRUE:
        return True
    return struct.unpack('<d',struct.pack('<Q',v))[0]


def main():
    trajectories, pairs, offset = {}, [], 0
    fields, columns = [], []
    with gzip.open(SOURCE,'rt') as f:
        for line in f:
            record = json.loads(line)
            if record['type']=='schema':
                fields = record['fields']
                columns = [array('Q') for _ in fields]
            elif record['type']=='trajectory':
                rows = record['rows']
                trajectories[record['id']] = [offset,len(rows)]
                for row in rows:
                    assert len(row)==len(fields)
                    for c, value in zip(columns,row):
                        c.append(encode(value))
                offset += len(rows)
            elif record['type']=='pair':
                pairs.append([record['rule'],record['scenario'],record['old'],record['new']])
    metadata = {'format':'household-ledgers.v1','fields':fields,'unique_trajectories_start_and_length':trajectories,
                'pair_columns':['strategy','scenario','old_trajectory','new_trajectory'],'pairs':pairs,
                'decode':'For zero-based field i use uint64 values = k{i}[v{i}]. Slice the trajectory by [start,start+length). Non-sentinel entries are IEEE-754 binary64 bit patterns.',
                'null_uint64':str(NULL),'false_uint64':str(FALSE),'true_uint64':str(TRUE)}
    payload = {'metadata':np.frombuffer(json.dumps(metadata,ensure_ascii=False,separators=(',',':')).encode(),dtype=np.uint8)}
    for i,c in enumerate(columns):
        keys, inverse = np.unique(np.asarray(c,dtype=np.uint64),return_inverse=True)
        payload['k'+str(i)] = keys
        dtype = np.uint8 if len(keys)<=256 else np.uint16 if len(keys)<=65536 else np.uint32
        payload['v'+str(i)] = inverse.astype(dtype)
    np.savez_compressed(TARGET,**payload)
    with np.load(TARGET,allow_pickle=False) as pack:
        assert json.loads(pack['metadata'].tobytes()) == metadata
        for i,c in enumerate(columns):
            recovered = pack[f'k{i}'][pack[f'v{i}']]
            assert np.array_equal(recovered,np.asarray(c,dtype=np.uint64))
    # Prove value/type equality to the original input, independently of numerical string formatting.
    with gzip.open(SOURCE,'rt') as f:
        for line in f:
            item = json.loads(line)
            if item['type']!='trajectory':
                continue
            start,count=trajectories[item['id']]
            assert len(item['rows'])==count
            for j,row in enumerate(item['rows']):
                for i,value in enumerate(row):
                    got=decode(columns[i][start+j])
                    if value is None or isinstance(value,bool):
                        assert got is value
                    else:
                        assert encode(got) == encode(value)
    print(json.dumps({'full_fields':len(fields),'matched_pairs':len(pairs),'unique_unrounded_trajectories':len(trajectories),
                      'unique_trajectory_months_stored':offset,'sha256':hashlib.sha256(TARGET.read_bytes()).hexdigest(),
                      'bytes':TARGET.stat().st_size,'round_trip_all_values_and_types':True},indent=2))


if __name__=='__main__':
    main()
