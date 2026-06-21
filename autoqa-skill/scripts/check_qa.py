#!/usr/bin/env python3
"""Validate AutoQA artifacts and execute their declared commands safely."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ALLOWED_CASE_CLASSES = {
    "happy",
    "negative",
    "boundary",
    "state",
    "permission",
    "dependency",
    "idempotency",
    "concurrency",
    "recovery",
}
ALLOWED_FLOW_VARIANTS = {"happy", "alternate", "failure"}
ALLOWED_SEVERITIES = {"P0", "P1", "P2", "P3"}
ALLOWED_HUMAN_STATUSES = {"pending", "pass", "fail", "blocked"}
ALLOWED_DEFECT_STATUSES = {"open", "fixed", "accepted"}
PHASES = ("plan", "automated", "release")
REQUIRED_DOC_MARKERS = {
    "QA-PLAN.md": {
        "qa-plan",
        "scope",
        "governance-sources",
        "risk",
        "best-practice",
        "environments",
        "responsibilities",
        "exit-criteria",
    },
    "QA-MATRIX.md": {
        "qa-matrix",
        "requirements",
        "file-gates",
        "module-boundaries",
        "business-flows",
        "fault-sensitivity",
        "residual-risk",
    },
    "HUMAN-E2E.md": {
        "human-e2e",
        "instructions",
        "environment",
        "checks",
        "defects",
        "sign-off",
    },
}
PLACEHOLDER_TOKENS = ("REPLACE_ME", "TODO", "TBD")


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Project root")
    parser.add_argument("--manifest", default="docs/QA/qa-manifest.json")
    parser.add_argument("--phase", choices=PHASES, default="plan")
    parser.add_argument("--run", action="store_true", help="Run commands required by the phase")
    return parser.parse_args()


def load_json(path: Path, report: Report) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        report.error(f"Missing manifest: {path}")
        return {}
    except json.JSONDecodeError as exc:
        report.error(f"Invalid JSON in {path}: {exc}")
        return {}
    if not isinstance(value, dict):
        report.error("Manifest root must be a JSON object")
        return {}
    return value


def is_nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def contains_placeholder(value: Any) -> bool:
    if isinstance(value, str):
        upper = value.upper()
        return any(token in upper for token in PLACEHOLDER_TOKENS)
    if isinstance(value, list):
        return any(contains_placeholder(item) for item in value)
    if isinstance(value, dict):
        return any(contains_placeholder(item) for item in value.values())
    return False


def as_list(value: Any, label: str, report: Report) -> list[Any]:
    if not isinstance(value, list):
        report.error(f"{label} must be a list")
        return []
    return value


def collect_unique(items: list[Any], label: str, report: Report) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            report.error(f"{label}[{index}] must be an object")
            continue
        item_id = item.get("id")
        if not is_nonempty_string(item_id):
            report.error(f"{label}[{index}] needs a non-empty id")
            continue
        if item_id in result:
            report.error(f"Duplicate {label} id: {item_id}")
            continue
        result[item_id] = item
    return result


def safe_workdir(root: Path, raw: Any, label: str, report: Report) -> Path:
    if not is_nonempty_string(raw):
        report.error(f"{label}.cwd must be a non-empty relative path")
        return root
    candidate = (root / raw).resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        report.error(f"{label}.cwd escapes the project root: {raw}")
        return root
    if not candidate.is_dir():
        report.error(f"{label}.cwd is not a directory: {raw}")
    return candidate


def validate_docs(root: Path, report: Report) -> None:
    qa_dir = root / "docs" / "QA"
    for filename, required in REQUIRED_DOC_MARKERS.items():
        path = qa_dir / filename
        if not path.is_file():
            report.error(f"Missing QA document: {path.relative_to(root)}")
            continue
        text = path.read_text(encoding="utf-8")
        found = set()
        for line in text.splitlines():
            line = line.strip()
            prefix = "<!-- autoqa:document:"
            section_prefix = "<!-- autoqa:section:"
            if line.startswith(prefix) and line.endswith(" -->"):
                found.add(line[len(prefix) : -len(" -->")])
            if line.startswith(section_prefix) and line.endswith(" -->"):
                found.add(line[len(section_prefix) : -len(" -->")])
        missing = sorted(required - found)
        if missing:
            report.error(f"{filename} is missing AutoQA markers: {', '.join(missing)}")
        if any(token in text.upper() for token in PLACEHOLDER_TOKENS):
            report.error(f"{filename} still contains placeholder text")


def validate_references(
    values: Any,
    known: set[str],
    label: str,
    report: Report,
    allow_empty: bool = False,
) -> set[str]:
    items = as_list(values, label, report)
    result = {item for item in items if is_nonempty_string(item)}
    if len(result) != len(items):
        report.error(f"{label} must contain unique non-empty strings")
    if not result and not allow_empty:
        report.error(f"{label} must not be empty")
    unknown = sorted(result - known)
    if unknown:
        report.error(f"{label} references unknown ids: {', '.join(unknown)}")
    return result


def command_fingerprint(command: dict[str, Any]) -> str:
    relevant = {
        "argv": command.get("argv"),
        "cwd": command.get("cwd", "."),
        "env": command.get("env", {}),
        "timeout_seconds": command.get("timeout_seconds", 300),
    }
    raw = json.dumps(relevant, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def validate_manifest(manifest: dict[str, Any], root: Path, report: Report) -> dict[str, Any]:
    if manifest.get("schema_version") != 1:
        report.error("schema_version must be 1")
    if not is_nonempty_string(manifest.get("project")):
        report.error("project must be a non-empty string")
    if contains_placeholder(manifest):
        report.error("qa-manifest.json still contains placeholder text")

    governance = as_list(manifest.get("governance"), "governance", report)
    if not governance:
        report.error("governance must name at least one source or assumption document")
    for index, item in enumerate(governance):
        if not isinstance(item, dict) or not is_nonempty_string(item.get("path")):
            report.error(f"governance[{index}] needs path and kind")
        elif not is_nonempty_string(item.get("kind")):
            report.error(f"governance[{index}].kind must be non-empty")

    requirements = collect_unique(
        as_list(manifest.get("requirements"), "requirements", report), "requirements", report
    )
    if not requirements:
        report.error("requirements must not be empty")
    for req_id, req in requirements.items():
        if not is_nonempty_string(req.get("description")) or not is_nonempty_string(req.get("source")):
            report.error(f"requirement {req_id} needs description and source")

    commands = collect_unique(as_list(manifest.get("commands"), "commands", report), "commands", report)
    for command_id, command in commands.items():
        argv = command.get("argv")
        if not isinstance(argv, list) or not argv or not all(is_nonempty_string(arg) for arg in argv):
            report.error(f"command {command_id}.argv must be a non-empty string array")
        safe_workdir(root, command.get("cwd", "."), f"command {command_id}", report)
        timeout = command.get("timeout_seconds", 300)
        if not isinstance(timeout, int) or not 1 <= timeout <= 3600:
            report.error(f"command {command_id}.timeout_seconds must be 1..3600")
        phases = command.get("required_phases", ["automated", "release"])
        if not isinstance(phases, list) or not phases or any(phase not in PHASES[1:] for phase in phases):
            report.error(f"command {command_id}.required_phases must use automated/release")
        env = command.get("env", {})
        if not isinstance(env, dict) or not all(
            is_nonempty_string(key) and isinstance(value, str) for key, value in env.items()
        ):
            report.error(f"command {command_id}.env must be a string map")

    command_ids = set(commands)
    requirement_ids = set(requirements)
    traced_requirements: set[str] = set()
    required_commands: set[str] = set()

    source_files = as_list(manifest.get("source_files"), "source_files", report)
    if not source_files:
        report.error("source_files must record every changed program file")
    seen_paths: set[str] = set()
    for index, source in enumerate(source_files):
        label = f"source_files[{index}]"
        if not isinstance(source, dict):
            report.error(f"{label} must be an object")
            continue
        path = source.get("path")
        if not is_nonempty_string(path):
            report.error(f"{label}.path must be non-empty")
        elif path in seen_paths:
            report.error(f"Duplicate source file path: {path}")
        else:
            seen_paths.add(path)
        kind = source.get("kind")
        if kind not in {"executable", "declarative"}:
            report.error(f"{label}.kind must be executable or declarative")
        refs = validate_references(
            source.get("command_ids", []), command_ids, f"{label}.command_ids", report, allow_empty=True
        )
        required_commands.update(refs)
        if kind == "executable" and not refs:
            report.error(f"{label} is executable and needs a narrow smoke command")
        if kind == "declarative" and not refs and not is_nonempty_string(source.get("coverage_reason")):
            report.error(f"{label} is declarative and needs command_ids or coverage_reason")

    modules = collect_unique(as_list(manifest.get("modules"), "modules", report), "modules", report)
    if not modules:
        report.error("modules must not be empty")
    all_case_ids: set[str] = set()
    for module_id, module in modules.items():
        if not is_nonempty_string(module.get("description")):
            report.error(f"module {module_id} needs a description")
        entries = collect_unique(as_list(module.get("entries"), f"module {module_id}.entries", report), "entries", report)
        exits = collect_unique(as_list(module.get("exits"), f"module {module_id}.exits", report), "exits", report)
        if not entries or not exits:
            report.error(f"module {module_id} needs at least one entry and exit")
        for boundary_label, boundaries in (("entry", entries), ("exit", exits)):
            for boundary_id, boundary in boundaries.items():
                if not is_nonempty_string(boundary.get("description")):
                    report.error(f"module {module_id} {boundary_label} {boundary_id} needs a description")

        applicable_raw = as_list(module.get("applicable_classes"), f"module {module_id}.applicable_classes", report)
        applicable = {value for value in applicable_raw if value in ALLOWED_CASE_CLASSES}
        if len(applicable) != len(applicable_raw):
            report.error(f"module {module_id} has unknown or duplicate applicable_classes")
        if "happy" not in applicable:
            report.error(f"module {module_id} must include happy in applicable_classes")
        if applicable == {"happy"} and not is_nonempty_string(module.get("non_happy_exemption")):
            report.error(f"module {module_id} needs a non-happy class or a non_happy_exemption")

        cases = as_list(module.get("cases"), f"module {module_id}.cases", report)
        covered_entries: set[str] = set()
        covered_exits: set[str] = set()
        covered_classes: set[str] = set()
        for index, case in enumerate(cases):
            label = f"module {module_id}.cases[{index}]"
            if not isinstance(case, dict):
                report.error(f"{label} must be an object")
                continue
            case_id = case.get("id")
            if not is_nonempty_string(case_id):
                report.error(f"{label} needs an id")
            elif case_id in all_case_ids:
                report.error(f"Duplicate case id: {case_id}")
            else:
                all_case_ids.add(case_id)
            rule = case.get("business_rule")
            if not is_nonempty_string(rule) or len(rule.strip()) < 12:
                report.error(f"{label}.business_rule must describe observable business behavior")
            case_class = case.get("class")
            if case_class not in applicable:
                report.error(f"{label}.class must be declared in applicable_classes")
            else:
                covered_classes.add(case_class)
            covered_entries.update(
                validate_references(case.get("entry_ids"), set(entries), f"{label}.entry_ids", report)
            )
            covered_exits.update(
                validate_references(case.get("exit_ids"), set(exits), f"{label}.exit_ids", report)
            )
            traced_requirements.update(
                validate_references(
                    case.get("requirement_ids"), requirement_ids, f"{label}.requirement_ids", report
                )
            )
            refs = validate_references(
                case.get("command_ids"), command_ids, f"{label}.command_ids", report
            )
            required_commands.update(refs)
        missing_entries = sorted(set(entries) - covered_entries)
        missing_exits = sorted(set(exits) - covered_exits)
        missing_classes = sorted(applicable - covered_classes)
        if missing_entries:
            report.error(f"module {module_id} has uncovered entries: {', '.join(missing_entries)}")
        if missing_exits:
            report.error(f"module {module_id} has uncovered exits: {', '.join(missing_exits)}")
        if missing_classes:
            report.error(f"module {module_id} has uncovered case classes: {', '.join(missing_classes)}")

    flows = collect_unique(as_list(manifest.get("flows"), "flows", report), "flows", report)
    if not flows:
        report.error("flows must not be empty")
    flow_variants: set[str] = set()
    for flow_id, flow in flows.items():
        if not is_nonempty_string(flow.get("name")):
            report.error(f"flow {flow_id} needs a business-facing name")
        variant = flow.get("variant")
        if variant not in ALLOWED_FLOW_VARIANTS:
            report.error(f"flow {flow_id}.variant must be happy, alternate, or failure")
        else:
            flow_variants.add(variant)
        traced_requirements.update(
            validate_references(
                flow.get("requirement_ids"), requirement_ids, f"flow {flow_id}.requirement_ids", report
            )
        )
        refs = validate_references(flow.get("command_ids"), command_ids, f"flow {flow_id}.command_ids", report)
        required_commands.update(refs)
    if "happy" not in flow_variants:
        report.error("flows need at least one happy variant")
    if not flow_variants.intersection({"alternate", "failure"}) and not is_nonempty_string(
        manifest.get("flow_non_happy_exemption")
    ):
        report.error("flows need an alternate/failure variant or flow_non_happy_exemption")

    human_checks = collect_unique(
        as_list(manifest.get("human_checks"), "human_checks", report), "human_checks", report
    )
    if not human_checks:
        report.error("human_checks must not be empty")
    for check_id, check in human_checks.items():
        if not is_nonempty_string(check.get("name")):
            report.error(f"human check {check_id} needs a name")
        steps = check.get("steps")
        if not isinstance(steps, list) or not steps or not all(is_nonempty_string(step) for step in steps):
            report.error(f"human check {check_id}.steps must be a non-empty string array")
        if not is_nonempty_string(check.get("expected")):
            report.error(f"human check {check_id} needs expected behavior")
        if check.get("severity_if_failed") not in ALLOWED_SEVERITIES:
            report.error(f"human check {check_id} has invalid severity_if_failed")
        if check.get("status") not in ALLOWED_HUMAN_STATUSES:
            report.error(f"human check {check_id} has invalid status")
        traced_requirements.update(
            validate_references(
                check.get("requirement_ids"), requirement_ids, f"human check {check_id}.requirement_ids", report
            )
        )

    defects = collect_unique(as_list(manifest.get("defects"), "defects", report), "defects", report)
    for defect_id, defect in defects.items():
        if defect.get("severity") not in ALLOWED_SEVERITIES:
            report.error(f"defect {defect_id} has invalid severity")
        if defect.get("status") not in ALLOWED_DEFECT_STATUSES:
            report.error(f"defect {defect_id} has invalid status")
        if not is_nonempty_string(defect.get("summary")):
            report.error(f"defect {defect_id} needs a summary")

    untraced = sorted(requirement_ids - traced_requirements)
    if untraced:
        report.error(f"requirements have no test or human trace: {', '.join(untraced)}")

    for command_id in sorted(required_commands):
        command = commands.get(command_id, {})
        phases = set(command.get("required_phases", []))
        missing_phases = {"automated", "release"} - phases
        if missing_phases:
            report.error(
                f"referenced command {command_id} must run in automated and release phases; "
                f"missing: {', '.join(sorted(missing_phases))}"
            )

    research = as_list(manifest.get("research", []), "research", report)
    for index, item in enumerate(research):
        if not isinstance(item, dict):
            report.error(f"research[{index}] must be an object")
            continue
        for key in ("scope", "source_url", "source_type", "reviewed_on"):
            if not is_nonempty_string(item.get(key)):
                report.error(f"research[{index}].{key} must be non-empty")

    return {
        "commands": commands,
        "required_commands": required_commands,
        "human_checks": human_checks,
        "defects": defects,
    }


def validate_human_trace_docs(root: Path, manifest: dict[str, Any], report: Report) -> None:
    qa_dir = root / "docs" / "QA"
    try:
        plan = (qa_dir / "QA-PLAN.md").read_text(encoding="utf-8")
        matrix = (qa_dir / "QA-MATRIX.md").read_text(encoding="utf-8")
        human = (qa_dir / "HUMAN-E2E.md").read_text(encoding="utf-8")
    except FileNotFoundError:
        return

    for source in manifest.get("governance", []):
        if isinstance(source, dict) and is_nonempty_string(source.get("path")) and source["path"] not in plan:
            report.error(f"QA-PLAN.md does not name governance source: {source['path']}")

    matrix_ids: set[str] = set()
    for requirement in manifest.get("requirements", []):
        if isinstance(requirement, dict) and is_nonempty_string(requirement.get("id")):
            matrix_ids.add(requirement["id"])
    for module in manifest.get("modules", []):
        if not isinstance(module, dict):
            continue
        if is_nonempty_string(module.get("id")):
            matrix_ids.add(module["id"])
        for case in module.get("cases", []):
            if isinstance(case, dict) and is_nonempty_string(case.get("id")):
                matrix_ids.add(case["id"])
    for flow in manifest.get("flows", []):
        if isinstance(flow, dict) and is_nonempty_string(flow.get("id")):
            matrix_ids.add(flow["id"])
    for item_id in sorted(matrix_ids):
        if item_id not in matrix:
            report.error(f"QA-MATRIX.md is missing trace id: {item_id}")

    for check in manifest.get("human_checks", []):
        if isinstance(check, dict) and is_nonempty_string(check.get("id")) and check["id"] not in human:
            report.error(f"HUMAN-E2E.md is missing human check id: {check['id']}")


def evidence_path(root: Path) -> Path:
    return root / ".autoqa" / "evidence" / "latest.json"


def run_commands(root: Path, commands: dict[str, dict[str, Any]], phase: str, report: Report) -> None:
    selected = {
        command_id: command
        for command_id, command in commands.items()
        if phase in command.get("required_phases", ["automated", "release"])
    }
    records: dict[str, Any] = {}
    for command_id, command in selected.items():
        cwd = safe_workdir(root, command.get("cwd", "."), f"command {command_id}", report)
        if report.errors:
            continue
        env = os.environ.copy()
        env.update(command.get("env", {}))
        started = datetime.now(timezone.utc)
        try:
            completed = subprocess.run(
                command["argv"],
                cwd=cwd,
                env=env,
                capture_output=True,
                text=True,
                timeout=command.get("timeout_seconds", 300),
                check=False,
            )
            exit_code = completed.returncode
            stdout = completed.stdout[-20000:]
            stderr = completed.stderr[-20000:]
        except (OSError, subprocess.TimeoutExpired) as exc:
            exit_code = 124 if isinstance(exc, subprocess.TimeoutExpired) else 127
            stdout = ""
            stderr = str(exc)
        finished = datetime.now(timezone.utc)
        records[command_id] = {
            "fingerprint": command_fingerprint(command),
            "started_at": started.isoformat(),
            "finished_at": finished.isoformat(),
            "exit_code": exit_code,
            "stdout_tail": stdout,
            "stderr_tail": stderr,
        }
        status = "PASS" if exit_code == 0 else "FAIL"
        print(f"[{status}] {command_id}: {' '.join(command['argv'])}")
    path = evidence_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"schema_version": 1, "commands": records}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def validate_evidence(
    root: Path,
    manifest: dict[str, Any],
    commands: dict[str, dict[str, Any]],
    required_commands: set[str],
    report: Report,
) -> None:
    path = evidence_path(root)
    evidence = load_json(path, report)
    records = evidence.get("commands", {}) if isinstance(evidence, dict) else {}
    if not isinstance(records, dict):
        report.error("Evidence commands must be an object")
        return
    max_age = manifest.get("evidence_max_age_hours", 24)
    if not isinstance(max_age, (int, float)) or not 0 < max_age <= 168:
        report.error("evidence_max_age_hours must be greater than 0 and no more than 168")
        max_age = 24
    now = datetime.now(timezone.utc)
    for command_id in sorted(required_commands):
        record = records.get(command_id)
        if not isinstance(record, dict):
            report.error(f"Missing fresh evidence for command: {command_id}")
            continue
        command = commands.get(command_id)
        if command and record.get("fingerprint") != command_fingerprint(command):
            report.error(f"Evidence command fingerprint is stale: {command_id}")
        if record.get("exit_code") != 0:
            report.error(f"Evidence command failed: {command_id} (exit {record.get('exit_code')})")
        try:
            finished = datetime.fromisoformat(record["finished_at"])
            if finished.tzinfo is None:
                raise ValueError("timezone missing")
            age_hours = (now - finished.astimezone(timezone.utc)).total_seconds() / 3600
            if age_hours < -0.1 or age_hours > max_age:
                report.error(f"Evidence is stale for {command_id}: {age_hours:.1f} hours old")
        except (KeyError, TypeError, ValueError):
            report.error(f"Evidence has invalid finished_at for command: {command_id}")


def validate_release(state: dict[str, Any], report: Report) -> None:
    for check_id, check in state["human_checks"].items():
        if check.get("status") != "pass":
            report.error(f"Human E2E is not passed: {check_id} ({check.get('status')})")
    for defect_id, defect in state["defects"].items():
        severity = defect.get("severity")
        status = defect.get("status")
        if severity in {"P0", "P1"} and status != "fixed":
            report.error(f"Blocking defect remains unresolved: {defect_id} ({severity}, {status})")
        elif severity in {"P2", "P3"} and status == "open":
            report.warn(f"Residual defect remains open: {defect_id} ({severity})")


def print_report(report: Report) -> int:
    for warning in report.warnings:
        print(f"WARN: {warning}")
    for error in report.errors:
        print(f"ERROR: {error}")
    if report.errors:
        print(f"AutoQA gate failed: {len(report.errors)} error(s), {len(report.warnings)} warning(s)")
        return 1
    print(f"AutoQA gate passed: 0 errors, {len(report.warnings)} warning(s)")
    return 0


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    report = Report()
    if not root.is_dir():
        report.error(f"Project root is not a directory: {root}")
        return print_report(report)
    manifest_path = (root / args.manifest).resolve()
    try:
        manifest_path.relative_to(root)
    except ValueError:
        report.error("Manifest path must stay within the project root")
        return print_report(report)
    validate_docs(root, report)
    manifest = load_json(manifest_path, report)
    state = validate_manifest(manifest, root, report) if manifest else {
        "commands": {}, "required_commands": set(), "human_checks": {}, "defects": {}
    }
    if manifest:
        validate_human_trace_docs(root, manifest, report)
    if args.run:
        if args.phase == "plan":
            report.error("--run requires --phase automated or release")
        elif not report.errors:
            run_commands(root, state["commands"], args.phase, report)
    if args.phase in {"automated", "release"} and not report.errors:
        validate_evidence(root, manifest, state["commands"], state["required_commands"], report)
    if args.phase == "release":
        validate_release(state, report)
    return print_report(report)


if __name__ == "__main__":
    sys.exit(main())
