from pathlib import Path

import pandas as pd
from .utils import *
from .basic_utils import *
from .config import default_config
from report.reporter import Reporter

CSV_DIR = Path(__file__).resolve().parent.parent / "csv"

pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 1000)

# =======================================
# Assumtions:
#       2. Just retired and insured people dies
#       3. Inflation rate is static through years
#       4. Azkaroftadeha is constant
# =======================================


class SimulationClass:
    def __init__(self, config=default_config, cli=False) -> None:
        self.load_csvs()
        self.load_config(config)

        self.reporter = Reporter(cli=cli)
        self.deads_number = 0
        self.new_added_population = 0
        self.year = 1400

    def load_config(self, config):
        self.inflation_rate = config["INFLATION_RATE"]
        self.insurance_fee_from_salary = config["INSURANCE_FEE_FROM_SALARY"]
        self.simulation_years = config["SIMULATION_YEARS"]
        self.added_people_rate = config["EMPLOYED_AND_INSURED_RATE"]
        self.retirement_age = config["RETIREMENT_AGE"]
        self.basic_retirement_strategy = config["BASIC_RETIREMENT_STRATEGY"]
        self.proposed_survivor_strategy = config["PROPOSED_SURVIVOR_STRATEGY"]
        self.death_to_survivor_rate = config["DEATH_TO_SURVIVOR_RATE"]
        self.survivor_final_year_of_payroll = config["SURVIVOR_FINAL_YEAR_OF_PAYROLL"]
        self.new_people_age = 30

    def load_csvs(self):
        # Bazneshasteha
        self.retired = pd.read_excel(CSV_DIR / "retired.xlsx")
        # Azkaroftadeh
        self.azkaroftadeh = pd.read_excel(CSV_DIR / "azkaroftadeh.xlsx")
        # SURVIVOR
        self.survivor = pd.read_excel(CSV_DIR / "bazmandeh.xlsx")
        # Bimeh pardazha
        self.insured = pd.read_excel(CSV_DIR / "insured.xlsx")
        # Projection for population
        self.population_projection = pd.read_excel(CSV_DIR / "population_projection.xlsx")
        self.population_projection["population"] = self.population_projection[
            "population"
        ].diff()
        # Current population
        self.population = pd.read_excel(CSV_DIR / "population.xlsx")

    def run(self):
        for i in range(self.simulation_years):
            self.reporter.generate_report(
                self.retired,
                self.azkaroftadeh,
                self.survivor,
                self.insured,
                self.year,
                self.insurance_fee_from_salary,
                self.deads_number,
                self.new_added_population,
                self.population,
            )
            # Inflation
            self.retired = add_inflation_to_salaries(self.retired, self.inflation_rate)
            self.azkaroftadeh = add_inflation_to_salaries(
                self.azkaroftadeh, self.inflation_rate
            )
            self.survivor = add_inflation_to_salaries(
                self.survivor, self.inflation_rate
            )
            self.insured = add_inflation_to_salaries(self.insured, self.inflation_rate)

            # Kills
            self.retired = add_death_rate(self.retired)
            self.retired, self.deads_number = calculate_deaths(self.retired)

            self.insured = add_death_rate(self.insured)
            self.insured, _ = calculate_deaths(self.insured)

            self.population = add_death_rate(self.population)
            self.population, _ = calculate_deaths(self.population)
            # new survivor
            self.survivor = add_to_survivor(
                self.survivor, self.deads_number, self.death_to_survivor_rate
            )

            # Proposed survivor strategy
            if self.proposed_survivor_strategy:
                self.survivor = remove_survivor_from_payroll(
                    self.survivor, self.survivor_final_year_of_payroll
                )

            # Bazneshastegi
            self.insured, self.retired = calculate_retirments(
                self.insured, self.retired, self.retirement_age
            )

            # New bimeh pardaz
            self.insured, self.population = calculate_new_people(
                self.population_projection,
                self.insured,
                self.population,
                self.added_people_rate,
                self.year,
                int(self.deads_number),
                self.new_people_age,
            )
            self.new_added_population = self.population.iloc[0].get("number")

            # Aging
            self.retired = add_to_ages(self.retired)
            self.retired = add_to_record_age(self.retired)
            self.azkaroftadeh = add_to_ages(self.azkaroftadeh)
            self.azkaroftadeh = add_to_record_age(self.azkaroftadeh)
            self.survivor = add_to_ages(self.survivor)
            self.survivor = add_to_record_age(self.survivor)

            self.insured = add_to_ages(self.insured)
            self.insured = add_to_record_age(self.insured)

            self.population = add_to_ages(self.population)

            # NEXT year
            self.year += 1

            if not self.basic_retirement_strategy:
                if self.retirement_age < 40:
                    self.retirement_age += 0.5

    def json_report(self):
        return self.reporter.jsonReporter.memory

    def human_json_report(self):
        return self.reporter.humanJsonReporter.memory

    def population_json(self):
        return self.reporter.jsonReporter.population_memory
