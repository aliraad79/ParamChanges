import csv
from datetime import datetime


class CSVReporter:
    def __init__(self) -> None:
        self.csv_path = "./generated_csvs/report_" + datetime.now().strftime(
            "%Y_%m_%d_%H:%M:%S"
        )

    def add_report(
        self,
        report_as_json
    ):
        bazneshaste_row = {
            "year": report_as_json['year'],
            "payment_obligation": report_as_json["bazneshasteh_payment_obligation"],
            "alive": report_as_json["bazneshasteh_population"],
        }
        bimeh_pardaz_row = {
            "year": report_as_json["year"],
            "sandogh_income": report_as_json["sandogh_income"],
            "alive": report_as_json["insured_population"],
        }
        sandogh_inbalance_row = {
            "sandogh_inbalance":report_as_json["sandogh_inbalance"]
        }
        with open(self.csv_path + "_baznesh.csv", "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=bazneshaste_row.keys())
            writer.writerow(bazneshaste_row)
        with open(self.csv_path + "_insured.csv", "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=bimeh_pardaz_row.keys())
            writer.writerow(bimeh_pardaz_row)
        with open(self.csv_path + "_inbalance.csv", "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=sandogh_inbalance_row.keys())
            writer.writerow(sandogh_inbalance_row)
