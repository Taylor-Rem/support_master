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


class HelperWidget(QWidget):
    def __init__(self, main_app, title):
        super().__init__()
        self.main_app = main_app
        self.setWindowTitle(title)

        # Create layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.label = QLabel(title, self)
        self.back_btn = self.create_button("Back", self.go_back)

    def go_back(self):
        self.main_app.stack.setCurrentWidget(self.main_app.main_window)

    def create_button(self, text, callback):
        button = QPushButton(text, self)
        button.clicked.connect(callback)
        self.layout.addWidget(button)
        return button


class TicketHelper(HelperWidget):
    def __init__(self, main_app, open_tickets):
        super().__init__(main_app, "Ticket Helper")
        self.open_tickets = open_tickets
        self.open_btn = self.create_button("Open Ticket", self.open_ticket)

    def open_ticket(self):
        self.open_tickets.open_ticket()


class ReportHelper(HelperWidget):
    def __init__(self, main_app):
        super().__init__(main_app, "Report Helper")


class App(QWidget):
    def __init__(self):
        super().__init__()

        # Create stacked widget
        self.stack = QStackedWidget()

        # Initialize UI components
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Support Master")

        self.init_main_window()
        self.init_ticket_helper()
        self.init_report_helper()

        self.stack.addWidget(self.main_window)
        self.stack.addWidget(self.ticket_helper)
        self.stack.addWidget(self.report_helper)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.stack)

    def init_main_window(self):
        self.main_window = QWidget()
        main_layout = QVBoxLayout()
        self.main_window.setLayout(main_layout)
        self.create_button("Ticket Helper", self.switch_to_ticket, main_layout)
        self.create_button("Report Helper", self.switch_to_report, main_layout)
        self.create_button("Quit App", self.close, main_layout)

    def init_ticket_helper(self):
        self.ticket_helper = TicketHelper(self, None)

    def init_report_helper(self):
        self.report_helper = ReportHelper(self)

    def create_button(self, text, callback, layout):
        button = QPushButton(text, self)
        button.clicked.connect(callback)
        layout.addWidget(button)

    def switch_to_ticket(self):
        # remove the old ticket helper from the stack
        index = self.stack.indexOf(self.ticket_helper)
        if index != -1:
            self.stack.removeWidget(self.ticket_helper)

        # initialize the new ticket helper
        self.webdriver_operations = WebdriverOperations()
        self.open_tickets = OpenTickets(self.webdriver_operations)
        self.ticket_helper = TicketHelper(self, self.open_tickets)

        # add the new ticket helper to the stack and switch to it
        self.stack.addWidget(self.ticket_helper)
        self.stack.setCurrentWidget(self.ticket_helper)

    def switch_to_report(self):
        self.stack.setCurrentWidget(self.report_helper)


if __name__ == "__main__":
    app = QApplication([])
    main_app = App()
    main_app.show()
    app.exec_()
