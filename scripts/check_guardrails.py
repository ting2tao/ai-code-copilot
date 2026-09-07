#!/usr/bin/env python3
"""Bounded, offline guardrail checks. Not an authorization service or full DLP scanner."""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
MODES = {"apply", "fix", "fix-ci", "review", "finish", "unknown"}
OPERATIONS = {"edit", "commit", "review", "publish", "deploy"}
RISKS = {"public-api", "schema", "database", "dependency", "ci", "deployment",
         "generated-artifact", "security", "permission", "authentication",
         "sensitive-data", "money", "state-machine", "cross-module-business-rule",
         "accepted-residual-risk", "production"}


class GitUnavailable(ValueError):
    """Git could not provide coverage; messages contain fixed, safe reasons only."""


def require(condition, field):
    if not condition:
        # Never echo untrusted values, lines, or JSON parse errors.
        raise ValueError("invalid " + field)


def read_json(path):
    return json.loads(sys.stdin.read() if str(path) == "-" else Path(path).read_text())


def load_policy(path):
    policy = read_json(path)
    require(isinstance(policy, dict) and type(policy.get("version")) is int
            and policy["version"] == 1, "policy version")
    require(policy.get("layers") == ["advisory", "deterministic", "human"], "policy layers")
    controls = policy.get("controls")
    require(isinstance(controls, list), "policy controls")
    expected = {
        "secret-diff": ("deterministic", "block", False, ["addedLinePatterns"]),
        "sensitive-data-diff": ("deterministic", "block", False, ["addedLinePatterns"]),
        "protected-path-edit": ("deterministic", "ask", True, ["paths"]),
        "fix-test-integrity": ("deterministic", "ask", True, ["paths", "taskModes"]),
        "high-risk-human-gate": ("human", "ask", True, ["risks", "operations"]),
        "review-context": ("advisory", "warn", False, ["operations"]),
    }
    require(all(isinstance(c, dict) for c in controls), "policy control")
    require({c.get("id") for c in controls} == set(expected) and len(controls) == len(expected), "policy control IDs")
    for control in controls:
        for key in ("owner", "approvalRoute", "evidence"):
            require(isinstance(control.get(key), str) and bool(control[key]), "policy " + key)
        layer, action, approval, selectors = expected[control["id"]]
        require(control.get("layer") == layer and control.get("action") == action
                and control.get("allowWithApproval") is approval, "policy control semantics")
        for selector in selectors:
            values = control.get(selector)
            require(isinstance(values, list) and bool(values)
                    and all(isinstance(value, str) and bool(value) for value in values), "policy selector")
        allowed_selectors = {"risks": RISKS, "operations": OPERATIONS, "taskModes": MODES}
        for selector, allowed in allowed_selectors.items():
            if selector in control:
                require(set(control[selector]).issubset(allowed), "policy " + selector)
        for pattern in control.get("addedLinePatterns", []):
            re.compile(pattern)
    require(isinstance(policy.get("adapters"), dict), "policy adapters")
    for adapter in ("local-cli", "ci", "claude-pretooluse", "codex-repo-hook"):
        capability = policy.get("adapters", {}).get(adapter, {})
        require(isinstance(capability, dict) and bool(capability.get("fallback"))
                and bool(capability.get("coverage")) and capability.get("status")
                in {"supported", "supported-with-runtime", "unavailable"}, "adapter capability")
    require(policy["adapters"]["codex-repo-hook"].get("status") == "unavailable", "Codex capability")
    return policy


def valid_path(path):
    require(isinstance(path, str) and bool(path) and "\\" not in path
            and not any(ord(c) < 32 for c in path), "relative path")
    parsed = PurePosixPath(path)
    require(not parsed.is_absolute() and ".." not in parsed.parts
            and str(parsed) == path and path != ".", "relative path")


def validate_event(event, policy):
    require(isinstance(event, dict), "event")
    require(type(event.get("eventVersion")) is int and event["eventVersion"] == 1, "event version")
    require(event.get("operation") in OPERATIONS and event.get("taskMode") in MODES, "event operation/taskMode")
    for key in ("changedPaths", "diffAddedLines", "risks", "approvals"):
        require(isinstance(event.get(key), list), "event " + key)
    for path in event["changedPaths"]:
        valid_path(path)
    require(all(isinstance(risk, str) and risk in RISKS for risk in event["risks"]), "event risks")
    for added in event["diffAddedLines"]:
        require(isinstance(added, dict) and added.get("path") in event["changedPaths"]
                and isinstance(added.get("line"), str), "event added line")
    ids = {c["id"] for c in policy["controls"]}
    for approval in event["approvals"]:
        require(isinstance(approval, dict) and approval.get("controlId") in ids, "approval control")
        for key in ("reviewer", "evidenceRef", "eventHash"):
            require(isinstance(approval.get(key), str) and bool(approval[key].strip()), "approval " + key)


