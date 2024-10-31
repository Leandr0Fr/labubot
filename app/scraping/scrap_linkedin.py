import time

from selenium.webdriver.common.by import By

from ..constants.constants import EMAIL, PSW
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
    driver = DriverSingleton.get_driver()
    base_url = "https://www.linkedin.com/jobs/search/?currentJobId=4062834304&f_TPR=r86400&keywords=desarrollador&origin=JOB_SEARCH_PAGE_JOB_FILTER&sortBy=DD"
    driver.get(base_url)
    time.sleep(10)
