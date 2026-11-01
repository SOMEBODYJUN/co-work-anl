"""Replay the exact captured mathematics, replacing only its workspace input path."""
from pathlib import Path
import hashlib,json,sys
here=Path(__file__).resolve().parent
source=here/'verify-root-and-full-history.py'
data=source.read_bytes()
assert hashlib.sha256(data).hexdigest()=='d4a8749e4784f9dcda5e6e8c955980aa4c4f785a39d4dff9732dbe9a36a02b09'
args=[x for x in sys.argv[1:]if x!='--prepare-only']
input_path=Path(args[0]).resolve()if args else here.parent/'related-original/largest_incumbent_n3p6_best.json'
assert hashlib.sha256(input_path.read_bytes()).hexdigest()=='7dcd445bdfe275e7b0521945ad4242aea3f3401dc0df848fb01c5bcb2fcfcbbd'
old="root=Path('/workspace/scratch/37f0f9248cfc');p=root/'boss4-research/archives/customer-attraction/tools/evidence/R-18-global-proof-incumbent-20261031/original/largest_incumbent_n3p6_best.json'"
text=data.decode();assert text.count(old)==1
text=text.replace(old,'p=Path('+repr(str(input_path))+')')
code=compile(text,str(source),'exec')
if '--prepare-only'in sys.argv:
 print(json.dumps({'original_code_sha_matches':True,'exact_input_sha_matches':True,'only_input_path_replaced':True,'compilation_passed':True,'mathematical_execution':False}))
else:exec(code,{'__name__':'__main__','__file__':str(source)})
