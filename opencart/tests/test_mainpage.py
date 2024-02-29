import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
from dotenv import load_dotenv

load_dotenv()
MAINPAGE_URL = os.getenv("OPENCART_LINK")

cash_enum = ["€", "£", "$"]
cash_locators = [
    "(//ul[@class ='dropdown-menu show']/li)[1]",
    "(//ul[@class ='dropdown-menu show']/li)[2]",
    "(//ul[@class ='dropdown-menu show']/li)[3]",
]

footer_txt = """Powered By OpenCart
Your Store © 2024"""


def test_check_title(browser):
    browser.get(MAINPAGE_URL)
    wait = WebDriverWait(browser, 5)
    wait.until(EC.title_is("Your Store"))


def test_check_carousel(browser):
    browser.get(MAINPAGE_URL)
    wait = WebDriverWait(browser, 5)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".carousel-inner")))


def test_check_cash(browser):
    browser.get(MAINPAGE_URL)

    for i in range(2):
        cash_select = browser.find_element(By.CSS_SELECTOR, ".dropdown")
        cash_select.click()

        cash_select_item = browser.find_element(By.XPATH, cash_locators[i])
        cash_select_item.click()
        product = browser.find_element(By.CSS_SELECTOR, ".price-new")

        if i == 0:
            assert product.text[-1] == cash_enum[i], f"Cash is {product.text[-1]}"
        else:
            assert product.text[0] == cash_enum[i], f"Cash is {product.text[0]}"


@pytest.mark.skip(
    reason="no way of currently testing this...btn_add_to_cart is not clickable"
)
def test_add_to_cart(browser):
    browser.get(MAINPAGE_URL)
    browser.execute_script("window.scrollTo(0, 500)")
    wait = WebDriverWait(browser, 5)
    btn_add_to_cart = wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//div[@class='button-group']/button[@data-bs-original-title='Add to Cart']",
            )
        )
    )
    browser.execute_script("arguments[0].click();", btn_add_to_cart)

    cart = browser.find_element(By.XPATH, "//button[@data-bs-toggle='dropdown']")
    assert int(cart.text[0]) > 0, f"Didn't add to cart any products"


def test_footer_text(browser):
    browser.get(MAINPAGE_URL)
    wait = WebDriverWait(browser, 5)
    wait.until(
        EC.text_to_be_present_in_element((By.XPATH, "//footer/div/p"), "Powered By ")
    )

    footer_text = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//footer/div/p"))
    )
    assert footer_text.text == footer_txt, f"Footer text is {footer_text.text}"
