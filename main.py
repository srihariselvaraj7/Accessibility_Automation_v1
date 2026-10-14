from playwright.sync_api import sync_playwright

from scanners.heading_scanner import scan_headings
from scanners.image_scanner import scan_images
from scanners.button_scanner import scan_buttons
from scanners.link_scanner import scan_links
from scanners.contrast_scanner import scan_contrast

from utils.screenshot import take_element_screenshot
from utils.excel_report import generate_excel_report


def main():

    url = input("Enter page URL: ")

    with sync_playwright() as p:

        browser = p.chromium.launch(
            channel="chrome",
            headless=False
        )

        page = browser.new_page()

        # ========================================
        # HEADER
        # ========================================

        print()
        print("=" * 40)
        print("       ACCESSIBILITY TESTING TOOL")
        print("=" * 40)

        print()
        print(f"Page URL : {url}")

        # ========================================
        # OPEN PAGE
        # ========================================

        page.goto(
            url,
            wait_until="domcontentloaded"
        )

        print(
            f"Title    : {page.title()}"
        )

        print()
        print("Page opened successfully.")

        # ========================================
        # START SCAN
        # ========================================

        print()
        print("Starting accessibility scan...")
        print()

        # ========================================
        # HEADING SCAN
        # ========================================

        print("Scanning headings...")

        heading_result = scan_headings(page)

        # ========================================
        # IMAGE SCAN
        # ========================================

        print("Scanning images...")

        image_result = scan_images(page)

        # ========================================
        # BUTTON SCAN
        # ========================================

        print("Scanning buttons...")

        button_result = scan_buttons(page)

        # ========================================
        # LINK SCAN
        # ========================================

        print("Scanning links...")

        link_result = scan_links(page)

        # ========================================
        # CONTRAST SCAN
        # ========================================

        print("Scanning color contrast...")

        contrast_result = scan_contrast(page)

        # ========================================
        # COMBINE ISSUES
        # ========================================

        all_issues = (
            heading_result.issues
            + image_result.issues
            + button_result.issues
            + link_result.issues
            + contrast_result.issues
        )

        # ========================================
        # SCAN SUMMARY
        # ========================================

        print()
        print("=" * 40)
        print("           SCAN SUMMARY")
        print("=" * 40)
        print()

        print(
            f"{'':<20}"
            f"{'Total':>8}"
            f"{'Passed':>10}"
            f"{'Failed':>10}"
        )

        print("-" * 48)

        heading_failed = (
            heading_result.checked
            - heading_result.passed
        )

        image_failed = (
            image_result.checked
            - image_result.passed
        )

        button_failed = (
            button_result.checked
            - button_result.passed
        )

        link_failed = (
            link_result.checked
            - link_result.passed
        )

        contrast_failed = (
            contrast_result.checked
            - contrast_result.passed
        )

        # ----------------------------------------
        # Individual scanner results
        # ----------------------------------------

        print(
            f"{'Headings':<20}"
            f"{heading_result.checked:>8}"
            f"{heading_result.passed:>10}"
            f"{heading_failed:>10}"
        )

        print(
            f"{'Images':<20}"
            f"{image_result.checked:>8}"
            f"{image_result.passed:>10}"
            f"{image_failed:>10}"
        )

        print(
            f"{'Buttons':<20}"
            f"{button_result.checked:>8}"
            f"{button_result.passed:>10}"
            f"{button_failed:>10}"
        )

        print(
            f"{'Links':<20}"
            f"{link_result.checked:>8}"
            f"{link_result.passed:>10}"
            f"{link_failed:>10}"
        )

        print(
            f"{'Color Contrast':<20}"
            f"{contrast_result.checked:>8}"
            f"{contrast_result.passed:>10}"
            f"{contrast_failed:>10}"
        )

        # ----------------------------------------
        # Overall totals
        # ----------------------------------------

        total_checked = (
            heading_result.checked
            + image_result.checked
            + button_result.checked
            + link_result.checked
            + contrast_result.checked
        )

        total_passed = (
            heading_result.passed
            + image_result.passed
            + button_result.passed
            + link_result.passed
            + contrast_result.passed
        )

        total_failed = (
            total_checked
            - total_passed
        )

        print("-" * 48)

        print(
            f"{'TOTAL':<20}"
            f"{total_checked:>8}"
            f"{total_passed:>10}"
            f"{total_failed:>10}"
        )

        print()
        print(
            f"Accessibility Issues Found: "
            f"{len(all_issues)}"
        )

        # ========================================
        # SCREENSHOTS
        # ========================================

        print()
        print("=" * 40)
        print("        SCREENSHOTS")
        print("=" * 40)
        print()

        screenshot_index = 1

        for issue in all_issues:

            try:

                screenshot_path = take_element_screenshot(
                    issue,
                    screenshot_index
                )

                issue.screenshot = screenshot_path

                if screenshot_path:

                    print(
                        "✓ Screenshot captured"
                    )

                    print(
                        f"  Issue: {issue.issue_type}"
                    )

                    print(
                        f"  XPath: {issue.xpath}"
                    )

                else:

                    print(
                        "⚠ Screenshot not captured"
                    )

                    print(
                        f"  Issue: {issue.issue_type}"
                    )

                    print(
                        f"  XPath: {issue.xpath}"
                    )

            except Exception as e:

                issue.screenshot = None

                if hasattr(
                    issue,
                    "screenshot_status"
                ):

                    issue.screenshot_status = (
                        f"Screenshot failed: {e}"
                    )

                print(
                    "⚠ Screenshot not captured"
                )

                print(
                    f"  Issue: {issue.issue_type}"
                )

                print(
                    f"  XPath: {issue.xpath}"
                )

            screenshot_index += 1

        # ========================================
        # EXCEL REPORT
        # ========================================

        print()
        print("=" * 40)
        print("        EXCEL REPORT")
        print("=" * 40)
        print()

        report_path = generate_excel_report(
            page.url,
            all_issues,
            heading_result,
            image_result,
            button_result,
            link_result,
            contrast_result
        )

        print(
            "✓ Excel report generated successfully:"
        )

        print(
            f"  {report_path}"
        )

        # ========================================
        # KEEP BROWSER OPEN
        # ========================================

        input(
            "\nPress Enter to close browser..."
        )

        browser.close()


if __name__ == "__main__":
    main()