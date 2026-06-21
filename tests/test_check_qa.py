from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CHECK_QA = REPO_ROOT / "autoqa-skill" / "scripts" / "check_qa.py"


DOCS = {
    "QA-PLAN.md": (
        "<!-- autoqa:document:qa-plan -->\n"
        "<!-- autoqa:section:scope -->\n"
        "<!-- autoqa:section:governance-sources -->\n"
        "<!-- autoqa:section:risk -->\n"
        "<!-- autoqa:section:best-practice -->\n"
        "<!-- autoqa:section:environments -->\n"
        "<!-- autoqa:section:responsibilities -->\n"
        "<!-- autoqa:section:exit-criteria -->\n"
        "# Valid QA Plan\nGovernance: docs/SPEC.md\n"
    ),
    "QA-MATRIX.md": (
        "<!-- autoqa:document:qa-matrix -->\n"
        "<!-- autoqa:section:requirements -->\n"
        "<!-- autoqa:section:file-gates -->\n"
        "<!-- autoqa:section:module-boundaries -->\n"
        "<!-- autoqa:section:business-flows -->\n"
        "<!-- autoqa:section:fault-sensitivity -->\n"
        "<!-- autoqa:section:residual-risk -->\n"
        "# Valid QA Matrix\nREQ-001 records CASE-001 CASE-002 FLOW-001 FLOW-002\n"
    ),
    "HUMAN-E2E.md": (
        "<!-- autoqa:document:human-e2e -->\n"
        "<!-- autoqa:section:instructions -->\n"
        "<!-- autoqa:section:environment -->\n"
        "<!-- autoqa:section:checks -->\n"
        "<!-- autoqa:section:defects -->\n"
        "<!-- autoqa:section:sign-off -->\n"
        "# Valid Human E2E\nHUMAN-001\n"
    ),
}


def valid_manifest() -> dict:
    return {
        "schema_version": 1,
        "project": "fixture",
        "evidence_max_age_hours": 24,
        "governance": [{"path": "docs/SPEC.md", "kind": "spec"}],
        "requirements": [
            {"id": "REQ-001", "description": "A user can create a record", "source": "SPEC workflow 1"}
        ],
        "commands": [
            {
                "id": "cmd-test",
                "argv": [sys.executable, "-c", "print('fixture pass')"],
                "cwd": ".",
                "timeout_seconds": 30,
                "required_phases": ["automated", "release"],
            }
        ],
        "source_files": [
            {
                "path": "src/example.py",
                "kind": "executable",
                "command_ids": ["cmd-test"],
                "coverage_reason": "Import and create-record smoke behavior",
            }
        ],
        "modules": [
            {
                "id": "records",
                "description": "Owns business records",
                "entries": [{"id": "create", "description": "Create a record"}],
                "exits": [
                    {"id": "created", "description": "A durable record"},
                    {"id": "rejected", "description": "A contractual rejection"},
                ],
                "applicable_classes": ["happy", "negative"],
                "non_happy_exemption": "",
                "cases": [
                    {
                        "id": "CASE-001",
                        "business_rule": "A valid request creates exactly one record",
                        "class": "happy",
                        "requirement_ids": ["REQ-001"],
                        "entry_ids": ["create"],
                        "exit_ids": ["created"],
                        "command_ids": ["cmd-test"],
                    },
                    {
                        "id": "CASE-002",
                        "business_rule": "An invalid request creates no durable record",
                        "class": "negative",
                        "requirement_ids": ["REQ-001"],
                        "entry_ids": ["create"],
                        "exit_ids": ["rejected"],
                        "command_ids": ["cmd-test"],
                    },
                ],
            }
        ],
        "flows": [
            {
                "id": "FLOW-001",
                "name": "User creates a valid record",
                "variant": "happy",
                "requirement_ids": ["REQ-001"],
                "command_ids": ["cmd-test"],
            },
            {
                "id": "FLOW-002",
                "name": "User receives a safe rejection",
                "variant": "failure",
                "requirement_ids": ["REQ-001"],
                "command_ids": ["cmd-test"],
            },
        ],
        "flow_non_happy_exemption": "",
        "human_checks": [
            {
                "id": "HUMAN-001",
                "name": "The creation journey is understandable",
                "requirement_ids": ["REQ-001"],
                "steps": ["Open the form", "Create one record"],
                "expected": "The result and next action are clear",
                "severity_if_failed": "P1",
                "status": "pass",
            }
        ],
        "defects": [],
        "research": [],
    }


