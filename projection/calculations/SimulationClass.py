import pandas as pd
from .utils import *
from .basic_utils import *
from .config import default_config
from report.reporter import Reporter

pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 1000)

# =======================================
# Assumtions:
#       1. No new bimeh pardaz
#       2. Just retired people dies
#       3. Inflation rate is static through years
#       4. Bamandeha and Azkaroftadeha is constant
#       5. People Die at age of 100
#       6. new people start at avarge of 30
# =======================================


class SimulationClass:
    DEATH_RATES = [
        0.001,  # 30-34
        0.001,  # 35-39
        0.002,  # 40-44
        0.003,  # 45-49
        0.006,  # 50-54
        0.011,  # 54-59
        0.018,  # 60-64
        0.029,  # 64-69
        0.048,  # 70-74
        0.079,  # 75-79
        0.15,  # 80-100
        0.5,  # 100-*
    ]

    def __init__(self, config=default_config, cli=False, csv=False, db=False) -> None:
        self.load_csvs()
        self.load_config(config)

        self.reporter = Reporter(cli=cli, csv=csv, db=db)
        self.deads_number = 0
        self.new_added_population = 0
        self.year = 1400

    def load_config(self, config):
        self.inflation_rate = config["INFLATION_RATE"]
        self.insurance_fee_from_salary = config["INSURANCE_FEE_FROM_SALARY"]
        self.simulation_years = config["SIMULATION_YEARS"]
        self.added_people_rate = config["ADDED_PEAOPLE_RATE"]
        self.retirement_age = config["RETIREMENTMENT_AGE"]
        self.basic_retirment_strategy = config["BASIC_RETIRMENT_STRATEGY"]
        self.proposed_bazmandeh_strategy = config["PROPOSED_BAZMANDEH_STRATEGY"]
        self.death_to_bazmandeh_rate = config["DEATH_TO_BAZMANDEH_RATE"]
        self.bazmandeh_final_year_of_payrool = config["BAZMANDEH_FINAL_YEAR_OF_PAYROOL"]
        self.new_people_age = 30

    def load_csvs(self):
        # Bazneshasteha
        self.retired = pd.read_excel("./csv/bazneshaste_bimepardaz_just_all.xlsx")
        # Azkaroftadeh
        self.azkaroftadeh = pd.read_excel("./csv/azkaroftadeh.xlsx")
        # Bazmandeh
        self.bazmandeh = pd.read_excel("./csv/bazmandeh.xlsx")
        # Bimeh pardazha
        self.bimehPardaz = pd.read_excel("./csv/sabeghe_bimepardaz_just_all.xlsx")
        # Projection for population
        self.population_projection = pd.read_excel("./csv/population_projection.xlsx")
        self.population_projection["population"] = self.population_projection[
            "population"
        ].diff()
        # Current population
        self.population = pd.read_excel("./csv/population.xlsx")

    def run(self):
        for i in range(self.simulation_years):
            self.reporter.generate_report(
                self.retired,
                self.azkaroftadeh,
                self.bazmandeh,
                self.bimehPardaz,
                self.year,
                self.insurance_fee_from_salary,
                self.deads_number,
                self.new_added_population,
                self.population,
            )
            print(self.population)
            # Inflation
            self.retired = add_inflation_to_salaries(self.retired, self.inflation_rate)
            self.azkaroftadeh = add_inflation_to_salaries(
                self.azkaroftadeh, self.inflation_rate
            )
            self.bazmandeh = add_inflation_to_salaries(
                self.bazmandeh, self.inflation_rate
            )
            self.bimehPardaz = add_inflation_to_salaries(
                self.bimehPardaz, self.inflation_rate
            )

            # Kills
            self.retired = add_death_rate(self.retired, self.DEATH_RATES)
            self.retired, self.deads_number = calculate_deaths(self.retired)

            self.population = add_death_rate(self.population, self.DEATH_RATES)
            self.population, self.deads_number = calculate_deaths(self.population)
            # new bazmandeh
            self.bazmandeh = add_to_bazmandeh(
                self.bazmandeh, self.deads_number, self.death_to_bazmandeh_rate
            )

            # Proposed bazmandeh strategy
            if self.proposed_bazmandeh_strategy:
                self.bazmandeh = remove_bazmandeh_from_payrool(
                    self.bazmandeh, self.bazmandeh_final_year_of_payrool
                )

            # Bazneshastegi
            self.retired = calculate_retirments(
                self.bimehPardaz, self.retired, self.retirement_age
            )

            # New bimeh pardaz
            self.bimehPardaz, self.population = calculate_new_people(
                self.population_projection,
                self.bimehPardaz,
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
            self.bazmandeh = add_to_ages(self.bazmandeh)
            self.bazmandeh = add_to_record_age(self.bazmandeh)

            self.bimehPardaz = add_to_ages(self.bimehPardaz)
            self.bimehPardaz = add_to_record_age(self.bimehPardaz)

            self.population = add_to_ages(self.population)

            # NEXT year
            self.year += 1

            if not self.basic_retirment_strategy:
                self.retirement_age += 0.5

    def json_report(self):
        return self.reporter.jsonReporter.memory

    def human_json_report(self):
        return self.reporter.humanJsonReporter.memory
