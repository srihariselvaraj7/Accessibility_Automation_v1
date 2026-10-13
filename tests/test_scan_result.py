from utils.scan_result import ScanResult


def test_scan_result_initial_values():
    result = ScanResult()

    assert result.issues == []
    assert result.checked == 0
    assert result.passed == 0
    assert result.failed == 0


def test_scan_result_counts_failures():
    issues = ["Missing image alt text", "Empty heading"]

    result = ScanResult(
        issues=issues,
        checked=10,
        passed=8
    )

    assert result.checked == 10
    assert result.passed == 8
    assert result.failed == 2