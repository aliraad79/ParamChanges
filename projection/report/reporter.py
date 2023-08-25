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

    def generate_report(self, retired, azkaroftadeh, bazmandeh, bimehPardaz, year, INSURANCE_FEE_FROM_SALARY):
        # Salary infos
        payment_obligation = (
            get_df_salary_sum(retired)
            + get_df_salary_sum(azkaroftadeh)
            + get_df_salary_sum(bazmandeh)
        )
        people_income = get_df_salary_sum(bimehPardaz)
        sandogh_income = convert_income_to_sandogh_income(people_income, INSURANCE_FEE_FROM_SALARY)

        sandogh_inbalance = sandogh_income - payment_obligation
        # Populations
        bimehPardaz_population = bimehPardaz["number"].sum()
        obligated_population = (
            retired["number"].sum()
            + azkaroftadeh["number"].sum()
            + bazmandeh["number"].sum()
        )

        if self.cli:
            self.cliReporter.add_report(
                payment_obligation,
                obligated_population,
                people_income,
                sandogh_income,
                bimehPardaz_population,
                sandogh_inbalance,
                year,
            )
        if self.csv:
            self.csvReporter.add_report(
                payment_obligation,
                obligated_population,
                sandogh_income,
                bimehPardaz_population,
                sandogh_inbalance,
                year,
            )
        if self.db:
            self.dbReporter.add_report(
                payment_obligation,
                obligated_population,
                sandogh_income,
                bimehPardaz_population,
                sandogh_inbalance,
                year,
            )
