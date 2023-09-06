import pandas as pd
from .utils import *
from .basic_utils import *
from .config import default_config
from report.reporter import Reporter

# =======================================
# Assumtions:
#       1. No new bimeh pardaz
#       2. Just retired people dies
#       3. Inflation rate is static through years
#       4. Bamandeha and Azkaroftadeha is constant
#       5. People Die at age of 100
# =======================================


class SimulationClass:
    #             30-34  35-39   40-44  45-49  50-54  54-59  60-64  64-69  70-74  75-79 80-*
    DEATH_RATES = [0.001, 0.001, 0.002, 0.003, 0.006, 0.011, 0.018, 0.029, 0.048, 0.79, 0.15]

    def __init__(self, config=default_config, cli=False, csv=False, db=False) -> None:
        self.load_csvs()
        self.load_config(config)

        self.reporter = Reporter(cli=cli, csv=csv, db=db)
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

    def run(self):
        for i in range(self.simulation_years):
            self.reporter.generate_report(
                self.retired,
                self.azkaroftadeh,
                self.bazmandeh,
                self.bimehPardaz,
                self.year,
                self.insurance_fee_from_salary,
            )
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
            self.retired, deads_number = calculate_deaths(self.retired)
            # new bazmandeh
            self.bazmandeh = add_to_bazmandeh(
                self.bazmandeh, deads_number, self.death_to_bazmandeh_rate
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
            self.bimehPardaz = calculate_new_people(
                self.population_projection,
                self.bimehPardaz,
                self.added_people_rate,
                self.year,
            )

            # Aging
            self.retired = add_to_ages(self.retired)
            self.retired = add_to_record_age(self.retired)
            self.azkaroftadeh = add_to_ages(self.retired)
            self.azkaroftadeh = add_to_record_age(self.retired)
            self.bazmandeh = add_to_ages(self.bazmandeh)
            self.bazmandeh = add_to_record_age(self.bazmandeh)

            self.bimehPardaz = add_to_ages(self.bimehPardaz)
            self.bimehPardaz = add_to_record_age(self.bimehPardaz)

            # NEXT year
            self.year += 1

            if not self.basic_retirment_strategy:
                self.retirement_age += 0.5

    def json_report(self):
        return self.reporter.jsonReporter.memory
