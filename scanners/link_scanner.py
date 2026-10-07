from utils.xpath import get_xpath
from utils.issue import AccessibilityIssue
from utils.scan_result import ScanResult
from utils.scanner_indicator import (
    show_scanning_element,
    clear_scanning_element
)


def scan_links(page):

    issues = []

    links = page.locator("a")
    link_count = links.count()

    checked = 0
    passed = 0

    meaningless_text = [
        "click here",
        "here",
        "read more",
        "more",
        "learn more"
    ]

    for i in range(link_count):

        link = links.nth(i)

        # ----------------------------------------
        # Make current link visible
        # ----------------------------------------

        try:

            if not link.is_visible():
                continue

            link.scroll_into_view_if_needed()

            page.wait_for_timeout(50)

        except Exception:
            continue

        # ----------------------------------------
        # Show live scanning indicator
        # ----------------------------------------

        try:
            show_scanning_element(page, link)
            page.wait_for_timeout(150)

        except Exception:
            pass

        # ----------------------------------------
        # Get link information
        # ----------------------------------------

        try:

            href = link.get_attribute("href")

            aria_label = link.get_attribute(
                "aria-label"
            )

            aria_labelledby = link.get_attribute(
                "aria-labelledby"
            )

            try:
                visible_text = link.inner_text().strip()

            except Exception:
                visible_text = ""

        except Exception:

            clear_scanning_element(page, link)
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

        # Check image alt if there is no text
        if not accessible_name:

            try:

                images = link.locator("img")

                if images.count() > 0:

                    image_alt = images.nth(0).get_attribute(
                        "alt"
                    )

                    if image_alt and image_alt.strip():

                        accessible_name = image_alt.strip()

            except Exception:
                pass

        # ----------------------------------------
        # Determine accessibility failures
        # ----------------------------------------

        link_issues = []

        # 1. Missing href
        if not href:

            link_issues.append(
                (
                    "Missing Href",
                    "Link does not have an href attribute.",
                    "Medium",
                    "Medium"
                )
            )

        # 2. Missing accessible name
        if not accessible_name:

            link_issues.append(
                (
                    "Missing Accessible Name",
                    "Link does not have a meaningful accessible name.",
                    "High",
                    "High"
                )
            )

        # 3. Meaningless link text
        if visible_text.lower() in meaningless_text:

            link_issues.append(
                (
                    "Meaningless Link Text",
                    f"Link text '{visible_text}' does not clearly "
                    "describe the destination or purpose of the link.",
                    "Medium",
                    "Medium"
                )
            )

        # 4. Raw URL
        if (
            visible_text.startswith("http://")
            or visible_text.startswith("https://")
        ):

            link_issues.append(
                (
                    "Raw URL Link Text",
                    "Link displays a raw URL as its visible text.",
                    "Low",
                    "Low"
                )
            )

        # ----------------------------------------
        # PASS
        # ----------------------------------------

        if not link_issues:

            passed += 1

            # Remove indicator before moving to next link
            try:
                clear_scanning_element(page, link)
            except Exception:
                pass

            continue

        # ----------------------------------------
        # FAIL
        # ----------------------------------------

        try:

            xpath = get_xpath(
                page,
                link
            )

        except Exception:

            xpath = ""

        for (
            issue_type,
            description,
            severity,
            priority
        ) in link_issues:

            issue = AccessibilityIssue(
                page.url,
                link,
                issue_type,
                description,
                severity,
                priority
            )

            issue.xpath = xpath

            issues.append(issue)

        # Remove indicator after checking the link
        try:
            clear_scanning_element(page, link)
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