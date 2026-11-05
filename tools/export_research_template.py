"""Export the research method to a new local repository, without project assets."""
import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess


def export(root, destination, remote, branch='main'):
    if not re.fullmatch(r'https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:\.git)?', remote):
        raise ValueError('Supply a credential-free GitHub repository URL')
    if subprocess.run(['git', 'check-ref-format', 'refs/heads/' + branch], capture_output=True).returncode:
        raise ValueError('Invalid branch')
    if destination.exists(): raise ValueError('Export destination must not already exist')
    destination.mkdir(parents=True)
    shutil.copy2(root / 'work.py', destination / 'work.py')
    shutil.copy2(root / '.gitignore', destination / '.gitignore')
    shutil.copytree(root / 'tools', destination / 'tools', ignore=shutil.ignore_patterns('evidence', '__pycache__'))
    shutil.copytree(root / '.devcontainer', destination / '.devcontainer')
    shutil.copytree(root / '.github', destination / '.github')
    (destination / 'research').mkdir(); (destination / 'prompts').mkdir()
    for name in ['IMPLEMENTATION.md', 'GITHUB_RESOURCES.md', 'PHASE3_READINESS.md', 'UPSTREAM_ADAPTATION.md']:
        shutil.copy2(root / 'research' / name, destination / 'research' / name)
    for name in ['research-runtime.md', 'solver-full.md', 'solver-obstacle.md', '02.5-3-register.md', '02.5-3-worker.md', '03-map.md', '03-map-worker.md']:
        shutil.copy2(root / 'prompts' / name, destination / 'prompts' / name)
    for name in ['p25-register-v2', 'map-v2']:
        path = destination / 'research/operations' / name
        path.mkdir(parents=True)
        shutil.copy2(root / 'research/operations' / name / 'run.json', path / 'run.json')
    experiments = json.loads((root / 'research/experiments.json').read_text())
    experiments['experiments'] = {
        name: experiments['experiments'][name]
        for name in ('cag-five-local', 'positive-kernels-rank')
        if name in experiments['experiments']
    }
    (destination / 'research/experiments.json').write_text(json.dumps(experiments, indent=2) + '\n')
    workflow = destination / '.github/workflows/research-compute.yml'
    workflow.write_text(workflow.read_text())
    source = (destination / 'work.py').read_text()
    for key, value in [('REMOTE', remote), ('DEFAULT_BRANCH', branch), ('DEFAULT_BOARD_BRANCH', 'wcg/board-research')]:
        source = re.sub(r'^' + key + r' = .*$', lambda _: key + ' = ' + json.dumps(value), source, count=1, flags=re.M)
    (destination / 'work.py').write_text(source)
    (destination / 'README.md').write_text('# Reusable mathematical research workspace\n\n'
        'Read [the executable workflow](research/IMPLEMENTATION.md). Create your own exact problem, model, archive and explicit registration.\n\n'
        'This export contains tools and prompts, not the original mathematical archive, credentials, Git history or running agents.\n'
        'Start with `python work.py start --actor Boss1 --role boss --save YOUR_ARCHIVE --remote ' + remote + '`.\n')
    (destination / 'prompts/README.md').write_text('# Research prompts\n\nRead research-runtime.md and the two solver prompts.\n')
    (destination / 'research/CURATION.md').write_text('# Prepare mathematical assets\n\nRead the new project mathematics. Preserve exact domains, quantifiers, hypotheses and conclusions. Register objects explicitly using IMPLEMENTATION.md. No prior project mathematical assets were copied.\n')
    for directory in ['prompts', 'research']:
        for path in (destination / directory).rglob('*.md'):
            text = path.read_text().replace('https://github.com/SOMEBODYJUN/co-work-anl.git', remote).replace('rebuild/research-v2', branch)
            if directory == 'research':
                text = '> Reusable template: historical account checks below belong to the source project. Check this new repository and its resources independently.\n\n' + text
            path.write_text(text)
    subprocess.run(['git', 'init', '--quiet', '--initial-branch=' + branch], cwd=destination, check=True)
    subprocess.run(['git', 'remote', 'add', 'origin', remote], cwd=destination, check=True)
    with (destination / 'README.md').open('a') as stream:
        stream.write('\nThe empty local Git repository and origin are prepared. After adding your exact problem, make an initial commit and publish with your own authentication. No remote push was performed.\n')
    return {'status': 'exported-local-not-published', 'path': str(destination), 'remote': remote, 'branch': branch}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True); parser.add_argument('--remote', required=True)
    parser.add_argument('--branch', default='main'); args = parser.parse_args()
    try: result = export(Path(__file__).resolve().parents[1], args.output.resolve(), args.remote, args.branch)
    except (ValueError, OSError) as exc: raise SystemExit(str(exc))
    print(json.dumps(result, indent=2))
