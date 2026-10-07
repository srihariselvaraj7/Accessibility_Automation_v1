class AccessibilityIssue:

    def __init__(
        self,
        page_url,
        element,
        issue_type,
        description,
        severity,
        priority
    ):
        self.page_url = page_url
        self.element = element
        self.issue_type = issue_type
        self.description = description
        self.severity = severity
        self.priority = priority
        self.xpath = None
        self.screenshot = None
        self.screenshot_status = "Not captured"

        # Test result
        self.test_case = "Failed"