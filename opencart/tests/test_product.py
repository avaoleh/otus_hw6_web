import time

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
from dotenv import load_dotenv

load_dotenv()
PRODUCTPAGE_URL = os.getenv("OPENCART_LINK_CARD")

macbook_price = ["$602.00", "£368.73", "472.33€"]


def test_check_title(browser):
    browser.get(PRODUCTPAGE_URL)
    wait = WebDriverWait(browser, 5)
    wait.until(EC.title_is("MacBook"))


def test_check_product_name(browser):
    browser.get(PRODUCTPAGE_URL)
    wait = WebDriverWait(browser, 5)
    wait.until(
        EC.text_to_be_present_in_element(
            (By.XPATH, "//div[@id='content']//h1"), "MacBook"
        )
    )


def test_check_price(browser):
    browser.get(PRODUCTPAGE_URL)

    wait = WebDriverWait(browser, 5)
    card_price = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//span[@class='price-new']"))
    )

    cash_type = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//div[@class='dropdown']/a[@class='dropdown-toggle']/strong")
        )
    )

    if cash_type.text == "$":
        assert (
            card_price.text == macbook_price[0]
        ), f"The actual price is {card_price.text}"
    elif cash_type.text == "£":
        assert (
            card_price.text == macbook_price[1]
        ), f"The actual price is {card_price.text}"
    elif cash_type.text == "€":
        assert (
            card_price.text == macbook_price[2]
        ), f"The actual price is {card_price.text}"


@pytest.mark.skip(reason="flaky test")
def test_add_to_cart(browser):
    browser.get(PRODUCTPAGE_URL)
    browser.execute_script("window.scrollTo(0, 500)")
    wait = WebDriverWait(browser, 5)
    add_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[@id='button-cart']"))
    )
    add_btn.click()
    time.sleep(3)

    notice_add = wait.until(
        (
            EC.visibility_of_element_located(
                (By.XPATH, "//div[@class='alert alert-success alert-dismissible']")
            )
        )
    )

    assert (
        notice_add.text == "Success: You have added MacBook to your shopping cart!"
    ), f"{notice_add.text}"


@pytest.mark.skip(reason="flaky test")
def test_qyt_default(browser):
    browser.get(PRODUCTPAGE_URL)
    wait = WebDriverWait(browser, 5)
    input_quantity = wait.until(
        EC.visibility_of_element_located((By.XPATH, '//input[@id="input-quantity"]'))
    )

    assert (
        int(input_quantity.text) == 1
    ), f"Default quantity is {input_quantity.text}, but should be 1!"
