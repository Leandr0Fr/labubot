import time

from dotenv import load_dotenv

from .constants.constants import KEYWORDS
from .constants.match_enum import Match_Color
from .gemini.match_prompt_cv import match_cv
from .scraping.scrap_linkedin import get_jobs, login
from .telegram.telegram_bot import send_keyword, send_ofert


def main():
    load_dotenv()
    login()
    for keyword in KEYWORDS:
        jobs = get_jobs(keyword)
        send_keyword(keyword)
        for url, job in jobs.items():
            time.sleep(1)
            match = match_cv(job)
            color = ""
            if match == Match_Color.AMARILLO:
                color = "🟡"
            if match == Match_Color.VERDE:
                color = "🟢"
            if match == Match_Color.ROJO:
                continue
            send_ofert(url, color)


if __name__ == "__main__":
    main()
