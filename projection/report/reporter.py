from calculations.basic_utils import *
from report.CLIReporter import CLIReporter
from report.HumanJSONReporter import HumanJSONReporter
from report.JSONReporter import JSONReporter


class Reporter:
    def __init__(self, cli) -> None:
        self.cli = cli
        self.cliReporter = CLIReporter()
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
        group_by_age_report = self.group_by_age(insured)

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
            group_by_age_report
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
            population
        )

        if self.cli:
            self.cliReporter.add_report(report_as_json)

    AGE_BINS = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70]
    AGE_LABELS = ["20_24", "25_29", "30_34", "35_39", "40_44", "45_49",
                  "50_54", "55_59", "60_64", "65_69"]

    def group_by_age(self, insured):
        # pd.cut once, then groupby — replaces 10 sequential .loc setitem
        # passes through the DataFrame. ~8× faster on these table sizes.
        buckets = pd.cut(insured["age"], bins=self.AGE_BINS,
                         labels=self.AGE_LABELS, right=False)
        return insured.groupby(buckets, observed=True)["number"].sum()