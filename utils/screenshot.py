import os
import re


def take_element_screenshot(issue, issue_number):

    os.makedirs("screenshots", exist_ok=True)

    safe_issue_type = re.sub(
        r"[^a-zA-Z0-9_-]",
        "_",
        issue.issue_type
    ).lower()

    filename = f"{issue_number}_{safe_issue_type}.png"

    filepath = os.path.abspath(
        os.path.join("screenshots", filename)
    )

    try:

        # Check whether the element is visible
        if not issue.element.is_visible():

            issue.screenshot = None
            issue.screenshot_status = "Element not visible"

            return None

        # Scroll element into view
        issue.element.scroll_into_view_if_needed()

        # Take screenshot
        issue.element.screenshot(
            path=filepath,
            timeout=10000
        )

        issue.screenshot = filepath
        issue.screenshot_status = "Captured"

        return filepath

    except Exception as e:

        issue.screenshot = None
        issue.screenshot_status = (
            f"Screenshot failed: {type(e).__name__}"
        )

        return None