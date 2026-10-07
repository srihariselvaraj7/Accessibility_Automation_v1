def get_xpath(page, element):
    return element.evaluate("""
        element => {
            if (element.id) {
                return `//*[@id="${element.id}"]`;
            }

            const parts = [];

            while (element && element.nodeType === Node.ELEMENT_NODE) {
                let index = 1;
                let sibling = element.previousElementSibling;

                while (sibling) {
                    if (sibling.tagName === element.tagName) {
                        index++;
                    }
                    sibling = sibling.previousElementSibling;
                }

                parts.unshift(
                    element.tagName.toLowerCase() + "[" + index + "]"
                );

                element = element.parentElement;
            }

            return "/" + parts.join("/");
        }
    """)