"""Pure JSON representation decoding and ordered equality; no mathematical audit."""
import hashlib,json,pathlib,sys
HERE=pathlib.Path(__file__).resolve().parent

def sequence(expr):
    out=[]
    for value in expr:
        if not isinstance(value,list): out.append(value)
        elif value[0]=='R': out.extend([value[1]]*value[2])
        elif value[0]=='A': out.extend(value[1]+value[2]*i for i in range(value[3]))
        elif value[0]=='P': out.extend(sequence(value[1])*value[2])
        elif value[0]=='E': out.extend(y for x in sequence(value[1]) for y in [x]*value[2])
        elif value[0]=='C': out.extend(y for i in range(value[1],value[1]+value[2]) for j in range(i+1,value[1]+value[2]) for y in [i,j])
        else: raise ValueError(value)
    return out

def decode_point(x):
    strings=x['string_dictionary'];groups=x['group_dictionary'];out=dict(x['header'])
    out['variables']=[dict(zip(x['record_keys'],[h,strings[l],strings[r],groups[g],bit,strings[w]])) for h,l,r,g,bit,w in x['records']]
    return {key:out[key] for key in x['top_level_key_order']}

def decode_atoms(x):
    strings=x['string_dictionary'];out=dict(x['header'])
    out['atoms']=[{k:strings[v] if k in x['string_fields'] else v for k,v in zip(x['record_keys'],row)} for row in x['records']]
    return {key:out[key] for key in x['top_level_key_order']}

def decode_slacks(x):
    columns=[sequence(c) for c in x['column_dictionary']];den=x['denominator_dictionary'];vals=[v[0]+'/'+den[v[1]] if len(v)==2 else v[0] for v in x['slack_dictionary']];out=[]
    for start,count,tid,argids,sids in x['row_blocks']:
        tpl=x['name_templates'][tid];args=[columns[i] for i in argids];ss=columns[sids]
        for offset in range(count):
            name=''.join(s+(str(args[i][offset]) if i<len(args) else '') for i,s in enumerate(tpl))
            out.append(dict(zip(x['record_keys'],[start+offset,name,vals[ss[offset]]])))
    return out

def canonical_ordered(x): return json.dumps(x,ensure_ascii=False,separators=(',',':')).encode()

def main():
    base=pathlib.Path(sys.argv[1]);manifest=[]
    items=[('compact-point.json','original/pair_cross_exact.json',decode_point),('compact-atoms.json','replay/cross/common-cube-atom-recipe.json',decode_atoms),('read-table-slacks.json','replay/cross/all-row-slacks.json',decode_slacks)]
    for compact,relative,decoder in items:
        source=base/'archives/customer-attraction/tools/evidence/pair-split-cross-points-boss3'/relative;raw=source.read_bytes();original=json.loads(raw);represented=json.loads((HERE/compact).read_text());decoded=decoder(represented)
        equal=canonical_ordered(decoded)==canonical_ordered(original)
        if not equal:raise ValueError(compact)
        manifest.append({'source':{'path':str(source.relative_to(base)),'sha256':hashlib.sha256(raw).hexdigest()},'compact':{'path':compact,'sha256':hashlib.sha256((HERE/compact).read_bytes()).hexdigest()},'all_fields_array_and_object_key_order_and_fraction_strings_equal':equal,'decoded_ordered_json_sha256':hashlib.sha256(canonical_ordered(decoded)).hexdigest(),'operation':'decode and byte/string equality only; no row arithmetic, sign audit, matrix reconstruction, optimizer, BI, or scan'})
    (HERE/'lossless-read-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(manifest,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
