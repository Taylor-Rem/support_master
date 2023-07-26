from datetime import datetime
import os


class OSInteract:
    def __init__(self):
        now = datetime.now()
        year = now.year
        month = now.month
        day = now.day
        username = "taylorremund"
        self.root_path = f"/Users/{username}/Desktop/Reports/{year}/{month}/{day}/"
        self.reports = [
            "zero_report",
            "double_report",
            "redstar_report",
            "moveout_report",
        ]

    def create_folders(self):
        for report in self.reports:
            report_path = self.root_path + report
            if not os.path.exists(report_path):
                os.makedirs(report_path)
