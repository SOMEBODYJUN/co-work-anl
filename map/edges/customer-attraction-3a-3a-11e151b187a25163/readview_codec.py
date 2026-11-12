"""Lossless JSON reading codec; no model, scalar, certificate or solver import.

The view exposes every scalar value. It replaces repeated rational denominators
with one gcd and a factor dictionary, repeated complete slack values with an
ordered value dictionary, and consecutive slack keys with an exact prefix length
plus literal suffix. A decoder reconstructs every original JSON field/value.
"""
import json
import math
import hashlib
from pathlib import Path
from functools import reduce

def encode(source):
    denominators = list(dict.fromkeys(v.split('/')[1] for v in source['slacks'].values() if '/' in v))
    common = reduce(math.gcd, map(int, denominators))
    values = list(dict.fromkeys(source['slacks'].values()))
    encoded_values = []
    for value in values:
        if '/' in value:
            numerator, denominator = value.split('/')
            encoded_values.append([numerator, denominators.index(denominator)])
        else:
            encoded_values.append([value, None])
    previous = ''
    rows = []
    for key, value in source['slacks'].items():
        prefix = 0
        while prefix < min(len(previous), len(key)) and previous[prefix] == key[prefix]:
            prefix += 1
        rows.append([prefix, key[prefix:], values.index(value)])
        previous = key
    return {'top_order': list(source), 'other_fields': {k:v for k,v in source.items() if k not in ('atoms','slacks')},
            'atoms': source['atoms'], 'denominator_gcd': str(common),
            'denominator_factors': [str(int(d)//common) for d in denominators],
            'slack_value_dictionary': encoded_values, 'slack_key_prefix_rows': rows}

def decode(book):
    den = [str(int(book['denominator_gcd'])*int(f)) for f in book['denominator_factors']]
    values = [n if d is None else n+'/'+den[d] for n,d in book['slack_value_dictionary']]
    previous = ''
    slacks = {}
    for prefix, suffix, value_index in book['slack_key_prefix_rows']:
        key = previous[:prefix] + suffix
        slacks[key] = values[value_index]
        previous = key
    fields = {**book['other_fields'], 'atoms': book['atoms'], 'slacks': slacks}
    return {k:fields[k] for k in book['top_order']}

def reading_lines(book):
    yield 'CODEC: vI = literal numerator / (denominator_gcd * denominator_factors[D]); null D means literal integer string. Each rI = [prefix_length, literal_suffix, value_index]; key = prior_key[:prefix_length] + suffix. Order is exact. IDs are zero based.'
    for key in ('top_order','other_fields','denominator_gcd','denominator_factors'):
        yield key+'='+json.dumps(book[key], ensure_ascii=False, separators=(',',':'))
    for i, atom in enumerate(book['atoms']):
        yield 'atom'+str(i)+'='+json.dumps(atom, ensure_ascii=False, separators=(',',':'))
    for i, (n,d) in enumerate(book['slack_value_dictionary']):
        yield 'v'+str(i)+'='+n+('/d'+str(d) if d is not None else '')
    for i, row in enumerate(book['slack_key_prefix_rows']):
        yield 'r'+str(i)+'='+json.dumps(row, ensure_ascii=False, separators=(',',':'))

if __name__ == '__main__':
    import sys
    source_path, output_root = map(Path,sys.argv[1:])
    original_bytes = source_path.read_bytes()
    source = json.loads(original_bytes)
    book = encode(source)
    restored = decode(book)
    assert restored == source
    assert list(restored) == list(source)
    assert list(restored['slacks'].items()) == list(source['slacks'].items())
    output_root.mkdir(parents=True,exist_ok=True)
    (output_root/'full_json_reading_dictionary.json').write_text(json.dumps(book,ensure_ascii=False,indent=2)+'\n')
    (output_root/'decoded_exact_max_menu_tuple_primal.json').write_text(json.dumps(restored,ensure_ascii=False,indent=2)+'\n')
    lines = list(reading_lines(book))
    (output_root/'full_json_reading_view.txt').write_text('\n'.join(lines)+'\n')
    chunks=[]; current=[]; size=0
    for line in lines:
        if current and size+len(line)>14500:
            chunks.append(current); current=[];size=0
        current.append(line);size+=len(line)+1
    if current:chunks.append(current)
    refs=[]
    for i,chunk in enumerate(chunks):
        path=output_root/('readpass-%02d.txt'%(i+1))
        path.write_text('\n'.join(chunk)+'\n')
        refs.append({'file':path.name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'first':chunk[0].split('=')[0],'last':chunk[-1].split('=')[0]})
    report={'source_sha256':hashlib.sha256(original_bytes).hexdigest(),'decoded_json_equals_original':restored==source,'top_field_order_equal':list(restored)==list(source),'all_4007_slack_key_value_pairs_order_equal':list(restored['slacks'].items())==list(source['slacks'].items()),'chunks':refs}
    (output_root/'readview_reversibility.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))
