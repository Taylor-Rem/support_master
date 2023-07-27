from scrape import Scrape
from config import username, password, resident_map
from selenium.common.exceptions import NoSuchElementException


class OpenTickets:
    def __init__(self, webdriver):
        self.webdriver = webdriver
        self.scrape = Scrape(webdriver)

    def open_ticket(self):
        self.webdriver.switch_to_primary_tab()
        property, unit, resident = self.scrape.scrape_ticket()
        print(property, unit, resident)
        self.open_resident_tab(property, unit, resident)

    def open_resident_tab(self, property, unit, resident):
        self.webdriver.new_tab()
        self.webdriver.driver.get(resident_map)
        self.webdriver.login(username, password)
        self.webdriver.open_property(property)
        self.check_and_open_unit_or_resident(unit, resident)

    def check_and_open_unit_or_resident(self, unit, resident):
        if unit is not None:
            self.webdriver.open_unit(unit)
            if resident is None or self.scrape.compare_resident(resident):
                self.webdriver.open_ledger()
            else:
                self.search_resident_and_open_ledger(resident)

    def search_resident_and_open_ledger(self, resident):
        try:
            self.webdriver.search_resident(resident, 2)
            self.webdriver.open_ledger()
        except NoSuchElementException:
            self.webdriver.search_resident(resident, 1)
            self.webdriver.open_ledger()
