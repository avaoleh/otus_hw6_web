from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from mimesis import Person
from random import random

def wait_title(title, driver, timeout=3):
    try:
        WebDriverWait(driver, timeout).until(EC.title_is(title))
    except TimeoutException:
        # Выбрасываю своё исключение и добавляю сообщение
        raise AssertionError(
            f"Ждал что title будет: '{title}' но он был '{driver.title}'"
        )


def assert_element(selector, driver, timeout=1, by=By.CSS_SELECTOR):
    try:
        return WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((by, selector))
        )
    except TimeoutException:
        driver.save_screenshot(f"{driver.session_id}.png")
        raise AssertionError(f"Не дождался видимости элемента: {selector}")



class Client():
    _person = Person()

    def __init__(self):
        self.__type = 'Client'
        self.first_name = self._person.name()
        self.last_name = self._person.surname()
        self.email = self._person.email()
        self.password = self._person.password()

