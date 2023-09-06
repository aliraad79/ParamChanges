from calculations.utils import *
from report.CSVReporter import CSVReporter
from report.CLIReporter import CLIReporter
from report.DBReporter import DBReporter
from report.JSONReporter import JSONReporter


class Reporter:
    def __init__(self, cli=False, csv=False, db=False) -> None:
        self.cli = cli
        self.csv = csv
        self.db = db
        self.csvReporter = CSVReporter()
        self.cliReporter = CLIReporter()
        self.dbReporter = DBReporter()
        self.jsonReporter = JSONReporter()

        self.reports = []

    def generate_report(
        self,
        retired,
        azkaroftadeh,
        bazmandeh,
        bimehPardaz,
        year,
        INSURANCE_FEE_FROM_SALARY,
    ):
        # Salary infos
        retired_obligation = get_df_salary_sum(retired)
        azkaroftadeh_obligation = get_df_salary_sum(azkaroftadeh)
        bazmandeh_obligation = get_df_salary_sum(bazmandeh)
        people_income = get_df_salary_sum(bimehPardaz)
        sandogh_income = convert_income_to_sandogh_income(
            people_income, INSURANCE_FEE_FROM_SALARY
        )

        sandogh_inbalance = sandogh_income - (
            retired_obligation + azkaroftadeh_obligation + bazmandeh_obligation
        )

        # Populations
        bimehPardaz_population = bimehPardaz["number"].sum()
        retired_population = retired["number"].sum()
        azkaroftadeh_population = azkaroftadeh["number"].sum()
        bazmandeh_population = bazmandeh["number"].sum()

        report_as_json = self.jsonReporter.add_report(
            retired_obligation,
            azkaroftadeh_obligation,
            bazmandeh_obligation,
            retired_population,
            azkaroftadeh_population,
            bazmandeh_population,
            people_income,
            sandogh_income,
            bimehPardaz_population,
            sandogh_inbalance,
            year,
        )

        if self.cli:
            self.cliReporter.add_report(report_as_json)
        if self.csv:
            self.csvReporter.add_report(report_as_json)
        if self.db:
            self.dbReporter.add_report(report_as_json)
