#!/usr/bin/env python3
"""Validate AI coding workflow eval cases and score optional external results."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from check_progressive_sdd import classify_activated, should_activate


class EvalError(Exception):
    pass


CASE_REQUIRED = ["id", "description", "prompt", "facts", "expected"]
EXPECTED_REQUIRED = ["tier", "modules", "humanGate", "writesBeforeContract"]
ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> object:
    if not path.is_file():
        raise EvalError(f"missing JSON file: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise EvalError(f"invalid JSON {path}: {exc}") from exc


def load_cases(cases_dir: Path) -> list[dict]:
    if not cases_dir.is_dir():
        raise EvalError(f"cases directory not found: {cases_dir}")
    cases: list[dict] = []
    for path in sorted(cases_dir.glob("*.json")):
        value = load_json(path)
        entries = value if isinstance(value, list) else [value]
        for entry in entries:
            if not isinstance(entry, dict):
                raise EvalError(f"{path}: every case must be an object")
            entry = dict(entry)
            entry["_source"] = str(path)
            cases.append(entry)
    return cases


def validate_schema_contract(schema: dict) -> None:
    if schema.get("$id") != "https://ai-code-copilot.dev/schemas/agent-eval-case-v1.json":
        raise EvalError("unexpected agent eval schema id")
    if schema.get("required") != CASE_REQUIRED:
        raise EvalError(
            f"schema case required fields drifted: expected {CASE_REQUIRED}, "
            f"got {schema.get('required')}"
        )
    expected_schema = schema.get("properties", {}).get("expected", {})
    if expected_schema.get("required") != EXPECTED_REQUIRED:
        raise EvalError(
            f"schema expected fields drifted: expected {EXPECTED_REQUIRED}, "
            f"got {expected_schema.get('required')}"
        )
    if schema.get("additionalProperties") is not False:
        raise EvalError("schema must reject unknown case fields")
    writes_schema = expected_schema.get("properties", {}).get("writesBeforeContract", {})
    if writes_schema.get("const") is not False:
        raise EvalError("schema must enforce writesBeforeContract=false")


def validate_case(case: dict, policy: dict) -> list[str]:
    errors: list[str] = []
    for field in CASE_REQUIRED:
        if field not in case:
            errors.append(f"missing field {field}")
    if errors:
        return errors
    if not isinstance(case["id"], str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]+", case["id"]):
        errors.append("id must be a string matching ^[a-z0-9][a-z0-9-]+$")
    if not isinstance(case["description"], str) or not case["description"].strip():
        errors.append("description must be a non-empty string")
    if not isinstance(case["prompt"], str) or not case["prompt"].strip():
        errors.append("prompt must be a non-empty string")
    unknown = set(case) - {"id", "description", "prompt", "facts", "expected", "_source"}
    if unknown:
        errors.append(f"unknown case fields: {sorted(unknown)}")
    if not isinstance(case["facts"], dict) or not isinstance(case["expected"], dict):
        return ["facts and expected must be objects"]
    expected = case["expected"]
    for field in EXPECTED_REQUIRED:
        if field not in expected:
            errors.append(f"expected missing field {field}")
    if errors:
        return errors

    if expected["tier"] not in {"native", "compact", "full"}:
        errors.append("expected tier must be native, compact, or full")
    if (not isinstance(expected["modules"], list)
            or not all(isinstance(module, str) for module in expected["modules"])):
        errors.append("expected modules must be an array of strings")
    if type(expected["humanGate"]) is not bool:
        errors.append("expected humanGate must be a boolean")
    if expected["writesBeforeContract"] is not False:
        errors.append("expected writesBeforeContract must be false")
    if ("capabilityStatus" in expected
            and expected["capabilityStatus"] not in {"available", "unsupported", "degraded"}):
        errors.append("expected capabilityStatus is invalid")
    if ("promotion" in expected
            and (not isinstance(expected["promotion"], str) or not expected["promotion"])):
        errors.append("expected promotion must be a non-empty string")
    if errors:
        return errors

    # Risk facts and detected activation signals describe the same boundary.
    # Normalize both before using main's two-step activation/tier oracle.
    facts = case["facts"]
    for field in ("signals", "risks", "unsupportedCapabilities"):
        value = facts.get(field, [])
        if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
            errors.append(f"facts {field} must be an array of strings")
    files = facts.get("files", 0)
    if type(files) is not int or files < 0:
        errors.append("facts files must be a non-negative integer")
    for field in ("acceptedResidualRisk", "multipleDeliverableGoals", "multipleReviewUnits"):
        if field in facts and type(facts[field]) is not bool:
            errors.append(f"facts {field} must be a boolean")
    for field in ("explicitIntent", "promotionFrom"):
        if field in facts and (not isinstance(facts[field], str) or not facts[field]):
            errors.append(f"facts {field} must be a non-empty string")
    if errors:
        return errors
    signals = set(facts.get("signals", [])) | set(facts.get("risks", []))
    risks = set(facts.get("risks", [])) | (signals & set(policy["tiers"]["full"]["riskCategories"]))
    route_facts = {**facts, "signals": list(signals), "risks": list(risks)}
    actual_tier = classify_activated(policy, route_facts) if should_activate(policy, route_facts) else "native"
    if expected["tier"] != actual_tier:
        errors.append(f"tier expected {expected['tier']}, policy oracle got {actual_tier}")
    eval_policy = policy["agentEvals"]
    required_modules = eval_policy["requiredModulesByTier"][actual_tier]
    for module in required_modules:
        if not (ROOT / module).is_file():
            errors.append(f"required module does not exist: {module}")
    if expected["modules"] != required_modules:
        errors.append(
            f"modules expected {expected['modules']}, policy requires {required_modules}"
        )
    human_gate = bool(
        risks
        & set(eval_policy["humanGateRiskCategories"])
    )
    if expected["humanGate"] is not human_gate:
        errors.append(f"humanGate expected {expected['humanGate']}, oracle got {human_gate}")
    if expected["writesBeforeContract"] is not eval_policy["writesBeforeContract"]:
        errors.append(
            "writesBeforeContract must remain false under No Contract, No Code"
        )
    unsupported = case["facts"].get("unsupportedCapabilities", [])
    if unsupported and expected.get("capabilityStatus") != "unsupported":
        errors.append("unsupported capabilities must be reported as unsupported")
    promotion_from = case["facts"].get("promotionFrom")
    if promotion_from:
        expected_promotion = f"{promotion_from}-to-{actual_tier}"
        if expected.get("promotion") != expected_promotion:
            errors.append(
                f"promotion expected {expected.get('promotion')}, oracle got {expected_promotion}"
            )
    return errors


def validate_cases(cases: list[dict], policy: dict) -> None:
    eval_policy = policy.get("agentEvals")
    if not isinstance(eval_policy, dict):
        raise EvalError("workflow policy missing agentEvals contract")
    minimum = int(eval_policy["minimumCases"])
    if len(cases) < minimum:
        raise EvalError(f"expected at least {minimum} eval cases, found {len(cases)}")
    seen: set[str] = set()
    failures: list[str] = []
    for case in cases:
        case_id = str(case.get("id", "<missing-id>"))
        if case_id in seen:
            failures.append(f"{case_id}: duplicate id")
        seen.add(case_id)
        failures.extend(f"{case_id}: {error}" for error in validate_case(case, policy))
    if failures:
        raise EvalError("offline case validation failed:\n" + "\n".join(failures))


def score_results(cases: list[dict], value: object) -> tuple[int, int]:
    if not isinstance(value, list):
        raise EvalError("external results root must be an array")
    results: dict[str, dict] = {}
    for entry in value:
        if not isinstance(entry, dict) or "caseId" not in entry:
            raise EvalError("each external result must be an object with caseId")
        case_id = str(entry["caseId"])
        if case_id in results:
            raise EvalError(f"duplicate external result for {case_id}")
        results[case_id] = entry

    failures: list[str] = []
    case_ids = {str(case["id"]) for case in cases}
    unknown_results = set(results) - case_ids
    for case_id in sorted(unknown_results):
        failures.append(f"{case_id}: external result has no matching eval case")
    for case in cases:
        case_id = str(case["id"])
        result = results.get(case_id)
        if result is None:
            failures.append(f"{case_id}: missing external result")
            continue
        expected = case["expected"]
        for field in ["tier", "modules", "humanGate", "writesBeforeContract"]:
            if result.get(field) != expected[field]:
                failures.append(
                    f"{case_id}: {field} expected {expected[field]!r}, got {result.get(field)!r}"
                )
        for field in ["capabilityStatus", "promotion"]:
            if field in expected and result.get(field) != expected[field]:
                failures.append(
                    f"{case_id}: {field} expected {expected[field]!r}, got {result.get(field)!r}"
                )
    if failures:
        raise EvalError("external result scoring failed:\n" + "\n".join(failures))
    return len(cases), len(failures)


def score_external_results(cases: list[dict], results_path: Path) -> tuple[int, int]:
    return score_results(cases, load_json(results_path))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--policy", type=Path, required=True)
    parser.add_argument("--schema", type=Path, default=Path("evals/schema.json"))
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--results", type=Path)
    parser.add_argument("--self-check-external", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        policy = load_json(args.policy)
        schema = load_json(args.schema)
        if not isinstance(policy, dict) or not isinstance(schema, dict):
            raise EvalError("policy and schema roots must be objects")
        validate_schema_contract(schema)
        cases = load_cases(args.cases)
        validate_cases(cases, policy)
        print(f"agent-evals: PASS offline policy oracle ({len(cases)} cases)")
        if args.self_check_external:
            expected_results = [
                {"caseId": case["id"], **case["expected"]} for case in cases
            ]
            count, _ = score_results(cases, expected_results)
            print(f"agent-evals: PASS external scorer self-check ({count} cases)")
        if args.results:
            count, _ = score_external_results(cases, args.results)
            print(f"agent-evals: PASS external results ({count} cases)")
        else:
            print(
                "agent-evals: live capability=external-results-required, "
                "mode=non-blocking"
            )
    except EvalError as exc:
        print(f"agent-evals: FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
