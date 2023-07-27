from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException


class WebdriverOperations:
    _instance = None
    driver = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self):
        if self.__initialized:
            return
        self.driver = self.setup_webdriver()
        self.wait = WebDriverWait(self.driver, 10)
        self.__initialized = True
        self.primary_tab = None

    def setup_webdriver(self):
        service = Service()
        options = webdriver.ChromeOptions()
        return webdriver.Chrome(service=service, options=options)

    def find_element(self, by, value):
        try:
            return self.driver.find_element(by, value)
        except NoSuchElementException:
            return None

    def send_keys(self, by, value, keys, clear=True):
        element = self.find_element(by, value)
        if element:
            if clear:
                element.clear()
            element.send_keys(keys)

    def click(self, by, value):
        element = self.find_element(by, value)
        if element:
            element.click()

    def login(self, username, password):
        self.send_keys(By.NAME, "username", username)
        self.send_keys(By.NAME, "password", password)
        self.send_keys(By.NAME, "password", Keys.ENTER, clear=False)

    def new_tab(self):
        self.driver.execute_script("window.open('about:blank', '_blank');")
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def switch_to_primary_tab(self):
        if self.primary_tab is None:
            self.primary_tab = self.driver.window_handles[0]
        else:
            try:
                current_tab = self.driver.current_window_handle
                if current_tab != self.primary_tab:
                    self.driver.close()
            except NoSuchWindowException:
                pass
        self.driver.switch_to.window(self.primary_tab)

    def open_property(self, property):
        self.click(By.XPATH, "//a[contains(., 'CHANGE PROPERTY')]")
        self.click(By.XPATH, f"//a[contains(., '{property}')]")

    def open_unit(self, unit):
        self.send_keys(By.NAME, "search_input", unit + Keys.ENTER)

    def open_ledger(self):
        self.click(
            By.XPATH,
            "/html/body/table[2]/tbody/tr[4]/td/table/tbody/tr/td/table[3]/tbody/tr[2]/td/table/tbody/tr[last()]/td[4]/a[4]",
        )

    def search_resident(self, resident, num):
        self.click(
            By.XPATH,
            f"/html/body/table[2]/tbody/tr[4]/td/table/tbody/tr/td/table[3]/tbody/tr[1]/td/table/tbody/tr/td[3]/input[{num}]",
        )
        self.send_keys(By.NAME, "ressearch", resident + Keys.ENTER)

    def close(self):
        if self.driver:
            self.driver.quit()
            self.driver = None
