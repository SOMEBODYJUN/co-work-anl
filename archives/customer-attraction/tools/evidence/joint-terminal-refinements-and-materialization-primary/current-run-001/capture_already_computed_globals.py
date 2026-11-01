from pathlib import Path
import sys,runpy,json,contextlib
out=Path(__file__).resolve().parent
with (out/'native-stdout.txt').open('w') as stdout,(out/'native-stderr.txt').open('w') as stderr:
 with contextlib.redirect_stdout(stdout),contextlib.redirect_stderr(stderr):
  values=runpy.run_path(sys.argv[1],run_name='__main__')
# Serialize only values the original already computed; no utility or row call.
data={'labels':values['labels'],'scaling':values['scale'],'customer_types':[{'mask':str(mask),'multiplicity':count}for mask,count in values['customers'].items()]}
(out/'native-already-computed-unit-type-instance.json').write_text(json.dumps(data,indent=2)+'\n')
