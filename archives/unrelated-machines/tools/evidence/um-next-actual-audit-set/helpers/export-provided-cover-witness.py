"""Export the frozen source's provided fixture/witness helpers, not its full audit."""
from pathlib import Path
import importlib.util,argparse,json
p=argparse.ArgumentParser();p.add_argument('--origin',type=Path,required=True);p.add_argument('--output-dir',type=Path,required=True);a=p.parse_args();a.output_dir.mkdir(exist_ok=False)
s=importlib.util.spec_from_file_location('frozen_finite_cover',a.origin/'tests/audits/unrelated_machines/configuration_finite_cover.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
for name,value in [('seed.json',m.serial_fixture()),('actual-cover-witness.json',m.serial_witness())]:
 with (a.output_dir/name).open('x') as f:f.write(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(result='EXPORTED_SOURCE_PROVIDED_HELPERS',q=6,job_copies=42,machine_copies=24,full_audit_called=False)))
