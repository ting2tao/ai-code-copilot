"""Black-box guardrail regressions and isolated, one-factor ablation checks."""
import copy
from contextlib import redirect_stderr, redirect_stdout
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "scripts/check_guardrails.py"
POLICY = ROOT / "config/guardrail-policy.json"


def event(path="src/main.py", line="answer = 42", **extra):
    return dict(eventVersion=1, operation="edit", taskMode="apply",
                changedPaths=[path], diffAddedLines=[dict(path=path, line=line)],
                risks=[], approvals=[], **extra)


class Guardrails(unittest.TestCase):
    def setUp(self):
        self.assertTrue(CHECKER.is_file(), "missing guardrail checker implementation")
        spec = importlib.util.spec_from_file_location("guardrails", CHECKER)
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)
        self.policy = self.module.load_policy(POLICY)

    def run_cli(self, data, *args, cwd=ROOT):
        return subprocess.run([sys.executable, str(CHECKER), "--policy", str(POLICY),
                               *args], input=json.dumps(data), text=True,
                              capture_output=True, cwd=cwd)

    def test_fixtures(self):
        cases = json.loads((ROOT / "tests/fixtures/guardrails/cases.json").read_text())
        for case in cases:
            with self.subTest(case=case["id"]):
                line = case.get("line", "".join(case.get("lineParts", [])))
                data = event(case["path"], line)
                for key in ("taskMode", "risks", "operation"):
                    if key in case:
                        data[key] = case[key]
                result = self.run_cli(data, "--event", "-")
                self.assertEqual(result.returncode, int(bool(case["expected"])))
                report = json.loads(result.stdout)
                self.assertEqual([d["controlId"] for d in report["decisions"]], case["expected"])
                if "secret-diff" in case["expected"] or "sensitive-data-diff" in case["expected"]:
                    self.assertNotIn(line, result.stdout + result.stderr)
                    self.assertNotIn("13800138000", result.stdout + result.stderr)
                    self.assertNotIn("synthetic-secret-value", result.stdout + result.stderr)

    def approve(self, data, control):
        digest_data = {k: v for k, v in data.items() if k != "approvals"}
        digest = hashlib.sha256(json.dumps(digest_data, sort_keys=True,
                                           separators=(",", ":")).encode()).hexdigest()
        data["approvals"] = [dict(controlId=control, reviewer="human-owner",
                                  evidenceRef="change/log.md#approval", eventHash="sha256:" + digest)]

    def test_approval_is_bound_to_exact_event(self):
        data = event("infra/main.tf")
        self.approve(data, "protected-path-edit")
        result = self.run_cli(data, "--event", "-")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)["decisions"][0]["action"], "approved")
        data["diffAddedLines"][0]["line"] = "changed again"
        self.assertEqual(self.run_cli(data, "--event", "-").returncode, 1)

    def test_secret_cannot_be_approved(self):
        data = event(line="password = " + "'synthetic-secret-value'")
        self.approve(data, "secret-diff")
        self.assertEqual(self.run_cli(data, "--event", "-").returncode, 1)

    def test_human_and_fix_approval(self):
        for control in ("high-risk-human-gate", "fix-test-integrity"):
            data = event("tests/test_main.py")
            data.update(risks=["money"] if control.startswith("high") else [], taskMode="fix" if control.startswith("fix") else "apply")
            self.approve(data, control)
            self.assertEqual(self.run_cli(data, "--event", "-").returncode, 0)

    def test_invalid_inputs_fail_without_echo(self):
        for field, value in [("eventVersion", True), ("eventVersion", 2), ("risks", ["typo"]),
                             ("taskMode", "typo"), ("changedPaths", ["../escape"]),
                             ("diffAddedLines", [{"path":"other", "line":"secret"}]),
                             ("approvals", ["secret-diff"]), ("operation", "typo")]:
            data = event()
            data[field] = value
            result = self.run_cli(data, "--event", "-")
            self.assertEqual(result.returncode, 1, field)
            self.assertIn("invalid", result.stderr)

    def test_hook_blocks_secrets_and_asks_for_protected_path(self):
        for name, key in (("Write", "content"), ("Edit", "new_string")):
            data = dict(hook_event_name="PreToolUse", cwd=str(ROOT), tool_name=name,
                        tool_input=dict(file_path=str(ROOT / "src/main.py")))
            data["tool_input"][key] = "api_key = " + "'synthetic-secret-value'"
            result = self.run_cli(data, "--hook-input", "-")
            self.assertEqual(result.returncode, 2)
            self.assertIn("secret-diff", result.stderr)
            self.assertNotIn("synthetic-secret-value", result.stderr)
            data["tool_input"] = dict(file_path=str(ROOT / "infra/main.tf"), **{key:"safe"}, approvals=["protected-path-edit"])
            result = self.run_cli(data, "--hook-input", "-")
            self.assertEqual(result.returncode, 0)
            self.assertEqual(json.loads(result.stdout)["hookSpecificOutput"]["permissionDecision"], "ask")

    def test_hook_invalid_payload_fail_closed(self):
        result = self.run_cli({}, "--hook-input", "-")
        self.assertEqual(result.returncode, 2)
        result = subprocess.run(["bash", str(ROOT / "hooks/pre-tool-guardrail")],
                                input="not json", text=True, capture_output=True)
        self.assertEqual(result.returncode, 2)

    def test_hook_safe_pii_and_outside_root(self):
        data = dict(hook_event_name="PreToolUse", cwd=str(ROOT), tool_name="Write",
                    tool_input=dict(file_path=str(ROOT / "src/main.py"), content="answer = 42"))
        result = self.run_cli(data, "--hook-input", "-")
        self.assertEqual((result.returncode, result.stdout), (0, ""))
        data["tool_input"]["content"] = 'phone = ' + '"13800138000"'
        result = self.run_cli(data, "--hook-input", "-")
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("13800138000", result.stdout + result.stderr)
        data["tool_input"] = dict(file_path="/outside-root.txt", content="safe")
        self.assertEqual(self.run_cli(data, "--hook-input", "-").returncode, 2)

    def test_review_warns_without_granting_authority(self):
        data = event()
        data["operation"] = "review"
        result = self.run_cli(data, "--event", "-")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)["decisions"][0]["action"], "warn")

    def test_capabilities_and_hook_registration(self):
        self.assertEqual(self.policy["adapters"]["codex-repo-hook"]["status"], "unavailable")
        self.assertTrue(self.policy["adapters"]["codex-repo-hook"]["fallback"])
        hooks = json.loads((ROOT / "hooks/hooks.json").read_text())["hooks"]
        self.assertEqual(hooks["PreToolUse"][0]["matcher"], "Write|Edit")

    def test_invalid_policy_cannot_silently_disable_controls(self):
        for field, value in (("addedLinePatterns", []), ("addedLinePatterns", "bad"),
                             ("layer", "advisory")):
            policy = copy.deepcopy(self.policy)
            policy["controls"][0][field] = value
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "policy.json"
                path.write_text(json.dumps(policy))
                with self.assertRaises(ValueError):
                    self.module.load_policy(path)

    def test_invalid_policy_selector_values_cannot_disable_controls(self):
        changes = [
            ("high-risk-human-gate", "risks", ["typo"]),
            ("high-risk-human-gate", "operations", ["typo"]),
            ("fix-test-integrity", "taskModes", ["typo"]),
        ]
        for control_id, field, value in changes:
            with self.subTest(control=control_id, field=field):
                policy = copy.deepcopy(self.policy)
                control = next(c for c in policy["controls"] if c["id"] == control_id)
                control[field] = value
                with tempfile.TemporaryDirectory() as directory:
                    path = Path(directory) / "policy.json"
                    path.write_text(json.dumps(policy))
                    with self.assertRaises(ValueError):
                        self.module.load_policy(path)

    def test_hook_preserves_protected_alias_path(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            (root / "infra").mkdir()
            (root / "safe.txt").write_text("safe")
            (root / "infra/alias").symlink_to(root / "safe.txt")
            data = dict(hook_event_name="PreToolUse", cwd=str(root), tool_name="Write",
                        tool_input=dict(file_path=str(root / "infra/alias"), content="safe"))
            result = self.run_cli(data, "--hook-input", "-")
            self.assertEqual(result.returncode, 0)
            self.assertIn('"permissionDecision": "ask"', result.stdout)

    def test_missing_runtime_reports_degraded_and_blocks(self):
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / "dirname").symlink_to("/usr/bin/dirname")
            result = subprocess.run(["/bin/bash", str(ROOT / "hooks/pre-tool-guardrail")],
                                    input="{}", text=True, capture_output=True,
                                    env={**os.environ, "PATH":directory})
            self.assertEqual(result.returncode, 2)
            self.assertIn("degraded", result.stderr)

    def test_git_invalid_base_and_binary_do_not_pass(self):
        result = self.run_cli(None, "--git-diff", "--output=unsafe")
        self.assertNotEqual(result.returncode, 0)
        with tempfile.TemporaryDirectory() as directory:
            subprocess.run(["git", "init", "-q", directory], check=True)
            subprocess.run(["git", "-C", directory, "-c", "user.name=Fixture", "-c",
                            "user.email=fixture@example.invalid", "commit", "--allow-empty", "-qm", "fixture"], check=True)
            (Path(directory) / "binary").write_bytes(b"\0\1\2")
            result = self.run_cli(None, "--git-diff", "HEAD", cwd=directory)
            self.assertEqual(result.returncode, 1)
            self.assertIn("invalid", result.stderr)

    def test_git_text_can_contain_binary_marker_words(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", directory], check=True)
            (root / "notes.txt").write_text("baseline\n")
            subprocess.run(["git", "-C", directory, "add", "notes.txt"], check=True)
            subprocess.run(["git", "-C", directory, "-c", "user.name=Fixture", "-c",
                            "user.email=fixture@example.invalid", "commit", "-qm", "fixture"], check=True)
            (root / "notes.txt").write_text("GIT binary patch\nBinary files are documented here\n")
            result = self.run_cli(None, "--git-diff", "HEAD", cwd=directory)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_single_factor_ablation(self):
        cases = json.loads((ROOT / "tests/fixtures/guardrails/cases.json").read_text())
        for control in ("secret-diff", "sensitive-data-diff", "protected-path-edit", "fix-test-integrity"):
            case = next(c for c in cases if c["expected"] == [control])
            data = event(case["path"], case.get("line", "".join(case.get("lineParts", []))))
            data["taskMode"] = case.get("taskMode", "apply")
            baseline = self.module.evaluate(self.policy, data)
            removed = copy.deepcopy(self.policy)
            removed["controls"] = [c for c in removed["controls"] if c["id"] != control]
            self.assertFalse(baseline["passed"])
            self.assertTrue(self.module.evaluate(removed, data)["passed"])
            self.assertEqual(self.module.evaluate(self.policy, data), baseline)

    def test_git_diff_includes_untracked_and_deletions(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            def git(*args):
                return subprocess.run(["git", *args], cwd=root, check=True, capture_output=True)
            git("init", "-q")
            (root / "tests").mkdir()
            (root / "tests/test_main.py").write_text("assert True\n")
            git("add", ".")
            git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "fixture")
            (root / "tests/test_main.py").unlink()
            (root / "new file.py").write_text("api_key = " + "'synthetic-secret-value'\n")
            result = self.run_cli(None, "--git-diff", "HEAD", "--task-mode", "fix", cwd=root)
            self.assertEqual(result.returncode, 1)
            ids = {d["controlId"] for d in json.loads(result.stdout)["decisions"]}
            self.assertEqual(ids, {"secret-diff", "fix-test-integrity"})

    def test_ablation_workflow_contract(self):
        for path in ("agents/workflows/full.md", "agents/workflows/review.md", "changes/templates/design-brief.md"):
            text = (ROOT / path).read_text()
            self.assertIn("消融", text)
            self.assertIn("证据", text)

    def test_git_snapshot_invalidates_stale_approvals(self):
        # Real diffs, no mocked Git. Each pair previously had the same lossy event.
        scenarios = ("deletion", "position", "base", "mode", "untracked-mode", "untracked-newline")
        for scenario in scenarios:
            with self.subTest(scenario=scenario), tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as evidence:
                root = Path(directory)
                def git(*args):
                    return subprocess.run(["git", *args], cwd=root, check=True, capture_output=True).stdout
                def commit():
                    git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "--allow-empty", "-qm", "fixture")
                git("init", "-q")
                git("config", "core.filemode", "false")  # Must not hide mode-only changes.
                (root / "infra").mkdir()
                target = root / "infra/config.txt"
                target.write_text("alpha\nbeta\ngamma\n")
                target.chmod(0o644)
                if not scenario.startswith("untracked"):
                    git("add", ".")
                commit()
                if scenario == "deletion":
                    target.write_text("beta\ngamma\n")
                elif scenario in {"position", "base"}:
                    target.write_text("added\nalpha\nbeta\ngamma\n")
                elif scenario == "mode":
                    target.chmod(0o755)
                first = self.run_cli(None, "--git-diff", "HEAD", cwd=root)
                self.assertEqual(first.returncode, 1)
                first_report = json.loads(first.stdout)
                approvals = Path(evidence) / "approvals.json"
                approvals.write_text(json.dumps([dict(controlId="protected-path-edit", reviewer="fixture-human",
                    evidenceRef="fixture-only", eventHash=first_report["eventHash"])]))
                args = ("--git-diff", "HEAD", "--approvals", str(approvals))
                self.assertEqual(self.run_cli(None, *args, cwd=root).returncode, 0, "same snapshot must remain approved")
                if scenario == "deletion":
                    target.write_text("alpha\ngamma\n")
                elif scenario == "position":
                    target.write_text("alpha\nbeta\nadded\ngamma\n")
                elif scenario == "base":
                    commit()  # Same tree and patch, a different base commit.
                elif scenario == "mode":
                    target.chmod(0o744)  # Still executable: same Git mode, different filesystem permissions.
                elif scenario == "untracked-mode":
                    target.chmod(0o755)
                else:
                    target.write_bytes(b"alpha\r\nbeta\r\ngamma\r\n")
                second = self.run_cli(None, *args, cwd=root)
                self.assertEqual(second.returncode, 1, "changed snapshot must reject old approval")
                self.assertNotEqual(first_report["eventHash"], json.loads(second.stdout)["eventHash"])
                self.assertNotIn("alpha", first.stdout + second.stdout)

    def test_non_git_modes_reject_git_only_flags(self):
        hook = dict(hook_event_name="PreToolUse", cwd=str(ROOT), tool_name="Write",
                    tool_input=dict(file_path="src/main.py", content="answer = 42"))
        for mode, data, code in (("--event", event(), 1), ("--hook-input", hook, 2)):
            for flag, value in (("--operation", "deploy"), ("--operation", "edit"),
                                ("--task-mode", "fix"), ("--task-mode", "unknown"), ("--risk", "security")):
                with self.subTest(mode=mode, flag=flag, value=value):
                    result = self.run_cli(data, mode, "-", flag, value)
                    self.assertEqual(result.returncode, code)
                    self.assertEqual(result.stdout, "")
                    self.assertIn("invalid", result.stderr)

    def test_git_mode_consumes_defaults_and_explicit_flags(self):
        with tempfile.TemporaryDirectory() as directory:
            subprocess.run(["git", "init", "-q", directory], check=True)
            subprocess.run(["git", "-C", directory, "-c", "user.name=Fixture", "-c",
                            "user.email=fixture@example.invalid", "commit", "--allow-empty", "-qm", "fixture"], check=True)
            safe = self.run_cli(None, "--git-diff", "HEAD", cwd=directory)
            self.assertEqual(safe.returncode, 0)
            for flag, value in (("--risk", "security"), ("--operation", "deploy")):
                result = self.run_cli(None, "--git-diff", "HEAD", flag, value, cwd=directory)
                self.assertEqual(result.returncode, 1)
                self.assertIn("high-risk-human-gate", result.stdout)
            target = Path(directory) / "tests/test_main.py"
            target.parent.mkdir()
            target.write_text("assert True\n")
            self.assertEqual(self.run_cli(None, "--git-diff", "HEAD", cwd=directory).returncode, 1)
            self.assertEqual(self.run_cli(None, "--git-diff", "HEAD", "--task-mode", "apply", cwd=directory).returncode, 0)

    def test_git_snapshot_unsupported_files_fail_closed(self):
        for kind in ("symlink", "directory", "binary"):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                subprocess.run(["git", "init", "-q", directory], check=True)
                target = root / "tracked.txt"
                target.write_text("original\n")
                subprocess.run(["git", "-C", directory, "add", "."], check=True)
                subprocess.run(["git", "-C", directory, "-c", "user.name=Fixture", "-c",
                                "user.email=fixture@example.invalid", "commit", "-qm", "fixture"], check=True)
                target.unlink()
                if kind == "symlink":
                    target.symlink_to(root / "missing-target")
                elif kind == "directory":
                    target.mkdir()
                else:
                    target.write_bytes(b"\0\1\2")
                result = self.run_cli(None, "--git-diff", "HEAD", cwd=root)
                self.assertEqual(result.returncode, 1)
                self.assertEqual(result.stdout, "")
                self.assertIn("content redacted", result.stderr)

    def test_hook_subdirectory_keeps_repository_path(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve() / "repo"
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            alias = root.parent / "repo-alias"
            alias.symlink_to(root, target_is_directory=True)
            for folder, filename, control in (("infra", "main.tf", "protected-path-edit"),
                                              ("tests", "helper.py", "fix-test-integrity")):
                (root / folder).mkdir()
                for entry in (root, alias):
                    for cwd in (entry, entry / folder):
                        for absolute in (True, False):
                            for tool, key in (("Write", "content"), ("Edit", "new_string")):
                                with self.subTest(folder=folder, alias=entry == alias, subdir=cwd != entry,
                                                  absolute=absolute, tool=tool):
                                    target = entry / folder / filename
                                    path = str(target) if absolute else str(target.relative_to(cwd))
                                    data = dict(hook_event_name="PreToolUse", cwd=str(cwd), tool_name=tool,
                                                tool_input=dict(file_path=path, **{key: "safe"}))
                                    result = self.run_cli(data, "--hook-input", "-")
                                    self.assertEqual(result.returncode, 0)
                                    self.assertIn('"permissionDecision": "ask"', result.stdout)
                                    self.assertIn(control, result.stdout)

    def test_hook_without_repository_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            data = dict(hook_event_name="PreToolUse", cwd=directory, tool_name="Write",
                        tool_input=dict(file_path="safe.txt", content="safe"))
            result = self.run_cli(data, "--hook-input", "-")
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, "")
            self.assertIn("content redacted", result.stderr)

    def test_hook_root_lookup_failures_are_bounded(self):
        data = dict(hook_event_name="PreToolUse", cwd=str(ROOT), tool_name="Write",
                    tool_input=dict(file_path="src/main.py", content="safe"))
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run([sys.executable, str(CHECKER), "--hook-input", "-"],
                                    input=json.dumps(data), text=True, capture_output=True,
                                    env={**os.environ, "PATH": directory})
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, "")
            self.assertIn("degraded", result.stderr)
            self.assertIn("Git", result.stderr)
            self.assertIn("human review", result.stderr)
        # Inject only the external timeout; real root/path logic remains under test.
        with patch.object(self.module.subprocess, "run", side_effect=subprocess.TimeoutExpired("git", 5)) as run:
            with self.assertRaises(ValueError):
                self.module.hook_event(data)
            self.assertEqual(run.call_args.kwargs["timeout"], 5)

    def test_git_execution_failures_report_degraded_without_echo(self):
        data = dict(hook_event_name="PreToolUse", cwd=str(ROOT), tool_name="Write",
                    tool_input=dict(file_path="src/main.py", content="safe"))
        failures = [subprocess.TimeoutExpired("untrusted-command", 5, stderr=b"private-diagnostic"),
                    subprocess.CompletedProcess(["git"], 128, b"", b"private-diagnostic")]
        for failure in failures:
            with self.subTest(kind=type(failure).__name__):
                stdout, stderr = io.StringIO(), io.StringIO()
                options = {"side_effect": failure} if isinstance(failure, Exception) else {"return_value": failure}
                with patch.object(self.module.subprocess, "run", **options), \
                     patch.object(sys, "argv", [str(CHECKER), "--hook-input", "-"]), \
                     patch.object(sys, "stdin", io.StringIO(json.dumps(data))), \
                     redirect_stdout(stdout), redirect_stderr(stderr):
                    code = self.module.main()
                self.assertEqual(code, 2)
                self.assertEqual(stdout.getvalue(), "")
                self.assertIn("degraded", stderr.getvalue())
                self.assertIn("Git", stderr.getvalue())
                self.assertIn("human review", stderr.getvalue())
                self.assertNotIn("private-diagnostic", stderr.getvalue())
                self.assertNotIn("untrusted-command", stderr.getvalue())

    def test_git_rejects_old_unsupported_modes(self):
        for kind in ("symlink", "submodule"):
            for operation in ("delete", "replace"):
                with self.subTest(kind=kind, operation=operation), tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    def git(*args):
                        return subprocess.run(["git", "-C", directory, *args], check=True, capture_output=True).stdout
                    def commit():
                        git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                            "commit", "--allow-empty", "-qm", "fixture")
                    git("init", "-q")
                    target = root / "old-file"
                    if kind == "symlink":
                        target.symlink_to("missing-target")
                        git("add", "old-file")
                    else:
                        commit()
                        oid = git("rev-parse", "HEAD").decode().strip()
                        git("update-index", "--add", "--cacheinfo", f"160000,{oid},old-file")
                    commit()
                    if kind == "symlink":
                        target.unlink()
                    else:
                        git("update-index", "--force-remove", "old-file")
                    if operation == "replace":
                        target.write_text("safe\n")
                    result = self.run_cli(None, "--git-diff", "HEAD", cwd=root)
                    self.assertEqual(result.returncode, 1)
                    self.assertEqual(result.stdout, "")
                    self.assertIn("content redacted", result.stderr)

    def test_official_harness_principles_contract(self):
        required = {
            "docs/harness-engineering.md": ["核对于", "codex-as-a-platform", "harness-design-long-running-apps", "控制面", "模型升级", "trace"],
            "docs/loop-engineering.md": ["恢复", "副作用", "预算", "当前状态"],
            "agents/workflows/full.md": ["恢复检查", "预算", "已发生副作用"],
            "agents/workflows/review.md": ["outcome", "trace", "self-review", "基线"],
            "evals/README.md": ["trace", "model", "policy", "outcome"],
        }
        for relative, markers in required.items():
            with self.subTest(file=relative):
                content = (ROOT / relative).read_text()
                for marker in markers:
                    self.assertIn(marker, content, f"{relative}: missing {marker}")

    def test_platform_support_is_not_adapter_readiness(self):
        content = (ROOT / "rules/security.md").read_text()
        for marker in ["平台支持", "仓库实现", "测试验证", "本地启用", "tool_input.command", "ask", "learn.chatgpt.com/docs/hooks"]:
            self.assertIn(marker, content)


if __name__ == "__main__":
    unittest.main()
