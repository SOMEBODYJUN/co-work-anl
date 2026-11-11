"""Run the frozen literal audit without modifying its frozen output files.

The exact source is SHA-bound and executed unchanged.  Only its output sink
is redirected into this task's write area.  No constructor is imported.
"""
from hashlib import sha256
from pathlib import Path
import json
import sys

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'z_successor_20910/literal_audit.py'

def main():
    blob=SOURCE.read_bytes()
    scope={'__file__':str(SOURCE),'__name__':'frozen_literal_audit_read_only'}
    exec(compile(blob,str(SOURCE),'exec'),scope)
    def save(name,data):
        data['frozen_literal_source_sha256']=sha256(blob).hexdigest()
        (HERE/('inherited_'+name)).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    scope['save']=save
    sys.argv=[str(SOURCE),'--certificate']
    scope['main']()

if __name__=='__main__':main()
