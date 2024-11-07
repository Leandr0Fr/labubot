import time

from dotenv import load_dotenv

from .constants.constants import KEYWORDS
from .constants.match_enum import Match_Color
from .gemini.match_prompt_cv import match_cv
from .scraping.scrap_linkedin import get_jobs, login
from .telegram.telegram_bot import send_keyword, send_offers


def main():
    load_dotenv()
    login()
    urls_used = []
    for keyword in KEYWORDS:
        jobs = get_jobs(keyword)
        offers = ""
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
                offers += f"Se encontró una oferta {color}: {url}\n"
        send_keyword(keyword)
        send_offers(offers)


if __name__ == "__main__":
    main()
