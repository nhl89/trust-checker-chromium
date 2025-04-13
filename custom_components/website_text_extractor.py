from langflow import CustomComponent
import requests
from bs4 import BeautifulSoup

class WebsiteTextExtractor(CustomComponent):
    display_name = "Website Text Extractor"
    description = "Extract visible text from a given website URL."

    def build_config(self):
        return {
            "url": {
                "display_name": "Website URL",
                "type": "str",
                "required": True
            }
        }

    def build(self, url: str, **kwargs) -> str:
        if not url.startswith("http"):
            return f"[ERROR] Invalid URL: {url}"

        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            visible_text = soup.get_text(separator=" ", strip=True)

            if not visible_text:
                return f"[WARNING] No visible text found on {url}"

            return visible_text

        except Exception as e:
            return f"[ERROR] Could not fetch {url}: {e}"