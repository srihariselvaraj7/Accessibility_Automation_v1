def show_scanning_element(page, locator):
    try:
        locator.scroll_into_view_if_needed()
        page.wait_for_timeout(150)

        locator.evaluate("""
            element => {
                element.dataset.originalOutline =
                    element.style.outline;

                element.style.outline = '3px solid red';
                element.style.outlineOffset = '3px';
            }
        """)

    except Exception:
        pass


def clear_scanning_element(page, locator):
    try:
        locator.evaluate("""
            element => {
                element.style.outline =
                    element.dataset.originalOutline || '';

                element.style.outlineOffset = '';
                delete element.dataset.originalOutline;
            }
        """)

    except Exception:
        pass