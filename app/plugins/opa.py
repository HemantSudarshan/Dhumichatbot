"""
OPA (Open Policy Agent) Stub
============================
Structural placeholder for California compliance checks.
In production, this module will make HTTP calls to a real OPA/Rego server.
For the MVP/PoC phase, it always returns compliant=True with no violations.

Usage:
    from app.plugins.opa import check_compliance
    result = check_compliance(state="CA", age=45, coverage_amount=250000)
"""

import logging

logger = logging.getLogger(__name__)


class ComplianceResult:
    def __init__(self, compliant: bool, violations: list[str], policy_version: str):
        self.compliant = compliant
        self.violations = violations
        self.policy_version = policy_version

    def to_dict(self) -> dict:
        return {
            "compliant": self.compliant,
            "violations": self.violations,
            "policy_version": self.policy_version,
        }


def check_compliance(
    state: str,
    age: int,
    coverage_amount: int,
    tobacco_user: bool = False,
) -> ComplianceResult:
    """
    Check if a quote request complies with state insurance regulations.

    Current stub behaviour:
      - Logs the parameters for observability.
      - Returns compliant=True, no violations.
      - Policy version is set to 'opa-stub-v1.0'.

    Production implementation:
      - POST to http://opa-server:8181/v1/data/insurance/california/quote
      - Parse the Rego policy evaluation response.
      - Map violations to denial reasons for the SB 263 disclosure.
    """
    logger.info(
        "[OPA STUB] check_compliance called | state=%s age=%d coverage=%d tobacco=%s",
        state,
        age,
        coverage_amount,
        tobacco_user,
    )

    # ── Future: real OPA HTTP call ──────────────────────────────────
    # import httpx
    # resp = httpx.post(
    #     "http://opa-server:8181/v1/data/insurance/california/quote",
    #     json={"input": {"state": state, "age": age, "coverage_amount": coverage_amount}},
    #     timeout=2.0
    # )
    # data = resp.json().get("result", {})
    # return ComplianceResult(
    #     compliant=data.get("allow", False),
    #     violations=data.get("violations", []),
    #     policy_version=data.get("policy_version", "unknown"),
    # )
    # ────────────────────────────────────────────────────────────────

    return ComplianceResult(
        compliant=True,
        violations=[],
        policy_version="opa-stub-v1.0",
    )
