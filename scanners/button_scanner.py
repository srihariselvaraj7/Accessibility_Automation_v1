from utils.xpath import get_xpath
from utils.issue import AccessibilityIssue
from utils.scan_result import ScanResult
from utils.scanner_indicator import (
    show_scanning_element,
    clear_scanning_element
)


def scan_buttons(page):

    issues = []

    buttons = page.locator(
        "button, [role='button'], "
        "input[type='button'], input[type='submit']"
    )

    button_count = buttons.count()

    checked = 0
    passed = 0

    for i in range(button_count):

        button = buttons.nth(i)

        # ----------------------------------------
        # Make current button visible
        # ----------------------------------------

        try:

            if not button.is_visible():
                continue

            button.scroll_into_view_if_needed()

            page.wait_for_timeout(50)

        except Exception:
            continue

        # ----------------------------------------
        # Show live scanning indicator
        # ----------------------------------------

        try:

            show_scanning_element(page, button)

            page.wait_for_timeout(150)

        except Exception:
            pass

        # ----------------------------------------
        # Get button information
        # ----------------------------------------

        try:

            aria_label = button.get_attribute(
                "aria-label"
            )

            aria_labelledby = button.get_attribute(
                "aria-labelledby"
            )

            try:
                visible_text = button.inner_text().strip()

            except Exception:
                visible_text = ""

        except Exception:

            clear_scanning_element(page, button)
            continue

        checked += 1

        # ----------------------------------------
        # Accessible name
        # ----------------------------------------

        accessible_name = (
            aria_label
            or aria_labelledby
            or visible_text
        )

        # ----------------------------------------
        # Determine accessibility failures
        # ----------------------------------------

        button_issues = []

        # Missing accessible name
        if not accessible_name:

            button_issues.append(
                (
                    "Missing Accessible Name",
                    "Button does not have a meaningful accessible name.",
                    "High",
                    "High"
                )
            )

        # ----------------------------------------
        # PASS
        # ----------------------------------------

        if not button_issues:

            passed += 1

            try:
                clear_scanning_element(page, button)
            except Exception:
                pass

            continue

        # ----------------------------------------
        # FAIL
        # ----------------------------------------

        try:

            xpath = get_xpath(
                page,
                button
            )

        except Exception:

            xpath = ""

        for (
            issue_type,
            description,
            severity,
            priority
        ) in button_issues:

            issue = AccessibilityIssue(
                page.url,
                button,
                issue_type,
                description,
                severity,
                priority
            )

            issue.xpath = xpath

            issues.append(issue)

        # ----------------------------------------
        # Remove scanning indicator
        # ----------------------------------------

        try:
            clear_scanning_element(page, button)
        except Exception:
            pass

    # ----------------------------------------
    # Return scanner result
    # ----------------------------------------

    return ScanResult(
        issues=issues,
        checked=checked,
        passed=passed
    )