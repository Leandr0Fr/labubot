import time

from dotenv import load_dotenv

from .constants.constants import KEYWORDS
from .constants.match_enum import Match_Color
from .gemini.match_prompt_cv import match_cv
from .scraping.scrap_linkedin import LinkedInJobScraper
from .telegram.telegram_bot import send_keyword, send_offers


def main():
    load_dotenv()
    scraper = LinkedInJobScraper()
    scraper.login()
    urls_used = []
    for keyword in KEYWORDS:
        scraper.reboot_data()
        jobs = scraper.get_jobs(keyword)
        for url, job in jobs.items():
            if url in urls_used:
                continue
            time.sleep(1)
            match = match_cv(job)
            color = ""
            if match == Match_Color.AMARILLO:
                color = "🟡"
            if match == Match_Color.VERDE:
                color = "🟢"
            if color:
                urls_used.append(url)
                send_offers(f"Se encontró una oferta {color}: {url}\n")
        send_keyword(keyword)


if __name__ == "__main__":
    main()
