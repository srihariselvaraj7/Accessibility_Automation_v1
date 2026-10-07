import re

from utils.xpath import get_xpath
from utils.issue import AccessibilityIssue
from utils.scan_result import ScanResult
from utils.scanner_indicator import (
    show_scanning_element,
    clear_scanning_element
)


def parse_color(color):
    """
    Convert rgb()/rgba() CSS color into RGB values.

    Returns None if the color cannot be parsed.
    """

    if not color:
        return None

    match = re.match(
        r"rgba?\(\s*([\d.]+)[,\s]+([\d.]+)[,\s]+([\d.]+)",
        color
    )

    if not match:
        return None

    return (
        int(float(match.group(1))),
        int(float(match.group(2))),
        int(float(match.group(3)))
    )


def relative_luminance(rgb):
    """
    Calculate WCAG relative luminance.
    """

    values = []

    for value in rgb:

        value = value / 255

        if value <= 0.03928:

            value = value / 12.92

        else:

            value = (
                (value + 0.055) / 1.055
            ) ** 2.4

        values.append(value)

    r, g, b = values

    return (
        0.2126 * r +
        0.7152 * g +
        0.0722 * b
    )


def contrast_ratio(color1, color2):
    """
    Calculate WCAG contrast ratio.
    """

    lum1 = relative_luminance(color1)
    lum2 = relative_luminance(color2)

    lighter = max(lum1, lum2)
    darker = min(lum1, lum2)

    return (
        (lighter + 0.05)
        / (darker + 0.05)
    )


def is_large_text(font_size, font_weight):
    """
    Determine whether text qualifies as large text.

    Normal:
        24px or larger

    Bold:
        18.67px or larger
    """

    size_match = re.match(
        r"([\d.]+)px",
        font_size
    )

    if not size_match:
        return False

    size = float(
        size_match.group(1)
    )

    try:

        weight = int(font_weight)

    except (ValueError, TypeError):

        weight = 400

    if weight >= 700:

        return size >= 18.67

    return size >= 24


def scan_contrast(page):

    issues = []

    elements = page.locator("body *")
    element_count = elements.count()

    checked = 0
    passed = 0

    for i in range(element_count):

        element = elements.nth(i)

        # ========================================
        # CHECK VISIBILITY
        # ========================================

        try:

            if not element.is_visible():
                continue

        except Exception:

            continue

        # ========================================
        # SHOW LIVE SCANNING INDICATOR
        # ========================================

        try:

            show_scanning_element(
                page,
                element
            )

            page.wait_for_timeout(100)

        except Exception:

            pass

        # ========================================
        # GET STYLE INFORMATION
        # ========================================

        try:

            data = element.evaluate(
                """
                element => {

                    const style =
                        window.getComputedStyle(element);

                    return {

                        text:
                            element.innerText || "",

                        color:
                            style.color,

                        backgroundColor:
                            style.backgroundColor,

                        fontSize:
                            style.fontSize,

                        fontWeight:
                            style.fontWeight
                    };
                }
                """
            )

        except Exception:

            try:
                clear_scanning_element(
                    page,
                    element
                )
            except Exception:
                pass

            continue

        # ========================================
        # CHECK WHETHER ELEMENT HAS TEXT
        # ========================================

        text = data["text"].strip()

        if not text:

            try:
                clear_scanning_element(
                    page,
                    element
                )
            except Exception:
                pass

            continue

        # ========================================
        # CHECK BACKGROUND
        # ========================================

        background_color = (
            data["backgroundColor"]
        )

        if (
            background_color == "transparent"
            or
            background_color == "rgba(0, 0, 0, 0)"
        ):

            try:
                clear_scanning_element(
                    page,
                    element
                )
            except Exception:
                pass

            continue

        # ========================================
        # PARSE FOREGROUND COLOR
        # ========================================

        foreground = parse_color(
            data["color"]
        )

        if not foreground:

            try:
                clear_scanning_element(
                    page,
                    element
                )
            except Exception:
                pass

            continue

        # ========================================
        # PARSE BACKGROUND COLOR
        # ========================================

        background = parse_color(
            background_color
        )

        if not background:

            try:
                clear_scanning_element(
                    page,
                    element
                )
            except Exception:
                pass

            continue

        # ========================================
        # REAL CONTRAST TEST
        # ========================================

        checked += 1

        # ========================================
        # CALCULATE CONTRAST
        # ========================================

        ratio = contrast_ratio(
            foreground,
            background
        )

        # ========================================
        # DETERMINE TEXT SIZE
        # ========================================

        large = is_large_text(
            data["fontSize"],
            data["fontWeight"]
        )

        required_ratio = (
            3.0
            if large
            else 4.5
        )

        # ========================================
        # CONTRAST FAILURE
        # ========================================

        if ratio < required_ratio:

            try:

                element.scroll_into_view_if_needed()

                page.wait_for_timeout(100)

            except Exception:

                pass

            try:

                xpath = get_xpath(
                    page,
                    element
                )

            except Exception:

                xpath = ""

            text_type = (
                "Large text"
                if large
                else "Normal text"
            )

            issue = AccessibilityIssue(
                page.url,
                element,
                "Color Contrast Failure",
                (
                    f"{text_type} has insufficient "
                    f"color contrast. "
                    f"Contrast ratio: "
                    f"{ratio:.2f}:1. "
                    f"Required: "
                    f"{required_ratio}:1. "
                    f"Text color: "
                    f"{data['color']}. "
                    f"Background color: "
                    f"{background_color}."
                ),
                "High",
                "High"
            )

            issue.xpath = xpath

            issues.append(issue)

        # ========================================
        # CONTRAST PASS
        # ========================================

        else:

            passed += 1

        # ========================================
        # REMOVE LIVE INDICATOR
        # ========================================

        try:

            clear_scanning_element(
                page,
                element
            )

        except Exception:

            pass

    # ========================================
    # RETURN RESULT
    # ========================================

    return ScanResult(
        issues=issues,
        checked=checked,
        passed=passed
    )