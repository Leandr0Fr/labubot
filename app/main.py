import time

from dotenv import load_dotenv

from .constants.constants import KEYWORDS
from .constants.match_enum import Match_Color
from .gemini.match_prompt_cv import match_cv
from .scraping.scrap_linkedin import LinkedInJobScraper
from .telegram.telegram_bot import send_keyword, send_no_jobs, send_offers


def main():
    load_dotenv()
    scraper = LinkedInJobScraper()
    scraper.login()
    for keyword in KEYWORDS:
        scraper.reboot_data()
        jobs = scraper.get_jobs(keyword)
        offers = ""
        cont = 0
        for url, job in jobs.items():
            time.sleep(1)
            match = match_cv(job)
            color = ""
            if match == Match_Color.AMARILLO:
                color = "🟡"
            if match == Match_Color.VERDE:
                color = "🟢"
            if color:
                offers += f"Se encontró una oferta {color}: {url}\n"
                cont += 1
                if cont == 5:
                    send_offers(offers)
                    cont = 0
                    offers = ""
        if offers:
            send_offers(offers)
        if jobs:
            send_keyword(keyword)
        else:
            send_no_jobs(keyword)
        jobs.clear()


if __name__ == "__main__":
    main()
