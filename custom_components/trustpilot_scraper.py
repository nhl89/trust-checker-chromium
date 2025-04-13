from langflow import CustomComponent
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

class TrustpilotScraper(CustomComponent):
    display_name = "Trustpilot Scraper"
    description = "Extract Trustpilot review data from company Trustpilot page."

    def build_config(self):
        return {
            "url": {
                "display_name": "Trustpilot URL",
                "type": "str",
                "required": True
            }
        }

    def build(self, url: str, **kwargs) -> str:
        if not url.startswith("http"):
            return "[ERROR] Invalid URL"

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url, timeout=60000)
                page.wait_for_selector("section.styles_reviewsOverview__JDbNU", timeout=15000)

                html = page.content()
                soup = BeautifulSoup(html, "html.parser")

                reviews_section = soup.find("section", class_="styles_reviewsOverview__JDbNU")
                reviews = reviews_section.get_text(separator="\n", strip=True) if reviews_section else "No reviews found."

                browser.close()
                return reviews

        except Exception as e:
            return f"[ERROR] Failed to extract Trustpilot data: {e}"