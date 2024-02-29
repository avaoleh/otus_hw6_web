import time

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from opencart.utils import helpers

import os
from dotenv import load_dotenv

load_dotenv()
AUTHORIZATION_URL = os.getenv("AUTHORIZATION_LINK")
LOGIN_URL = os.getenv("LOGIN_LINK")

person = helpers.Client()
FIRSTNAME_TEST = person.first_name
LASTNAME_TEST = person.last_name
EMAIL_TEST = person.email
PASSWORD_TEST = person.password

def test_check_title(browser):
    browser.get(AUTHORIZATION_URL)
    wait = WebDriverWait(browser, 5)
    wait.until(EC.title_is("Register Account"))

def test_form(browser):
    browser.get(AUTHORIZATION_URL)
    wait = WebDriverWait(browser, 10)

    input_firstname = wait.until(EC.visibility_of_element_located((By.ID, "input-firstname")))
    input_firstname.send_keys(FIRSTNAME_TEST)

    input_lastname = wait.until(EC.visibility_of_element_located((By.ID, "input-lastname")))
    input_lastname.send_keys(LASTNAME_TEST)

    password = wait.until(EC.visibility_of_element_located((By.ID, "input-password")))
    password.send_keys(PASSWORD_TEST)

    email = wait.until(EC.visibility_of_element_located((By.ID, "input-email")))
    email.send_keys(EMAIL_TEST)

    policy = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="form-register"]/div/div/input')))
    browser.execute_script("arguments[0].click();", policy)

    submit_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="form-register"]/div/button')))
    browser.execute_script("arguments[0].click();", submit_btn)


    wait.until(EC.title_is("Your Account Has Been Created!"))

    logout = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="column-right"]/div/a[13]')))
    browser.execute_script("arguments[0].click();", logout)

    wait.until(EC.title_is("Account Logout"))


def test_login(browser):
    browser.get(LOGIN_URL)
    wait = WebDriverWait(browser, 10)

    email = wait.until(EC.visibility_of_element_located((By.ID, "input-email")))
    email.send_keys(EMAIL_TEST)

    password = wait.until(EC.visibility_of_element_located((By.ID, "input-password")))
    password.send_keys(PASSWORD_TEST)

    submit_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="form-login"]/div[3]/button')))
    browser.execute_script("arguments[0].click();", submit_btn)
