#!/usr/bin/env python3
"""Validate the final audit proof record.

This is the repository's proof-loop-lite guardrail: the audited task must have a
PASS verdict, every declared acceptance criterion must be PASS with evidence,
and there must be no open problems.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROOF = ROOT / ".agent/tasks/comfy-audit-hardening-20260829/proof.json"
EXPECTED_IDS = [f"AC{i}" for i in range(1, 11)]


def main() -> None:
    data = json.loads(PROOF.read_text(encoding="utf-8"))
    assert data.get("task_id") == "comfy-audit-hardening-20260829"
    assert data.get("overall_verdict") == "PASS"

    criteria = data.get("acceptance_criteria")
    assert isinstance(criteria, list) and len(criteria) == len(EXPECTED_IDS)
    assert [item.get("id") for item in criteria] == EXPECTED_IDS

    for item in criteria:
        assert item.get("status") == "PASS", f"{item.get('id')}: not PASS"
        proof = item.get("proof")
        assert isinstance(proof, list) and proof, f"{item.get('id')}: proof missing"
        reason = item.get("reason")
        assert isinstance(reason, str) and reason.strip(), f"{item.get('id')}: reason missing"

    assert data.get("problems") == [], "proof has open problems"
    checks = data.get("checks")
    assert isinstance(checks, list) and checks, "verification checks missing"
    assert any(
        check.get("name") == "GitHub Actions static-validation"
        and check.get("status") == "PASS"
        for check in checks
        if isinstance(check, dict)
    ), "green GitHub Actions proof missing"

    print("OK proof.json: PASS, 10/10 criteria, no open problems")


if __name__ == "__main__":
    main()