def matches(path, patterns):
    return any(fnmatch.fnmatchcase(path, pattern) or
               (pattern.startswith("**/") and fnmatch.fnmatchcase(path, pattern[3:]))
               for pattern in patterns)


def evaluate(policy, event):
    validate_event(event, policy)
    body = {k: v for k, v in event.items() if k != "approvals"}
    digest = "sha256:" + hashlib.sha256(json.dumps(body, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    approved = {a["controlId"] for a in event["approvals"] if a["eventHash"] == digest}
    decisions = []
    for control in policy["controls"]:
        paths = set()
        if "addedLinePatterns" in control:
            for added in event["diffAddedLines"]:
                if any(re.search(p, added["line"]) for p in control["addedLinePatterns"]):
                    paths.add(added["path"])
        if "paths" in control and event["taskMode"] in control.get("taskModes", MODES):
            paths.update(p for p in event["changedPaths"] if matches(p, control["paths"]))
        if (set(event["risks"]) & set(control.get("risks", [])) or
                event["operation"] in control.get("operations", [])):
            paths.add("<operation>")
        for path in sorted(paths):
            action = "approved" if control["allowWithApproval"] and control["id"] in approved else control["action"]
            decisions.append(dict(controlId=control["id"], layer=control["layer"], action=action,
                                  path=path, owner=control["owner"], approvalRoute=control["approvalRoute"]))
    return dict(eventVersion=1, eventHash=digest,
                passed=not any(d["action"] in {"block", "ask"} for d in decisions), decisions=decisions,
                approvalTrust="caller-attested; verify human evidence independently")


def hook_event(payload):
    require(isinstance(payload, dict) and payload.get("hook_event_name") == "PreToolUse", "hook event")
    name, params = payload.get("tool_name"), payload.get("tool_input")
    require(name in {"Write", "Edit"} and isinstance(params, dict), "hook tool")
    require(isinstance(payload.get("cwd"), str) and Path(payload["cwd"]).is_absolute(), "hook cwd")
    logical_cwd = Path(payload["cwd"])
    root = Path(git_output(logical_cwd, "rev-parse", "--show-toplevel", timeout=5).decode().strip()).resolve()
    require(logical_cwd.resolve().is_relative_to(root), "hook cwd outside repository")
    # Find the lexical spelling of the actual worktree root, including root aliases.
    logical_root = next((p for p in (logical_cwd, *logical_cwd.parents) if p.resolve() == root), None)
    require(logical_root is not None, "hook ambiguous repository root")
    raw_path = params.get("file_path")
    require(isinstance(raw_path, str) and bool(raw_path), "hook path")
    target = Path(raw_path)
    require(".." not in target.parts, "hook traversal")
    logical_target = logical_cwd / target if not target.is_absolute() else target
    target = logical_target.resolve()
    require(target.is_relative_to(root), "hook outside-root path")
    # Evaluate both lexical and resolved paths; a symlink must not erase either boundary.
    lexical_root = logical_root if logical_target.is_relative_to(logical_root) else root
    require(logical_target.is_relative_to(lexical_root), "hook lexical outside-root path")
    paths = sorted({logical_target.relative_to(lexical_root).as_posix(), target.relative_to(root).as_posix()})
    content = params.get("content" if name == "Write" else "new_string")
    require(isinstance(content, str), "hook content")
    # Unknown task mode conservatively asks on tests. Never trust embedded approvals.
    return dict(eventVersion=1, operation="edit", taskMode="unknown", changedPaths=paths,
                diffAddedLines=[dict(path=path, line=line) for path in paths for line in content.splitlines()], risks=[], approvals=[])


def git_output(root: Path, *args: str, timeout: int | None = None) -> bytes:
    try:
        result = subprocess.run(["git", "-C", str(root), *args], capture_output=True, check=False, timeout=timeout)
    except subprocess.TimeoutExpired:
        raise GitUnavailable("Git query timed out") from None
    except OSError:
        raise GitUnavailable("Git executable unavailable") from None
    if result.returncode != 0:
        raise GitUnavailable("Git query failed; check repository/ref and runtime")
    return result.stdout


def git_event(base, operation, mode, risks):
    root = Path(git_output(Path.cwd(), "rev-parse", "--show-toplevel").decode().strip()).resolve()
    require(bool(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_./~^{}-]*", base)), "git base")
    revision = git_output(root, "rev-parse", "--verify", base + "^{commit}").decode().strip()
    diff_args = ("--literal-pathspecs", "-c", "core.filemode=true", "diff", "--no-ext-diff",
                 "--no-textconv", "--no-renames", "--no-color", "--no-relative", "--ignore-submodules=none")
    paths = sorted(git_output(root, *diff_args, "--name-only", "-z", revision, "--").decode().split("\0")[:-1])
    untracked = sorted(git_output(root, "ls-files", "--others", "--exclude-standard", "-z").decode().split("\0")[:-1])
    added = []
    snapshot = dict(baseRevision=revision, patches=[], files=[])
    for path in paths:
        valid_path(path)
        # Check the old side too: deleted/replaced symlinks and gitlinks have no
        # unsupported current filesystem object left for lstat() to detect.
        old_entries = git_output(root, "--literal-pathspecs", "ls-tree", "-z", revision, "--", path).split(b"\0")[:-1]
        require(all(entry.split(b" ", 1)[0] in {b"100644", b"100755"} for entry in old_entries),
                "unsupported base file type")
        patch_bytes = git_output(root, *diff_args, "--unified=0", "--full-index",
                                 "--diff-algorithm=myers", "--no-indent-heuristic", revision, "--", path)
        snapshot["patches"].append(dict(path=path, hash=hashlib.sha256(patch_bytes).hexdigest()))
        patch = patch_bytes.decode()
        in_hunk = False
        for line in patch.splitlines():
            if line.startswith("@@ "):
                in_hunk = True
            elif not in_hunk and (line == "GIT binary patch" or line.startswith("Binary files ")):
                require(False, "binary diff requires manual review")
            elif in_hunk and line.startswith("+"):
                added.append(dict(path=path, line=line[1:]))
    for path in sorted(set(paths + untracked)):
        valid_path(path)
        target = root / path
        require(not target.is_symlink() and target.resolve() == target, "unsupported symlink path")
        try:
            metadata = target.lstat()
        except FileNotFoundError:
            require(path in paths and path not in untracked, "missing untracked file")
            snapshot["files"].append(dict(path=path, deleted=True))
            continue
        require(stat.S_ISREG(metadata.st_mode), "unsupported non-file")
        content_bytes = target.read_bytes()
        content = content_bytes.decode("utf-8")
        require("\0" not in content, "binary untracked file requires manual review")
        snapshot["files"].append(dict(path=path, mode=stat.S_IMODE(metadata.st_mode),
                                      hash=hashlib.sha256(content_bytes).hexdigest()))
        if path in untracked:
            added.extend(dict(path=path, line=line) for line in content.splitlines())
    # Bind all diff semantics, not just the lossy added-line scanner input.
    # Raw bytes additionally preserve newline/filter differences and filesystem modes.
    snapshot_hash = "sha256:" + hashlib.sha256(json.dumps(snapshot, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return dict(eventVersion=1, operation=operation, taskMode=mode, changedPaths=sorted(set(paths + untracked)),
                diffAddedLines=added, risks=risks, approvals=[], gitSnapshotHash=snapshot_hash)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--policy", type=Path, default=ROOT / "config/guardrail-policy.json")
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--event", help="event JSON file or - for stdin")
    modes.add_argument("--hook-input", help="Claude PreToolUse JSON file or - for stdin")
    modes.add_argument("--git-diff", metavar="BASE", help="single commit/ref to worktree, including untracked text")
    parser.add_argument("--operation", choices=sorted(OPERATIONS), help="Git mode only (default: edit)")
    parser.add_argument("--task-mode", choices=sorted(MODES), help="Git mode only (default: unknown)")
    parser.add_argument("--risk", action="append", choices=sorted(RISKS), help="Git mode only; repeat for multiple risks")
    parser.add_argument("--approvals", type=Path, help="human-supplied event-bound approval JSON list (local/CI only)")
    args = parser.parse_args()
    try:
        require(args.git_diff is not None or all(value is None for value in
                (args.operation, args.task_mode, args.risk)), "Git-only flags with non-Git input")
        policy = load_policy(args.policy)
        if args.hook_input:
            require(args.approvals is None, "hook approval override")
            data = hook_event(read_json(args.hook_input))
        elif args.git_diff:
            data = git_event(args.git_diff, args.operation or "edit", args.task_mode or "unknown", args.risk or [])
        else:
            data = read_json(args.event)
        if args.approvals:
            data["approvals"] = read_json(args.approvals)
        report = evaluate(policy, data)
        if args.hook_input:
            blocked = [d for d in report["decisions"] if d["action"] == "block"]
            if blocked:
                print(json.dumps(blocked), file=sys.stderr)
                return 2
            asked = [d for d in report["decisions"] if d["action"] == "ask"]
            if asked:
                print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "ask", "permissionDecisionReason": json.dumps(asked)}}))
            return 0  # No allow: never skip the platform's permission checks.
        print(json.dumps(report, ensure_ascii=True))
        return 0 if report["passed"] else 1
    except GitUnavailable as error:
        print(f"guardrails: degraded ({error}); blocked. Restore Git/runtime or explicitly use trusted event input with human review (content redacted)", file=sys.stderr)
        return 2 if args.hook_input else 1
    except (ValueError, TypeError, KeyError, OSError, re.error):
        print("guardrails: invalid input/policy or unsupported diff; correct input or request human review (content redacted)", file=sys.stderr)
        return 2 if args.hook_input else 1


if __name__ == "__main__":
    sys.exit(main())
