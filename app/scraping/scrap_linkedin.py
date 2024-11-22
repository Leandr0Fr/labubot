import math
import re
import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ..constants.constants import EMAIL, PSW, TAGS, TAGS_BANNED
from ..decorators.refresh import refresh
from .driver import DriverSingleton


class LinkedInJobScraper:
    def __init__(self):
        self.actual_page = 0
        self.total_pages = 0
        self.driver = DriverSingleton.get_driver()
        self.jobs_used = []

    @refresh()
    def login(self) -> None:
        base_url = "https://www.linkedin.com/checkpoint/lg/sign-in-another-account"
        self.driver.get(base_url)
        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.ID, "username")))
        username_input = self.driver.find_element(By.ID, "username")
        username_input.send_keys(EMAIL)

        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.ID, "password")))
        password_input = self.driver.find_element(By.ID, "password")
        password_input.send_keys(PSW)

        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Iniciar sesión']"))
        )
        login_button = self.driver.find_element(By.XPATH, "//button[@aria-label='Iniciar sesión']")
        login_button.click()

    @refresh()
    def get_jobs(self, keyword: str) -> dict:
        time.sleep(30)
        base_url = "https://www.linkedin.com/jobs/search/?keywords={}&f_TPR=r86400&origin=JOB_SEARCH_PAGE_JOB_FILTER&sortBy=DD&start="
        self.driver.get(base_url.format(keyword) + "0")
        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//span[@dir='ltr']"))
        )
        number_jobs = self.driver.find_element(By.XPATH, "//span[@dir='ltr']")
        jobs_found = self.get_first_digits(number_jobs.text)
        self.total_pages = self.get_num_pags(jobs_found)
        jobs = self.get_matchs(keyword, base_url)
        return jobs

    @refresh()
    def get_matchs(self, keyword, base_url):
        jobs = {}
        while self.actual_page < self.total_pages:
            page_url = base_url.format(keyword) + str(self.actual_page * 25)
            self.driver.get(page_url)
            if self.check_element_exists_by_class("jobs-search-no-results-banner"):
                return jobs
            WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "jobs-search-results-list"))
            )
            jobs_page_result = self.get_match_jobs(TAGS)
            if jobs_page_result:
                jobs.update(jobs_page_result)
            self.actual_page += 1
        return jobs

    @refresh()
    def get_match_jobs(self, tags) -> dict:
        jobs_match = {}
        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "jobs-search-results-list"))
        )
        results_list = self.driver.find_element(By.CLASS_NAME, "jobs-search-results-list")
        ul_element = results_list.find_element(By.CLASS_NAME, "scaffold-layout__list-container")
        li_elements = ul_element.find_elements(By.CLASS_NAME, "jobs-search-results__list-item")
        if not li_elements:
            return {}
        scroll_percentage = 0
        for li in li_elements:
            scroll_percentage += 4
            self.driver.execute_script(
                f"arguments[0].scrollTop = arguments[0].scrollHeight * {scroll_percentage / 100};",
                results_list,
            )
            title_element = li.find_element(By.CLASS_NAME, "job-card-list__title")
            title_strong = title_element.find_element(By.TAG_NAME, "strong")
            title_words = self.clean_title(title_strong.text)
            title_words = title_words.split()
            if any(tag in title_words for tag in tags) and not any(
                tag_b in title_words for tag_b in TAGS_BANNED
            ):
                url = title_element.get_attribute("href")
                job_id = self.extract_job_id(url)
                if job_id not in self.jobs_used:
                    li.click()
                    time.sleep(1)
                    WebDriverWait(self.driver, 20).until(
                        EC.visibility_of_element_located((By.CLASS_NAME, "jobs-description__container"))
                    )
                    description = self.extract_description_text()
                    jobs_match[url] = description
                    self.jobs_used.append(job_id)

        return jobs_match

    def extract_job_id(self, url) -> str:
        match = re.search(r"/jobs/view/(\d+)", url)
        return match.group(1) if match else None

    def clean_title(self, title):
        title_words = title.lower()
        title_words = (
            title_words.replace("(", " ")
            .replace(")", " ")
            .replace("-", " ")
            .replace("/", " ")
            .replace(".", " ")
            .replace("+", " ")
            .replace(",", " ")
            .replace("|", " ")
        )

        return title_words

    @refresh()
    def extract_description_text(self) -> str:
        description_container = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "jobs-description__container"))
        )
        p_container = description_container.find_element(By.CLASS_NAME, "mt4")
        description = p_container.find_element(By.TAG_NAME, "p")
        paragraph_spans = description.find_elements(By.TAG_NAME, "span")
        paragraph_text = " ".join([span.text for span in paragraph_spans])
        return paragraph_text

    def reboot_data(self) -> None:
        self.actual_page = 0
        self.total_pages = 0

    def check_element_exists_by_class(self, class_name):
        try:
            self.driver.find_element(By.CLASS_NAME, class_name)
            return True
        except NoSuchElementException:
            return False

    def get_first_digits(self, text: str) -> int:
        first_digits = re.search(r"^\d+", text).group()
        return int(first_digits)

    def get_num_pags(self, number_jobs: int) -> int:
        jobs_per_page = 25
        return math.ceil(number_jobs / jobs_per_page)
