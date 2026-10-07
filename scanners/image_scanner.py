from utils.xpath import get_xpath
from utils.issue import AccessibilityIssue
from utils.scan_result import ScanResult
from utils.scanner_indicator import (
    show_scanning_element,
    clear_scanning_element
)


def scan_images(page):

    issues = []

    images = page.locator("img")
    image_count = images.count()

    checked = 0
    passed = 0

    for i in range(image_count):

        image = images.nth(i)

        # ----------------------------------------
        # Make current image visible
        # ----------------------------------------

        try:

            if not image.is_visible():
                continue

            image.scroll_into_view_if_needed()

            page.wait_for_timeout(50)

        except Exception:
            continue

        # ----------------------------------------
        # Show live scanning indicator
        # ----------------------------------------

        try:

            show_scanning_element(page, image)

            page.wait_for_timeout(150)

        except Exception:
            pass

        # ----------------------------------------
        # Get image information
        # ----------------------------------------

        try:

            alt = image.get_attribute("alt")
            src = image.get_attribute("src")

        except Exception:

            clear_scanning_element(page, image)
            continue

        checked += 1

        # ----------------------------------------
        # Determine accessibility failures
        # ----------------------------------------

        image_issues = []

        # 1. Missing alt attribute
        if alt is None:

            image_issues.append(
                (
                    "Missing Alt Text",
                    "Image does not have an alt attribute.",
                    "High",
                    "High"
                )
            )

        # 2. Empty alt attribute
        elif alt.strip() == "":

            image_issues.append(
                (
                    "Empty Alt Text",
                    "Image has an empty alt attribute. "
                    "Verify whether the image is decorative.",
                    "Medium",
                    "Medium"
                )
            )

        # 3. Image not loaded
        try:

            loaded = image.evaluate(
                """
                element => element.complete &&
                           element.naturalWidth > 0
                """
            )

            if not loaded:

                image_issues.append(
                    (
                        "Image Not Loaded",
                        f"Image could not be loaded successfully. "
                        f"Source: {src}",
                        "Medium",
                        "Medium"
                    )
                )

        except Exception:
            pass

        # ----------------------------------------
        # PASS
        # ----------------------------------------

        if not image_issues:

            passed += 1

            try:
                clear_scanning_element(page, image)
            except Exception:
                pass

            continue

        # ----------------------------------------
        # FAIL
        # ----------------------------------------

        try:

            xpath = get_xpath(
                page,
                image
            )

        except Exception:

            xpath = ""

        for (
            issue_type,
            description,
            severity,
            priority
        ) in image_issues:

            issue = AccessibilityIssue(
                page.url,
                image,
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
            clear_scanning_element(page, image)
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