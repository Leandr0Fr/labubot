import math
import re
import time

from selenium.webdriver.common.by import By

from ..constants.constants import EMAIL, KEYWORDS, PSW
from .driver import DriverSingleton


def login():
    driver = DriverSingleton.get_driver()
    base_url = "https://www.linkedin.com/login/es?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin"

    driver.get(base_url)
    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys(EMAIL)
    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys(PSW)

    login_button = driver.find_element(By.XPATH, "//button[@aria-label='Iniciar sesión']")
    login_button.click()


def get_jobs():
    login()
    time.sleep(10)

    driver = DriverSingleton.get_driver()
    base_url = "https://www.linkedin.com/jobs/search/?keywords=desarrollador&f_TPR=r86400&origin=JOB_SEARCH_PAGE_JOB_FILTER&sortBy=DD&start={}"
    driver.get(base_url)

    number_jobs = driver.find_element(By.XPATH, "//span[@dir='ltr']")
    jobs_found = get_first_digits(number_jobs.text)
    total_pages = get_num_pags(jobs_found)

    jobs = {}
    for page in range(total_pages):
        page_url = base_url.format(page * 25)
        driver.get(page_url)
        jobs.update(get_match_jobs(driver, KEYWORDS))

    return jobs


def get_first_digits(text: str) -> int:
    first_digits = re.search(r"^\d+", text).group()
    return int(first_digits)


def get_num_pags(number_jobs: int) -> int:
    jobs_per_page = 25
    return math.ceil(number_jobs / jobs_per_page)


def get_match_jobs(driver, keywords) -> dict:
    jobs_match = {}
    results_list = driver.find_element(By.CLASS_NAME, "jobs-search-results-list")
    ul_element = results_list.find_element(By.CLASS_NAME, "scaffold-layout__list-container")
    li_elements = ul_element.find_elements(By.CLASS_NAME, "jobs-search-results__list-item")
    matchs = 0
    scroll_percentage = 0
    for li in li_elements:
        scroll_percentage += 4
        driver.execute_script(
            f"arguments[0].scrollTop = arguments[0].scrollHeight * {scroll_percentage / 100};", results_list
        )
        title_element = li.find_element(By.CLASS_NAME, "job-card-list__title")
        title_strong = title_element.find_element(By.TAG_NAME, "strong")
        title_text = title_strong.text
        title_words = title_text.lower().split()
        time.sleep(4)

        if any(keyword.lower() in title_words for keyword in keywords):
            li.click()
            time.sleep(4)
            matchs += 1
            description = extract_description_text(driver)
            jobs_match[title_element.get_attribute("href")] = description

    return jobs_match


def extract_description_text(driver) -> str:
    description_container = driver.find_element(By.CLASS_NAME, "jobs-description__container")
    p_container = description_container.find_element(By.CLASS_NAME, "mt4")
    description = p_container.find_element(By.TAG_NAME, "p")
    paragraph_spans = description.find_elements(By.TAG_NAME, "span")

    paragraph_text = " ".join([span.text for span in paragraph_spans])
    return paragraph_text