class CheckQATest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        qa_dir = self.root / "docs" / "QA"
        qa_dir.mkdir(parents=True)
        for name, content in DOCS.items():
            (qa_dir / name).write_text(content, encoding="utf-8")
        self.write_manifest(valid_manifest())

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_manifest(self, manifest: dict) -> None:
        path = self.root / "docs" / "QA" / "qa-manifest.json"
        path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    def run_gate(self, phase: str, run: bool = False) -> subprocess.CompletedProcess[str]:
        argv = [sys.executable, str(CHECK_QA), "--root", str(self.root), "--phase", phase]
        if run:
            argv.append("--run")
        return subprocess.run(argv, capture_output=True, text=True, check=False)

    def test_plan_accepts_complete_manifest(self) -> None:
        result = self.run_gate("plan")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("AutoQA gate passed", result.stdout)

    def test_automated_run_creates_current_evidence(self) -> None:
        result = self.run_gate("automated", run=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        evidence = self.root / ".autoqa" / "evidence" / "latest.json"
        self.assertTrue(evidence.is_file())
        self.assertIn("[PASS] cmd-test", result.stdout)

    def test_uncovered_exit_is_rejected(self) -> None:
        manifest = valid_manifest()
        manifest["modules"][0]["cases"][1]["exit_ids"] = ["created"]
        self.write_manifest(manifest)
        result = self.run_gate("plan")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("uncovered exits: rejected", result.stdout)

    def test_human_matrix_cannot_omit_machine_trace_id(self) -> None:
        matrix = self.root / "docs" / "QA" / "QA-MATRIX.md"
        matrix.write_text(DOCS["QA-MATRIX.md"].replace("FLOW-002", ""), encoding="utf-8")
        result = self.run_gate("plan")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("QA-MATRIX.md is missing trace id: FLOW-002", result.stdout)

    def test_changed_command_invalidates_old_evidence(self) -> None:
        first = self.run_gate("automated", run=True)
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        manifest = valid_manifest()
        manifest["commands"][0]["argv"] = [sys.executable, "-c", "print('changed command')"]
        self.write_manifest(manifest)
        result = self.run_gate("automated")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("fingerprint is stale", result.stdout)

    def test_release_rejects_pending_human_check(self) -> None:
        automated = self.run_gate("automated", run=True)
        self.assertEqual(automated.returncode, 0, automated.stdout + automated.stderr)
        manifest = valid_manifest()
        manifest["human_checks"][0]["status"] = "pending"
        self.write_manifest(manifest)
        result = self.run_gate("release")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Human E2E is not passed", result.stdout)

    def test_release_rejects_open_p1_and_warns_for_open_p2(self) -> None:
        automated = self.run_gate("automated", run=True)
        self.assertEqual(automated.returncode, 0, automated.stdout + automated.stderr)
        manifest = valid_manifest()
        manifest["defects"] = [
            {"id": "DEF-001", "summary": "Core flow is blocked", "severity": "P1", "status": "open"},
            {"id": "DEF-002", "summary": "Minor copy issue", "severity": "P2", "status": "open"},
        ]
        self.write_manifest(manifest)
        result = self.run_gate("release")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Blocking defect remains unresolved", result.stdout)
        self.assertIn("Residual defect remains open", result.stdout)

    def test_release_allows_open_p2_with_visible_warning(self) -> None:
        automated = self.run_gate("automated", run=True)
        self.assertEqual(automated.returncode, 0, automated.stdout + automated.stderr)
        manifest = valid_manifest()
        manifest["defects"] = [
            {"id": "DEF-002", "summary": "Minor copy issue", "severity": "P2", "status": "open"}
        ]
        self.write_manifest(manifest)
        result = self.run_gate("release")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Residual defect remains open", result.stdout)

    def test_happy_only_module_requires_explicit_exemption(self) -> None:
        manifest = valid_manifest()
        manifest["modules"][0]["applicable_classes"] = ["happy"]
        manifest["modules"][0]["non_happy_exemption"] = ""
        manifest["modules"][0]["cases"] = manifest["modules"][0]["cases"][:1]
        self.write_manifest(manifest)
        result = self.run_gate("plan")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("needs a non-happy class or a non_happy_exemption", result.stdout)


if __name__ == "__main__":
    unittest.main()
