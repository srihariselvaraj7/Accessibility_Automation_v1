from utils.xpath import get_xpath
from utils.issue import AccessibilityIssue
from utils.scan_result import ScanResult
from utils.scanner_indicator import (
    show_scanning_element,
    clear_scanning_element
)


def scan_headings(page):

    issues = []

    headings = page.locator(
        "h1, h2, h3, h4, h5, h6"
    )

    heading_count = headings.count()

    checked = 0
    passed = 0

    # ========================================
    # H1 COUNT CHECK
    # ========================================

    h1_elements = page.locator("h1")
    h1_count = h1_elements.count()

    # ----------------------------------------
    # Missing H1
    # ----------------------------------------

    if h1_count == 0:

        issue = AccessibilityIssue(
            page.url,
            None,
            "Missing H1",
            "Page does not contain an H1 heading.",
            "Medium",
            "Medium"
        )

        issue.xpath = "//h1"

        issues.append(issue)

    # ----------------------------------------
    # Multiple H1
    # ----------------------------------------

    elif h1_count > 1:

        for i in range(1, h1_count):

            h1 = h1_elements.nth(i)

            try:

                if not h1.is_visible():
                    continue

                h1.scroll_into_view_if_needed()

                page.wait_for_timeout(50)

            except Exception:
                continue

            # ----------------------------------------
            # Show live scanning indicator
            # ----------------------------------------

            try:

                show_scanning_element(page, h1)

                page.wait_for_timeout(150)

            except Exception:
                pass

            try:

                xpath = get_xpath(
                    page,
                    h1
                )

            except Exception:

                xpath = ""

            issue = AccessibilityIssue(
                page.url,
                h1,
                "Multiple H1 Headings",
                f"Page contains {h1_count} H1 headings. "
                f"The project rule requires a single H1 per page.",
                "Medium",
                "Medium"
            )

            issue.xpath = xpath

            issues.append(issue)

            # ----------------------------------------
            # Remove scanning indicator
            # ----------------------------------------

            try:
                clear_scanning_element(page, h1)
            except Exception:
                pass

    # ========================================
    # HEADING HIERARCHY CHECK
    # ========================================

    previous_level = None

    for i in range(heading_count):

        heading = headings.nth(i)

        # ----------------------------------------
        # Make current heading visible
        # ----------------------------------------

        try:

            if not heading.is_visible():
                continue

            heading.scroll_into_view_if_needed()

            page.wait_for_timeout(50)

        except Exception:
            continue

        # ----------------------------------------
        # Show live scanning indicator
        # ----------------------------------------

        try:

            show_scanning_element(page, heading)

            page.wait_for_timeout(150)

        except Exception:
            pass

        # ----------------------------------------
        # Get heading information
        # ----------------------------------------

        try:

            tag_name = heading.evaluate(
                "element => element.tagName.toLowerCase()"
            )

            level = int(tag_name[1])

            text = heading.inner_text().strip()

        except Exception:

            try:
                clear_scanning_element(page, heading)
            except Exception:
                pass

            continue

        checked += 1

        try:

            xpath = get_xpath(
                page,
                heading
            )

        except Exception:

            xpath = ""

        heading_issues = []

        # ----------------------------------------
        # Empty heading
        # ----------------------------------------

        if not text:

            heading_issues.append(
                (
                    "Empty Heading",
                    f"{tag_name.upper()} is empty and "
                    "does not contain meaningful text.",
                    "Medium",
                    "Medium"
                )
            )

        # ----------------------------------------
        # Heading hierarchy
        # ----------------------------------------

        if previous_level is not None:

            if level > previous_level + 1:

                heading_issues.append(
                    (
                        "Heading Hierarchy",
                        f"{tag_name.upper()} appears after "
                        f"H{previous_level}. "
                        "Heading level skipped.",
                        "Medium",
                        "Medium"
                    )
                )

        # ----------------------------------------
        # PASS
        # ----------------------------------------

        if not heading_issues:

            passed += 1

        # ----------------------------------------
        # FAIL
        # ----------------------------------------

        else:

            for (
                issue_type,
                description,
                severity,
                priority
            ) in heading_issues:

                issue = AccessibilityIssue(
                    page.url,
                    heading,
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
            clear_scanning_element(page, heading)
        except Exception:
            pass

        previous_level = level

    # ========================================
    # RETURN SCAN RESULT
    # ========================================

    return ScanResult(
        issues=issues,
        checked=checked,
        passed=passed
    )