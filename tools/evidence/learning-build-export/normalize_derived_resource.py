"""Format a derived resource and bind its actual bytes; never edit frozen HTML."""
from pathlib import Path
import hashlib
import json
import sys

resource, audit = map(Path, sys.argv[1:3])
before = resource.read_text()
after = ''.join('\n' if line.strip() == '' and line.endswith('\n') else line
                for line in before.splitlines(keepends=True))
if after != before:
    resource.write_text(after)
data = resource.read_bytes()
record = json.loads(audit.read_text())
record['post_extraction_normalization'] = {
    'operation': 'remove spaces only from otherwise empty lines in the derived Markdown',
    'prior_resource_bytes': record['resource_bytes'],
    'prior_resource_sha256': record['resource_sha256'],
    'frozen_html_changed': False,
    'mathematical_content_changed': False,
}
record['resource_bytes'] = len(data)
record['resource_sha256'] = hashlib.sha256(data).hexdigest()
audit.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
print(record['resource_bytes'], record['resource_sha256'])
