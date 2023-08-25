import csv
from datetime import datetime


class CSVReporter:
    def __init__(self) -> None:
        self.csv_path = "./generated_csvs/report_" + datetime.now().strftime(
            "%Y_%m_%d_%H:%M"
        )

    def add_report(
        self,
        bazneshasteh_payment_obligation,
        bazneshasteh_population,
        sandogh_income,
        bimehPardaz_population,
        year,
    ):
        bazneshaste_row = {
            "year": year,
            "payment_obligation": bazneshasteh_payment_obligation,
            "alive": bazneshasteh_population,
        }
        bimeh_pardaz_row = {
            "year": year,
            "sandogh_income": sandogh_income,
            "alive": bimehPardaz_population,
        }
        with open(self.csv_path + "_baznesh.csv", "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=bazneshaste_row.keys())
            writer.writerow(bazneshaste_row)
        with open(self.csv_path + "_bimehpardaz.csv", "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=bimeh_pardaz_row.keys())
            writer.writerow(bimeh_pardaz_row)
