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
    for name in ['README.md', 'IMPLEMENTATION.md', 'RESEARCH_WORKFLOW.md', 'GITHUB_RESOURCES.md', 'UPSTREAM_ADAPTATION.md']:
        shutil.copy2(root / 'research' / name, destination / 'research' / name)
    for directory in ['agent-design', 'schemas']:
        shutil.copytree(root / 'research' / directory, destination / 'research' / directory,
                        ignore=shutil.ignore_patterns('validation.json', '__pycache__'))
    for name in ['research-runtime.md', 'research-main-design.md', 'research-line-design.md',
                 'research-review-design.md', 'paper-evaluation.md']:
        shutil.copy2(root / 'prompts' / name, destination / 'prompts' / name)
    experiments = json.loads((root / 'research/experiments.json').read_text())
    # The mathematical scripts are intentionally not part of this export.
    # New projects declare their own useful computations in this manifest.
    experiments['experiments'] = {}
    (destination / 'research/experiments.json').write_text(json.dumps(experiments, indent=2) + '\n')
    workflow = destination / '.github/workflows/research-compute.yml'
    workflow.write_text(workflow.read_text().replace('rebuild/research-v2', branch))
    source = (destination / 'work.py').read_text()
    for key, value in [('REMOTE', remote), ('DEFAULT_BRANCH', branch)]:
        source = re.sub(r'^' + key + r' = .*$', lambda _: key + ' = ' + json.dumps(value), source, count=1, flags=re.M)
    (destination / 'work.py').write_text(source)
    (destination / 'README.md').write_text('# Reusable mathematical research workspace\n\n'
        'Read [the executable workflow](research/IMPLEMENTATION.md). Create your own exact problem, model, archive and explicit registration.\n\n'
        'For mathematical paper evaluation, see [the evaluation workflow](tools/PAPER_EVALUATION.md).\n\n'
        'This export contains tools and prompts, not the original mathematical archive, credentials, Git history or running agents.\n'
        'Initialize the local Git repository with an initial commit, then run `python work.py start --actor Boss1 --role boss --save YOUR_ARCHIVE --create-archive --remote ' + remote + '`.\n')
    (destination / 'prompts/README.md').write_text('# Research prompts\n\nStart with research-runtime.md. Main reads the internal Main, line and review instructions from this repository.\n')
    (destination / 'AGENTS.md').write_text('# Mathematical research workspace\n\n'
        'Use work.py and prompts/research-runtime.md; read research/IMPLEMENTATION.md and research/agent-design/HYPEREDGE_WORKFLOW.md as needed.\n\n'
        'Fix the user\'s original target, model and quantifiers before doing research. Main reads hyperedges and short receipts; idea, execution and independent workers do the substantive reading and mathematics. Python files do not launch models.\n\n'
        'When asked to evaluate a paper, run research evaluate --paper, follow the generated task, then validate and render the report; see tools/PAPER_EVALUATION.md.\n'
        'Keep credentials outside the repository. Main serializes Git writes, preserves peer changes and reports remote saving only after checkpoint confirms pushed.\n\n'
        'Save useful drafts and failures in each RUN journal promptly. Register reusable mathematics with exact state, scope and evidence; retain ALL premises, alternative proofs and unpaid obligations. Structural checks do not certify mathematical truth.\n\n'
        'This export has no active research board and contains no source-project mathematics or live agents. Add project-specific rules and the exact problem when available.\n')
    for directory in ['prompts', 'research']:
        for path in (destination / directory).rglob('*.md'):
            # Third-party originals and NOTICE must retain the exact licensed
            # bytes recorded in provenance.json, including when re-exported.
            if path.is_relative_to(destination / 'research/agent-design/upstream'):
                continue
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
