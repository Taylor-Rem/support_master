from open_tickets import OpenTickets
from webdriver_operations import WebdriverOperations
from PyQt5.QtWidgets import (
    QApplication,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLabel,
    QStackedWidget,
)
from config import username, password, management_portal, resident_map
from os_interact import OSInteract
from filter_properties import FilterProperties


class HelperWidget(QWidget):
    def __init__(self, main_app, title):
        super().__init__()
        self.main_app = main_app
        self.setWindowTitle(title)

        # Create layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel(title, self)

    def go_back(self):
        self.main_app.stack.setCurrentWidget(self.main_app.main_window)

    def create_button(self, text, callback):
        button = QPushButton(text, self)
        button.clicked.connect(callback)
        self.layout.addWidget(button)
        return button


class TicketHelper(HelperWidget):
    def __init__(self, main_app):
        super().__init__(main_app, "Ticket Helper")
        self.open_btn = self.create_button("Open Ticket", self.open_ticket)
        self.back_btn = self.create_button("Back", self.go_back)
        self.open_tickets = OpenTickets(main_app.webdriver)

    def open_ticket(self):
        if self.open_tickets:
            self.open_tickets.open_ticket()


class ChooseReport(HelperWidget):
    def __init__(self, main_app):
        super().__init__(main_app, "Choose Report")
        self.zero_btn = self.create_button(
            "Zero Report", lambda: self.switch_to_report("zero_report")
        )
        self.double_btn = self.create_button(
            "Double Report", lambda: self.switch_to_report("double_report")
        )
        self.moveout_btn = self.create_button(
            "Moveout Report", lambda: self.switch_to_report("moveout_report")
        )
        self.back_btn = self.create_button("Back", self.go_back)

    def switch_to_report(self, report_type):
        self.main_app.stack.setCurrentWidget(self.main_app.report_helper)
        self.main_app.report_helper.set_report_type(report_type)
        filter_properties = FilterProperties(report_type)
        self.main_app.report_helper.retrieve_report_information(
            filter_properties.filter_properties()
        )


class ReportHelper(HelperWidget):
    def __init__(self, main_app, report_type):
        self._report_type = report_type
        label_text = ""
        super().__init__(main_app, label_text)
        self.complete_btn = self.create_button("Complete", self.complete)
        self.skip_btn = self.create_button("Skip", self.skip)
        self.back_btn = self.create_button("Back", self.go_back)
        self.report_type = report_type

    def set_report_type(self, report_type):
        self._report_type = report_type
        self.label.setText(f"{report_type.replace('_', ' ')}")

    def retrieve_report_information(self, properties, units, residents):
        print(properties, units, residents)

    def complete(self):
        print("Complete!")

    def skip(self):
        print("Skipped!")


class App(QWidget):
    def __init__(self):
        super().__init__()
        # Create stacked widget
        self.stack = QStackedWidget()

        # Init WebdriverOperations
        self.webdriver = WebdriverOperations()

        # Initialize UI components
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Support Master")

        self.init_main_window()
        self.init_ticket_helper()
        self.init_choose_report()
        self.init_report_helper()

        self.stack.addWidget(self.main_window)
        self.stack.addWidget(self.ticket_helper)
        self.stack.addWidget(self.choose_report)
        self.stack.addWidget(self.report_helper)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.stack)

    def init_main_window(self):
        self.main_window = QWidget()
        main_layout = QVBoxLayout()
        self.main_window.setLayout(main_layout)
        self.create_button("Ticket Helper", self.switch_to_ticket, main_layout)
        self.create_button("Choose Report", self.switch_to_report, main_layout)
        self.create_button("Quit App", self.quit_app, main_layout)

    def init_ticket_helper(self):
        self.ticket_helper = TicketHelper(self)

    def init_choose_report(self):
        self.choose_report = ChooseReport(self)

    def init_report_helper(self):
        self.report_helper = ReportHelper(self, "")

    def create_button(self, text, callback, layout):
        button = QPushButton(text, self)
        button.clicked.connect(callback)
        layout.addWidget(button)

    def switch_to_ticket(self):
        self.stack.setCurrentWidget(self.ticket_helper)
        self.open_program(management_portal)

    def switch_to_report(self):
        self.stack.setCurrentWidget(self.choose_report)
        self.open_program(resident_map)

    def open_program(self, site):
        self.webdriver.driver.get(site)
        self.webdriver.login(username, password)

    def quit_app(self):
        self.close()
        self.webdriver.driver.quit()


if __name__ == "__main__":
    OSInteract().create_folders()
    app = QApplication([])
    main_app = App()
    main_app.show()
    app.exec_()
