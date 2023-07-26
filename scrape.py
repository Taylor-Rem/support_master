from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_operations import WebdriverOperations


class Scrape:
    # XPATHs
    ticket_property_xpath = "/html/body/div[1]/div[19]/div/main/div/div/div/div/div[2]/div/div/table/tbody/tr[6]/td[2]/strong/a"
    ticket_unit_xpath = "/html/body/div[1]/div[19]/div/main/div/div/div/div/div[2]/div/div/table/tbody/tr[11]/td[2]/a/strong"
    ticket_resident_xpath = "/html/body/div[1]/div[19]/div/main/div/div/div/div/div[2]/div/div/table/tbody/tr[12]/td[2]/a/strong"
    resident_xpath = "/html/body/table[2]/tbody/tr[4]/td/table/tbody/tr/td/table[3]/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/a"

    def __init__(self):
        self.webdriver = WebdriverOperations()

    def scrape_ticket(self):
        try:
            property_element = self.webdriver.driver.find_element(
                By.XPATH, self.ticket_property_xpath
            )
            property = property_element.get_attribute("innerHTML")
        except NoSuchElementException:
            property = None

        try:
            unit_element = self.webdriver.driver.find_element(
                By.XPATH, self.ticket_unit_xpath
            )
            unit = unit_element.get_attribute("innerHTML")
        except NoSuchElementException:
            unit = None

        try:
            resident_element = self.webdriver.driver.find_element(
                By.XPATH, self.ticket_resident_xpath
            )
            resident = resident_element.get_attribute("innerHTML").strip()
        except NoSuchElementException:
            resident = None

        return property, unit, resident

    def compare_resident(self, resident):
        try:
            RM_resident_element = self.webdriver.driver.find_element(
                By.XPATH, self.resident_xpath
            )
            RM_resident = RM_resident_element.get_attribute("innerHTML").strip()
            if resident in RM_resident:
                return True
            else:
                return False
        except NoSuchElementException:
            return False
