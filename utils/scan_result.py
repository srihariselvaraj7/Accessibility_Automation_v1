class ScanResult:

    def __init__(self, issues=None, checked=0, passed=0):
        self.issues = issues or []
        self.checked = checked
        self.passed = passed

    @property
    def failed(self):
        return len(self.issues)