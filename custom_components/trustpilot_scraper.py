from langflow import CustomComponent
from langflow.schema.message import Message
from playwright.sync_api import sync_playwright
import re

class TrustpilotScraper(CustomComponent):
    display_name = "Trustpilot Scraper"
    description = "Scrapes reviews from Trustpilot using Playwright."

    def build_config(self):
        return {
            "url_input": {
                "display_name": "Website URL",
                "type": "str",
                "required": True
            }
        }

    def build(self, url_input: str) -> str:
        domain = self.extract_domain(url_input)

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            try:
                page.goto("https://www.trustpilot.com/")
                page.fill('input[name="query"]', domain)
                page.keyboard.press("Enter")
                page.wait_for_timeout(3000)

                first_result = page.locator('a[href*="/review/"]').first
                first_result.click()

                page.wait_for_timeout(3000)

                reviews = page.locator('[data-service-review-text-typography]')
                stars = page.locator('[data-service-review-rating]')
                usernames = page.locator('[data-consumer-name-typography]')

                scraped_reviews = []
                for i in range(min(reviews.count(), 5)):
                    scraped_reviews.append({
                        "user": usernames.nth(i).inner_text(),
                        "stars": stars.nth(i).inner_text(),
                        "review": reviews.nth(i).inner_text(),
                    })

                return str(scraped_reviews)

            except Exception as e:
                return f"[ERROR] Trustpilot scrape failed: {e}"
            finally:
                browser.close()

    def extract_domain(self, url):
        domain = re.sub(r"https?://(www\.)?", "", url)
        return domain.split("/")[0]