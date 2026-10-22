"""Behavioral regressions for production routing and installed Codex hooks."""
import importlib.util
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import run_agent_evals as runner
from check_progressive_sdd import should_activate, classify_activated


class WorkflowAlignment(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='copilot alignment ')
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name) / 'repo'
        self.repo.mkdir()
        subprocess.run(['git', 'init', '-q', str(self.repo)], check=True)
        self.policy = json.loads((ROOT / 'config/workflow-policy.json').read_text())

    def hook(self, patch, **extra):
        payload = dict(hook_event_name='PreToolUse', cwd=str(self.repo), tool_name='apply_patch',
                       tool_input={'command': patch, 'approvals': ['protected-path-edit']})
        payload.update(extra)
        return subprocess.run(['bash', str(ROOT / 'hooks/pre-tool-codex')], input=json.dumps(payload),
                              text=True, capture_output=True, cwd=self.repo)

    def test_production_alone_is_full_and_human_gated(self):
        facts = dict(files=1, signals=['production'], risks=['production'])
        self.assertTrue(should_activate(self.policy, facts))
        self.assertEqual(classify_activated(self.policy, facts), 'full')
        case = dict(id='production-only-regression', description='Independent production risk',
                    prompt='Change production behavior', facts=facts,
                    expected=dict(tier='full', modules=['agents/workflows/full.md'],
                                  humanGate=True, writesBeforeContract=False))
        self.assertEqual(runner.validate_case(case, self.policy), [])
        for field in ['signals', 'risks']:
            case['facts'] = {'files': 1, field: ['production']}
            self.assertEqual(runner.validate_case(case, self.policy), [])

    def test_native_and_authorized_local_work_remain_native(self):
        for facts in [dict(files=1, signals=[]), dict(files=5, signals=[], authorizedLocalWork=True)]:
            self.assertFalse(should_activate(self.policy, facts))
        for count, tier in [(2, 'compact'), (3, 'compact'), (5, 'compact'), (6, 'full')]:
            self.assertEqual(classify_activated(self.policy, dict(files=count)), tier)

    def test_codex_safe_patch_and_delete(self):
        for patch in ['*** Begin Patch\n*** Add File: src/main.py\n+answer = 42\n*** End Patch',
                      '*** Begin Patch\n*** Update File: src/main.py\n@@\n-old\n+new\n*** End Patch',
                      '*** Begin Patch\n*** Delete File: src/old.py\n*** End Patch']:
            result = self.hook(patch)
            self.assertEqual((result.returncode, result.stdout), (0, ''), result.stderr)

    def test_codex_blocks_secret_pii_protected_test_and_move(self):
        for path, content, control in [
            ('src/main.py', 'api_key = ' + "'synthetic-secret-value'", 'secret-diff'),
            ('src/main.py', 'phone = ' + '"13800138000"', 'sensitive-data-diff'),
            ('infra/main.tf', 'safe', 'protected-path-edit'),
            ('tests/test_main.py', 'safe', 'fix-test-integrity')]:
            result = self.hook(f'*** Begin Patch\n*** Add File: {path}\n+{content}\n*** End Patch')
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertIn(control, result.stdout + result.stderr)
            self.assertNotIn('synthetic-secret-value', result.stdout + result.stderr)
            self.assertNotIn('13800138000', result.stdout + result.stderr)
            self.assertNotIn('"ask"', result.stdout)
        for patch in ['*** Begin Patch\n*** Update File: src/a.py\n*** Move to: infra/a.py\n@@\n-x\n+y\n*** End Patch',
                      '*** Begin Patch\n*** Delete File: infra/a.py\n*** End Patch']:
            result = self.hook(patch)
            self.assertEqual(result.returncode, 2)
            self.assertIn('protected-path-edit', result.stdout + result.stderr)

    def test_codex_malformed_unsupported_and_traversal_block(self):
        for patch in ['', 'not a patch', '*** Begin Patch\n*** End Patch',
                      '*** Begin Patch\n*** Add File: ../outside.py\n+ok\n*** End Patch',
                      '*** Begin Patch\n*** Add File: a.py\ninvalid\n*** End Patch',
                      '*** Begin Patch\n*** Update File: a.py\n+no hunk\n*** End Patch',
                      '*** Begin Patch\n*** Delete File: a.py\n*** End Patch\ntrailing']:
            result = self.hook(patch)
            self.assertEqual(result.returncode, 2, patch)
        self.assertEqual(self.hook('echo ignored', tool_name='Bash').returncode, 2)
        self.assertEqual(self.hook('ignored', cwd=self.tmp.name).returncode, 2)

    def test_codex_resolved_and_lexical_protected_paths(self):
        (self.repo / 'infra').mkdir()
        (self.repo / 'alias').symlink_to(self.repo / 'infra', target_is_directory=True)
        result = self.hook('*** Begin Patch\n*** Add File: alias/main.tf\n+ok\n*** End Patch')
        self.assertEqual(result.returncode, 2)
        self.assertIn('protected-path-edit', result.stdout + result.stderr)
        (self.repo / 'outside').symlink_to(Path(self.tmp.name), target_is_directory=True)
        self.assertEqual(self.hook('*** Begin Patch\n*** Add File: outside/a.py\n+ok\n*** End Patch').returncode, 2)

    def register(self, platform, config, prefix='bash'):
        return subprocess.run([sys.executable, str(ROOT / 'scripts/register_hooks.py'),
                               '--platform', platform, '--config', str(config),
                               '--root', str(ROOT), '--bash-command', prefix],
                              text=True, capture_output=True)

    def test_registration_preserves_unrelated_handlers_and_is_idempotent(self):
        for platform in ['codex', 'claude']:
            config = Path(self.tmp.name) / (platform + '.json')
            initial = {'custom': 7, 'hooks': {'SessionStart': [{'hooks': [{'type': 'command', 'command': 'echo unrelated'}]}]}}
            config.write_text(json.dumps(initial))
            for _ in range(2):
                result = self.register(platform, config)
                self.assertEqual(result.returncode, 0, result.stderr)
            data = json.loads(config.read_text())
            self.assertEqual(data['custom'], 7)
            commands = [h['command'] for g in data['hooks']['SessionStart'] for h in g['hooks']]
            self.assertEqual(commands.count('echo unrelated'), 1)
            self.assertEqual(len(commands), 2)
            self.assertEqual('PreToolUse' in data['hooks'], platform == 'codex')
            if platform == 'codex':
                self.assertIn('trust', result.stdout)
                handler = data['hooks']['PreToolUse'][0]
                self.assertEqual(handler['matcher'], '^apply_patch$')
                call = subprocess.run(shlex.split(handler['hooks'][0]['command']), cwd=self.repo,
                    input=json.dumps(dict(hook_event_name='PreToolUse', cwd=str(self.repo),
                    tool_name='apply_patch', tool_input={'command': '*** Begin Patch\n*** Add File: main.py\n+ok\n*** End Patch'})),
                    text=True, capture_output=True)
                self.assertEqual(call.returncode, 0, call.stderr)

    def test_mixed_group_preserves_unrelated_handler(self):
        config = Path(self.tmp.name) / 'hooks.json'
        self.assertEqual(self.register('codex', config).returncode, 0)
        data = json.loads(config.read_text())
        data['hooks']['SessionStart'][0]['hooks'].append({'type': 'command', 'command': 'echo unrelated'})
        config.write_text(json.dumps(data))
        self.assertEqual(self.register('codex', config).returncode, 0)
        commands = [h['command'] for g in json.loads(config.read_text())['hooks']['SessionStart'] for h in g['hooks']]
        self.assertEqual(len(commands), 2)
        self.assertEqual(commands.count('echo unrelated'), 1)

    def test_real_installer_and_registered_command_round_trip_with_spaces(self):
        home = Path(self.tmp.name) / 'home with spaces'; home.mkdir()
        app = home / '.codex'; installed = app / 'ai_code_copilot'
        env = {**os.environ, 'HOME': str(home), 'CODEX_HOME': str(app), 'AI_CODE_COPILOT_HOME': str(installed)}
        for _ in range(2):
            result = subprocess.run(['bash', str(ROOT / 'install.sh'), '--codex'], cwd=ROOT,
                                    env=env, text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('trust', result.stdout)
        self.assertFalse((app / 'settings.json').exists())
        hooks = json.loads((app / 'hooks.json').read_text())['hooks']
        self.assertEqual(len(hooks['PreToolUse']), 1)
        command = shlex.split(hooks['PreToolUse'][0]['hooks'][0]['command'])
        for path, expected in [('src/main.py', 0), ('infra/main.tf', 2)]:
            payload = dict(hook_event_name='PreToolUse', cwd=str(self.repo), tool_name='apply_patch',
                           tool_input={'command': f'*** Begin Patch\n*** Add File: {path}\n+ok\n*** End Patch'})
            result = subprocess.run(command, cwd=self.repo, env=env, input=json.dumps(payload), text=True, capture_output=True)
            self.assertEqual(result.returncode, expected, result.stderr)
        startup = subprocess.run(shlex.split(hooks['SessionStart'][0]['hooks'][0]['command']),
                                 cwd=self.repo, env=env, input='{}', text=True, capture_output=True)
        self.assertEqual(startup.returncode, 0, startup.stderr)
        self.assertIn('hookSpecificOutput', startup.stdout)

    def test_windows_quote_and_wsl_path_translation(self):
        spec = importlib.util.spec_from_file_location('alignment_guardrail', ROOT / 'scripts/check_guardrails.py')
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        from unittest.mock import patch
        with patch.object(module.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, b'/mnt/c/repo\n', b'')) as run:
            self.assertEqual(module.codex_host_path('C:\\repo'), '/mnt/c/repo')
            self.assertEqual(run.call_args.args[0], ['wslpath', '-u', 'C:\\repo'])
        with patch.object(module.subprocess, 'run', side_effect=FileNotFoundError):
            with self.assertRaises(module.GitUnavailable):
                module.codex_host_path('C:\\repo')
        config = Path(self.tmp.name) / 'windows.json'
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/register_hooks.py'), '--platform', 'codex',
            '--config', str(config), '--root', str(ROOT), '--bash-command', '"C:/Program Files/Git/bin/bash.exe"',
            '--windows-command'], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        command = json.loads(config.read_text())['hooks']['SessionStart'][0]['hooks'][0]['command']
        self.assertTrue(command.startswith('"C:/Program Files/Git/bin/bash.exe" '))
        for installer in ['install.sh', 'install-wsl.sh', 'install.ps1']:
            text = (ROOT / installer).read_text()
            self.assertIn('hooks.json', text)
            self.assertIn('register_hooks.py', text)

    def test_registration_preserves_non_command_hooks(self):
        config = Path(self.tmp.name) / 'mixed.json'
        other = {'type': 'prompt', 'prompt': 'A separate user workflow'}
        config.write_text(json.dumps({'hooks': {'SessionStart': [{'hooks': [other]}]}}))
        result = self.register('codex', config)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(config.read_text())['hooks']['SessionStart'][0]['hooks'], [other])

    def test_registration_rejects_invalid_config_without_modification(self):
        config = Path(self.tmp.name) / 'invalid.json'
        for raw in ['not-json', '[]', '{"hooks": []}', '{"hooks":{"SessionStart":{}}}']:
            config.write_text(raw)
            self.assertNotEqual(self.register('codex', config).returncode, 0)
            self.assertEqual(config.read_text(), raw)

    def test_codex_missing_python_is_explicitly_blocked(self):
        bindir = Path(self.tmp.name) / 'bin'; bindir.mkdir()
        for tool in ['dirname']:
            (bindir / tool).symlink_to('/usr/bin/' + tool)
        result = subprocess.run(['/bin/bash', str(ROOT / 'hooks/pre-tool-codex')], input='{}',
            env={**os.environ, 'PATH': str(bindir)}, text=True, capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn('degraded', result.stderr)


if __name__ == '__main__':
    unittest.main()
