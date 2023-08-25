from utils import *
from report.CSVReporter import CSVReporter
from report.CLIReporter import CLIReporter
from report.DBReporter import DBReporter

class Reporter:
    def __init__(self, cli=False, csv=False, db=False) -> None:
        self.cli = cli
        self.csv = csv
        self.db = db
        self.csvReporter = CSVReporter()
        self.cliReporter = CLIReporter()
        self.dbReporter = DBReporter()

        self.reports = []

    def generate_report(self, bazneshasteh, bimehPardaz, year):
        # Salary infos
        bazneshasteh_payment_obligation = get_df_salary_sum(bazneshasteh)
        people_income = get_df_salary_sum(bimehPardaz)
        sandogh_income = convert_income_to_sandogh_income(people_income)
        # Populations
        bimehPardaz_population = bimehPardaz["number"].sum()
        bazneshasteh_population = bazneshasteh["number"].sum()

        if self.cli:
            self.cliReporter.add_report(
                bazneshasteh_payment_obligation,
                bazneshasteh_population,
                people_income,
                sandogh_income,
                bimehPardaz_population,
                year,
            )
        if self.csv:
            self.csvReporter.add_report(
                bazneshasteh_payment_obligation,
                bazneshasteh_population,
                sandogh_income,
                bimehPardaz_population,
                year,
            )
        if self.db:
            self.dbReporter.add_report(
                bazneshasteh_payment_obligation,
                bazneshasteh_population,
                sandogh_income,
                bimehPardaz_population,
                year,
            )
