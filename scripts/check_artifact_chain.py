#!/usr/bin/env python3
"""Validate versioned ai-code-copilot artifact chains with no third-party deps."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


ARTIFACT_BLOCK = re.compile(r"<!--\s*artifact\s*\n(?P<body>.*?)\n-->", re.DOTALL)
SHA256 = re.compile(r"^sha256:[0-9a-f]{64}$")


class ValidationError(Exception):
    pass


@dataclass(frozen=True)
class Artifact:
    path: Path
    metadata: dict[str, object]

    @property
    def artifact_id(self) -> str:
        return str(self.metadata["artifactId"])

    @property
    def artifact_type(self) -> str:
        return str(self.metadata["artifactType"])


def load_json(path: Path) -> dict:
    if not path.is_file():
        raise ValidationError(f"missing JSON file: {path}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValidationError(f"invalid JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValidationError(f"JSON root must be an object: {path}")
    return value


def scalar(value: str) -> object:
    value = value.strip()
    if not value:
        return ""
    if value.startswith('"') and value.endswith('"'):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            pass
    if value.isdigit():
        return int(value)
    return value


def parse_key_values(body: str) -> dict[str, object]:
    result: dict[str, object] = {}
    for raw_line in body.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        if key in result:
            raise ValidationError(f"duplicate artifact metadata key: {key}")
        result[key] = scalar(value)
    return result


def parse_metadata(path: Path) -> dict[str, object] | None:
    text = path.read_text(encoding="utf-8")
    block = ARTIFACT_BLOCK.search(text)
    if block:
        return parse_key_values(block.group("body"))
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            values = parse_key_values(text[4:end])
            if "artifactVersion" in values:
                return values
    return None


def file_hash(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def artifact_policy(policy_path: Path) -> dict:
    policy = load_json(policy_path)
    artifacts = policy.get("artifacts")
    if not isinstance(artifacts, dict):
        raise ValidationError("workflow policy missing artifacts contract")
    return artifacts


def validate_artifact(artifact: Artifact, policy: dict) -> None:
    metadata = artifact.metadata
    missing = [field for field in policy["metadataFields"] if field not in metadata]
    if missing:
        raise ValidationError(
            f"{artifact.path}: artifact metadata missing fields: {', '.join(missing)}"
        )
    if metadata["artifactVersion"] != policy["version"]:
        raise ValidationError(
            f"{artifact.artifact_id}: artifactVersion expected {policy['version']}, "
            f"got {metadata['artifactVersion']}"
        )
    if artifact.artifact_type not in policy["types"]:
        raise ValidationError(
            f"{artifact.artifact_id}: unknown artifactType {artifact.artifact_type}"
        )
    status = str(metadata["artifactStatus"])
    if status not in policy["statusTransitions"]:
        raise ValidationError(f"{artifact.artifact_id}: unknown artifactStatus {status}")
    source = str(metadata["sourceOfTruth"])
    if source not in policy["sourceOfTruthValues"]:
        raise ValidationError(f"{artifact.artifact_id}: unknown sourceOfTruth {source}")
    source_ref = str(metadata["sourceRef"])
    source_revision = str(metadata["sourceRevision"])
    if source == "repository":
        if source_ref != "self":
            raise ValidationError(
                f"{artifact.artifact_id}: repository sourceRef must be self"
            )
        if source_revision != "working-tree" and not re.fullmatch(
            r"git:[0-9a-f]{7,40}", source_revision
        ):
            raise ValidationError(
                f"{artifact.artifact_id}: repository sourceRevision must be "
                "working-tree or git:<sha>"
            )
        if status in {"finished", "archived"} and source_revision == "working-tree":
            raise ValidationError(
                f"{artifact.artifact_id}: {status} repository artifact requires git:<sha> revision"
            )
    elif source_ref == "none" or source_revision == "none":
        raise ValidationError(
            f"{artifact.artifact_id}: {source} source requires sourceRef and sourceRevision"
        )


def validate_change(change_dir: Path, policy: dict, require_chain: bool = False) -> str:
    if not change_dir.is_dir():
        raise ValidationError(f"change directory not found: {change_dir}")
    artifacts: list[Artifact] = []
    for path in sorted(change_dir.rglob("*.md")):
        metadata = parse_metadata(path)
        if metadata is not None:
            artifact = Artifact(path=path, metadata=metadata)
            validate_artifact(artifact, policy)
            artifacts.append(artifact)
    if not artifacts:
        if require_chain:
            raise ValidationError(f"{change_dir}: artifact chain required but metadata is missing")
        return "SKIP legacy change without artifact metadata"

    by_id: dict[str, Artifact] = {}
    for artifact in artifacts:
        if artifact.artifact_id in by_id:
            raise ValidationError(f"duplicate artifactId: {artifact.artifact_id}")
        by_id[artifact.artifact_id] = artifact

    for artifact in artifacts:
        metadata = artifact.metadata
        upstream_id = str(metadata["upstream"])
        upstream_hash = str(metadata["upstreamHash"])
        allowed_types = policy["types"][artifact.artifact_type]["allowedUpstreamTypes"]
        if upstream_id == "none":
            if allowed_types:
                raise ValidationError(
                    f"{artifact.artifact_id}: upstream required; allowed types={allowed_types}"
                )
            if upstream_hash != "none":
                raise ValidationError(
                    f"{artifact.artifact_id}: upstreamHash must be none without upstream"
                )
            continue
        if upstream_id not in by_id:
            raise ValidationError(
                f"{artifact.artifact_id}: upstream artifact not found: {upstream_id}"
            )
        upstream = by_id[upstream_id]
        if upstream.artifact_type not in allowed_types:
            raise ValidationError(
                f"{artifact.artifact_id}: upstream type {upstream.artifact_type} "
                f"not allowed for {artifact.artifact_type}"
            )
        status = str(metadata["artifactStatus"])
        if upstream_hash == "pending" and status == "draft":
            continue
        if not SHA256.fullmatch(upstream_hash):
            raise ValidationError(
                f"{artifact.artifact_id}: upstreamHash must be sha256:<64 hex> or draft pending"
            )
        actual_hash = file_hash(upstream.path)
        if upstream_hash != actual_hash:
            raise ValidationError(
                f"{artifact.artifact_id}: upstream hash drift for {upstream_id}; "
                f"expected {upstream_hash}, actual {actual_hash}"
            )
    return f"PASS {len(artifacts)} artifacts"


def validate_transition(policy: dict, transition: str) -> str:
    parts = transition.split(":")
    if len(parts) != 2:
        raise ValidationError("transition must use FROM:TO")
    previous, current = parts
    transitions = policy["statusTransitions"]
    if previous not in transitions:
        raise ValidationError(f"unknown transition source status: {previous}")
    if current not in transitions[previous]:
        raise ValidationError(f"illegal artifact transition: {previous} -> {current}")
    return f"PASS transition {previous} -> {current}"


def validate_templates(template_dir: Path, policy: dict) -> str:
    type_to_file = {
        "design-brief": "design-brief.md",
        "quick-card": "quick-card.md",
        "roadmap": "roadmap.md",
        "spec": "spec.md",
        "tasks": "tasks.md",
        "test-spec": "test-spec.md",
        "log": "log.md",
        "summary": "summary.md",
        "log-summary": "log-summary.md",
    }
    for artifact_type, filename in type_to_file.items():
        path = template_dir / filename
        if not path.is_file():
            raise ValidationError(f"artifact template missing: {path}")
        metadata = parse_metadata(path)
        if metadata is None:
            raise ValidationError(f"artifact template missing metadata: {path}")
        missing = [field for field in policy["metadataFields"] if field not in metadata]
        if missing:
            raise ValidationError(f"{path}: template metadata missing {', '.join(missing)}")
        if str(metadata["artifactType"]) != artifact_type:
            raise ValidationError(
                f"{path}: artifactType expected {artifact_type}, got {metadata['artifactType']}"
            )
    return f"PASS {len(type_to_file)} artifact templates"


def validate_fixtures(fixtures_dir: Path, policy: dict) -> str:
    if not fixtures_dir.is_dir():
        raise ValidationError(f"fixtures directory not found: {fixtures_dir}")
    count = 0
    for fixture_dir in sorted(path for path in fixtures_dir.iterdir() if path.is_dir()):
        expected_path = fixture_dir / "expected.json"
        expected = load_json(expected_path)
        should_pass = bool(expected.get("pass"))
        require_chain = bool(expected.get("requireChain", False))
        try:
            result = validate_change(fixture_dir, policy, require_chain=require_chain)
        except ValidationError as exc:
            if should_pass:
                raise ValidationError(f"fixture {fixture_dir.name} expected PASS: {exc}") from exc
            marker = str(expected.get("errorContains", ""))
            if marker and marker not in str(exc):
                raise ValidationError(
                    f"fixture {fixture_dir.name} expected error containing {marker!r}, got {exc!s}"
                ) from exc
        else:
            if not should_pass:
                raise ValidationError(
                    f"fixture {fixture_dir.name} expected FAIL, got {result}"
                )
        count += 1
    if count == 0:
        raise ValidationError("no artifact-chain fixtures found")
    return f"PASS {count} artifact-chain fixtures"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--policy", type=Path, required=True)
    parser.add_argument("--change-dir", type=Path)
    parser.add_argument("--fixtures", type=Path)
    parser.add_argument("--templates", type=Path)
    parser.add_argument("--require-chain", action="store_true")
    parser.add_argument("--transition")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        policy = artifact_policy(args.policy)
        actions = 0
        if args.change_dir:
            print(validate_change(args.change_dir, policy, args.require_chain))
            actions += 1
        if args.fixtures:
            print(validate_fixtures(args.fixtures, policy))
            actions += 1
        if args.templates:
            print(validate_templates(args.templates, policy))
            actions += 1
        if args.transition:
            print(validate_transition(policy, args.transition))
            actions += 1
        if actions == 0:
            raise ValidationError("select --change-dir, --fixtures, --templates, or --transition")
    except ValidationError as exc:
        print(f"artifact-chain: FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
