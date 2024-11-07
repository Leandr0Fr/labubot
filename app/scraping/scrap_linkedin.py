import math
import re
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ..constants.constants import EMAIL, PSW, TAGS, TAGS_BANNED
from ..decorators.refresh import refresh
from .driver import DriverSingleton


def login():
    driver = DriverSingleton.get_driver()
    base_url = "https://www.linkedin.com/checkpoint/lg/sign-in-another-account"
    driver.get(base_url)
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "username")))
    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys(EMAIL)

    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "password")))
    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys(PSW)

    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Iniciar sesión']"))
    )
    login_button = driver.find_element(By.XPATH, "//button[@aria-label='Iniciar sesión']")
    login_button.click()


@refresh()
def get_jobs(keyword: str) -> dict:
    time.sleep(20)

    driver = DriverSingleton.get_driver()
    base_url = "https://www.linkedin.com/jobs/search/?keywords={}&f_TPR=r86400&origin=JOB_SEARCH_PAGE_JOB_FILTER&sortBy=DD&start="
    driver.get(base_url.format(keyword) + "0")

    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//span[@dir='ltr']")))
    number_jobs = driver.find_element(By.XPATH, "//span[@dir='ltr']")
    jobs_found = get_first_digits(number_jobs.text)
    total_pages = get_num_pags(jobs_found)

    jobs = {}
    for page in range(total_pages):
        page_url = base_url.format(keyword) + str(page * 25)
        driver.get(page_url)
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "jobs-search-results-list"))
        )
        jobs_page_result = get_match_jobs(driver, TAGS)
        if jobs_page_result:
            jobs.update(jobs_page_result)
    return jobs


def get_first_digits(text: str) -> int:
    first_digits = re.search(r"^\d+", text).group()
    return int(first_digits)


def get_num_pags(number_jobs: int) -> int:
    jobs_per_page = 25
    return math.ceil(number_jobs / jobs_per_page)


@refresh()
def get_match_jobs(driver, tags) -> dict:
    jobs_match = {}
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "jobs-search-results-list"))
    )
    results_list = driver.find_element(By.CLASS_NAME, "jobs-search-results-list")
    ul_element = results_list.find_element(By.CLASS_NAME, "scaffold-layout__list-container")
    li_elements = ul_element.find_elements(By.CLASS_NAME, "jobs-search-results__list-item")
    if not li_elements:
        return {}

    scroll_percentage = 0
    for li in li_elements:
        scroll_percentage += 4
        driver.execute_script(
            f"arguments[0].scrollTop = arguments[0].scrollHeight * {scroll_percentage / 100};",
            results_list,
        )
        title_element = li.find_element(By.CLASS_NAME, "job-card-list__title")
        title_strong = title_element.find_element(By.TAG_NAME, "strong")
        title_text = title_strong.text
        title_words = title_text.lower()
        title_words = title_words.replace("(", "").replace(")", "").replace("-", "").replace("/", "")
        title_words = title_words.split()
        if any(tag in title_words for tag in tags) and not any(tag_b in title_words for tag_b in TAGS_BANNED):
            li.click()
            time.sleep(1)
            WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "jobs-description__container"))
            )
            description = extract_description_text(driver)
            jobs_match[title_element.get_attribute("href")] = description

    return jobs_match


@refresh()
def extract_description_text(driver) -> str:
    description_container = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "jobs-description__container"))
    )
    p_container = description_container.find_element(By.CLASS_NAME, "mt4")
    description = p_container.find_element(By.TAG_NAME, "p")
    paragraph_spans = description.find_elements(By.TAG_NAME, "span")
    paragraph_text = " ".join([span.text for span in paragraph_spans])
    return paragraph_text
