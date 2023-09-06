from calculations.basic_utils import *
from report.CSVReporter import CSVReporter
from report.CLIReporter import CLIReporter
from report.DBReporter import DBReporter
from report.HumanJSONReporter import HumanJSONReporter
from report.JSONReporter import JSONReporter


class Reporter:
    def __init__(self, cli, csv, db) -> None:
        self.cli = cli
        self.csv = csv
        self.db = db
        # self.csvReporter = CSVReporter()
        self.cliReporter = CLIReporter()
        # self.dbReporter = DBReporter()
        self.jsonReporter = JSONReporter()
        self.humanJsonReporter = HumanJSONReporter()

        self.reports = []

    def generate_report(
        self,
        retired: pd.DataFrame,
        azkaroftadeh: pd.DataFrame,
        survivor: pd.DataFrame,
        insured: pd.DataFrame,
        year,
        INSURANCE_FEE_FROM_SALARY,
        deads_number,
        new_added_population,
        population_df: pd.DataFrame,
    ):
        # Salary infos
        retired_obligation = get_df_salary_sum(retired)
        azkaroftadeh_obligation = get_df_salary_sum(azkaroftadeh)
        survivor_obligation = get_df_salary_sum(survivor)

        # Sandogh Info
        people_income = get_df_salary_sum(insured)
        sandogh_income = convert_income_to_sandogh_income(
            people_income, INSURANCE_FEE_FROM_SALARY
        )
        sandogh_inbalance = sandogh_income - (
            retired_obligation + azkaroftadeh_obligation + survivor_obligation
        )

        # Populations
        insured_population = insured["number"].sum()
        retired_population = retired["number"].sum()
        azkaroftadeh_population = azkaroftadeh["number"].sum()
        survivor_population = survivor["number"].sum()
        population = population_df["number"].sum()

        ## Population grouping
        insured.loc[insured["age"].between(20, 24), "age_group"] = "20_24"
        insured.loc[insured["age"].between(25, 29), "age_group"] = "25_29"
        insured.loc[insured["age"].between(30, 34), "age_group"] = "30_34"
        insured.loc[insured["age"].between(35, 39), "age_group"] = "35_39"
        insured.loc[insured["age"].between(40, 44), "age_group"] = "40_44"
        insured.loc[insured["age"].between(45, 49), "age_group"] = "45_49"
        insured.loc[insured["age"].between(50, 54), "age_group"] = "50_54"
        insured.loc[insured["age"].between(55, 59), "age_group"] = "55_59"
        insured.loc[insured["age"].between(60, 64), "age_group"] = "60_64"
        insured.loc[insured["age"].between(65, 69), "age_group"] = "65_69"
        group_by_report = insured.groupby(["age_group"])["number"].sum()

        report_as_json = self.jsonReporter.add_report(
            retired_obligation,
            azkaroftadeh_obligation,
            survivor_obligation,
            retired_population,
            azkaroftadeh_population,
            survivor_population,
            people_income,
            sandogh_income,
            insured_population,
            sandogh_inbalance,
            year,
            deads_number,
            new_added_population,
            population,
            group_by_report
        )

        self.humanJsonReporter.add_report(
            retired_obligation,
            azkaroftadeh_obligation,
            survivor_obligation,
            retired_population,
            azkaroftadeh_population,
            survivor_population,
            people_income,
            sandogh_income,
            insured_population,
            sandogh_inbalance,
            year,
            deads_number,
            new_added_population,
            population,
            group_by_report
        )

        if self.cli:
            self.cliReporter.add_report(report_as_json)
        # if self.csv:
        #     self.csvReporter.add_report(report_as_json)
        # if self.db:
        #     self.dbReporter.add_report(report_as_json)
