from dotenv import load_dotenv

from .scraping.scrap_linkedin import get_jobs


def main():
    load_dotenv()
    get_jobs()


if __name__ == "__main__":
    main()
