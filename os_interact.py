from datetime import datetime
import os
import fitz
import re
import json
import pandas as pd


class OSInteract:
    def __init__(self):
        now = datetime.now()
        year = now.year
        month = now.month
        day = now.day
        username = "taylorremund"
        self.root_path = f"/Users/{username}/Desktop/Reports/{year}/{month}/"
        self.reports_path = os.path.join(self.root_path, f"{day}/")
        self.json_path = os.path.join(self.root_path, "json_reports/")
        self.reports = [
            "zero_report",
            "double_report",
            "redstar_report",
            "moveout_report",
        ]
        self.csv_handler = CSVHandler()
        self.pdf_handler = PDFHandler()
        self.json_operations = JsonOperations(self.json_path)

    def create_folders(self):
        for report in self.reports:
            report_path = os.path.join(self.reports_path, report)
            if not os.path.exists(report_path):
                os.makedirs(report_path)
        if not os.path.exists(self.json_path):
            os.makedirs(self.json_path)

    def retrieve_report_info(self, report):
        path = os.path.join(self.reports_path, report)
        file_name = os.listdir(path)[-1]
        file_path = os.path.join(path, file_name)

        if file_name.endswith(".csv"):
            return self.csv_handler.retrieve_csv_info(file_path)
        else:
            return self.pdf_handler.retrieve_pdf_info(file_path)


class CSVHandler:
    def retrieve_csv_info(self, path):
        if os.path.isfile(path):
            df = pd.read_csv(path)
        else:
            print(f"File does not exist: {path}")
            return None
        properties = df.filter(like="Property Name").values.flatten().tolist()
        units = df.filter(like="Space Number").values.flatten().tolist()
        residents = df.filter(like="Resident").values.flatten().tolist()
        return properties, units, residents


class PDFHandler:
    def retrieve_pdf_info(self, path):
        pdf_text = []
        numbers = []
        with fitz.open(path) as pdf:
            for page_number in range(pdf.page_count):
                page = pdf.load_page(page_number)
                page_text, _ = self.extract_text_and_links(page)

                # Extract property name and unit number using regular expressions
                matches = re.findall(r"([\w\s]+)\s+(\d+\.\d+)", page_text)
                if matches:
                    pdf_text.extend(match[0].split("\n")[-1] for match in matches)
                    numbers.extend(match[1] for match in matches)

        properties = pdf_text[0::2]
        units = numbers[0::2]
        residents = pdf_text[1::2]

        return properties, units, residents

    def extract_text_and_links(self, page):
        text = page.get_text()
        links = []

        for link in page.get_links():
            if link["kind"] == 1:  # 1 represents URI links
                link_url = link["uri"]
                links.append(link_url)

        return text, links


class JsonOperations:
    def write_json(self, json_path):
        file_path = json_path
        try:
            with open(file_path, "w") as file:
                json.dump(data, file)
        except Exception as e:
            print(e)

    def retrieve_json(self):
        try:
            file_path = self.json_path + "completed.json"
            with open(file_path, "r") as file:
                json_string = file.read()
            data = json.loads(json_string)
            return data
        except:
            return []

    def delete_json(self):
        file_path = self.json_path + "completed.json"
        if os.path.exists(self.json_path):
            os.remove(file_path)
