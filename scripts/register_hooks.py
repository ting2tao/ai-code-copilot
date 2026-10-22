#!/usr/bin/env python3
"""Register framework-owned hooks without trusting them or replacing unrelated handlers."""
import argparse
import json
from pathlib import Path
import shlex
import sys
import subprocess
import tempfile
import os


def register(platform, config, root, bash_command, windows_command=False):
    data = json.loads(config.read_text(encoding='utf-8-sig')) if config.exists() else {}
    if not isinstance(data, dict):
        raise ValueError('config must be an object')
    hooks = data.setdefault('hooks', {})
    if not isinstance(hooks, dict):
        raise ValueError('hooks must be an object')
    scripts = {'SessionStart': ('session-start', '')}
    if platform == 'codex':
        scripts['PreToolUse'] = ('pre-tool-codex', '^apply_patch$')
    for event, (name, matcher) in scripts.items():
        entries = hooks.setdefault(event, [])
        if not isinstance(entries, list):
            raise ValueError('event must be an array')
        script = str(root / 'hooks' / name)
        if not Path(script).is_file():
            raise ValueError('missing hook script')
        argument = subprocess.list2cmdline([script.replace('\\', '/')]) if windows_command else shlex.quote(script)
        command = bash_command + ' ' + argument
        # Remove only this installation's exact commands, retaining mixed groups.
        # Other launchers/legacy registrations are not silently migrated.
        retained = []
        for group in entries:
            if not isinstance(group, dict) or not isinstance(group.get('hooks'), list):
                raise ValueError('invalid matcher group')
            remaining = []
            for handler in group['hooks']:
                if not isinstance(handler, dict):
                    raise ValueError('invalid handler')
                if handler.get('type') == 'command' and not isinstance(handler.get('command'), str):
                    raise ValueError('invalid command handler')
                if handler.get('command') != command:
                    remaining.append(handler)
            if remaining:
                retained.append({**group, 'hooks': remaining})
        handler = {'type': 'command', 'command': command, 'timeout': 15}
        if event == 'SessionStart':
            handler['async'] = False
        hooks[event] = retained + [{'matcher': matcher, 'hooks': [handler]}]
    config.parent.mkdir(parents=True, exist_ok=True)
    # Keep original bytes intact on validation failure; replace atomically after serialization.
    encoded = json.dumps(data, indent=2, ensure_ascii=False) + '\n'
    fd, temporary = tempfile.mkstemp(prefix='.copilot-hooks-', dir=config.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as handle:
            handle.write(encoded)
        os.replace(temporary, config)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--platform', choices=['codex', 'claude'], required=True)
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--bash-command', default='bash', help='trusted launcher prefix, e.g. wsl bash')
    parser.add_argument('--windows-command', action='store_true', help='quote script argument for a Windows host')
    args = parser.parse_args()
    try:
        register(args.platform, args.config, args.root, args.bash_command, args.windows_command)
    except (OSError, ValueError, TypeError):
        print('hooks: registration failed; inspect config shape and script/runtime availability (content redacted)', file=sys.stderr)
        return 1
    print('hooks: configured; execution not verified')
    if args.platform == 'codex':
        print('hooks: review and trust current definitions with /hooks; untrusted hooks are skipped. Runtime support must be checked in the host.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
