"""
Offline Plugin Tests — Batches A, B, C
Runs ACORD, OPA, and MLflow/PII tests without requiring a live API.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Run only offline batches
from run_plugin_tests import batch_a, batch_b, batch_c, generate_report, RESULTS

if __name__ == "__main__":
    from datetime import datetime
    print("=" * 65)
    print("  OFFLINE PLUGIN TESTS (Batches A / B / C)")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 65)
    batch_a()
    batch_b()
    batch_c()
    print("\n" + "=" * 65)
    passed, failed, total = generate_report()
    print(f"  OFFLINE RESULT: {passed}/{total} passed | {failed} failed")
    print("=" * 65)
    sys.exit(0 if failed == 0 else 1)
