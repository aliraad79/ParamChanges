import pandas as pd
from .utils import *
from report.reporter import Reporter

# =======================================
# Assumtions:
#       1. No new bimeh pardaz
#       2. Just retired people dies
#       3. Inflation rate is static through years
#       4. Bamandeha and Azkaroftadeha is constant
# =======================================

default_config = {
    "INFLATION_RATE": 0.23,
    "INSURANCE_FEE_FROM_SALARY": 0.30,
    "SIMULATION_YEARS": 15,
    "ADDED_PEAOPLE_RATE": 0.01,
    "RETIREMENTMENT_AGE": 30,
}


class SimulationClass:
    #             40-50  50-60 60-70 70-80 80-90 90-
    DEATH_RATES = [0.01, 0.01, 0.01, 0.02, 0.03, 0.5]

    def __init__(self, config=default_config) -> None:
        # Bazneshasteha
        self.retired = pd.read_excel("./csv/bazneshaste_bimepardaz_just_all.xlsx")
        # Azkaroftadeh
        self.azkaroftadeh = pd.read_excel("./csv/azkaroftadeh.xlsx")
        # Bazmandeh
        self.bazmandeh = pd.read_excel("./csv/bazmandeh.xlsx")
        # Bimeh pardazha
        self.bimehPardaz = pd.read_excel("./csv/sabeghe_bimepardaz_just_all.xlsx")

        self.reporter = Reporter(json=True)
        self.year = 1400

        self.inflation_rate = config["INFLATION_RATE"]
        self.insurance_fee_from_salary = config["INSURANCE_FEE_FROM_SALARY"]
        self.simulation_years = config["SIMULATION_YEARS"]
        self.added_people_rate = config["ADDED_PEAOPLE_RATE"]
        self.retirement_age = config["RETIREMENTMENT_AGE"]

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
            self.retired = calculate_deaths(self.retired)

            # Bazneshastegi
            self.retired = calculate_retirments(
                self.bimehPardaz, self.retired, self.retirement_age
            )

            # New bimeh pardaz
            self.bimehPardaz = calculate_new_people(
                self.bimehPardaz, self.added_people_rate
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

    def json_report(self):
        return self.reporter.jsonReporter.memory