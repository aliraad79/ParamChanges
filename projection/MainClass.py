import pandas as pd
from utils import *
from formulas import basic_bazneshastegi_rule
from report.reporter import Reporter

# =======================================
# Assumtions:
#       1. No new bimeh pardaz
#       2. Just retired people dies
#       3. Inflation rate is static through years
#       4. Bamandeha and Azkaroftadeha is constant
# =======================================


class MainClass:
    # Paramethers
    INFLATION_RATE = 0.23
    INSURANCE_FEE_FROM_SALARY = 0.75
    SIMULATION_YEARS = 15
    ADDED_PEAOPLE_RATE = 0.01
    #             40-50  50-60 60-70 70-80 80-90 90-
    DEATH_RATES = [0.01, 0.01, 0.01, 0.02, 0.03, 0.5]

    def __init__(self) -> None:
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

    def run(self):
        for i in range(self.SIMULATION_YEARS):
            self.reporter.generate_report(
                self.retired, self.azkaroftadeh, self.bazmandeh, self.bimehPardaz, self.year, self.INSURANCE_FEE_FROM_SALARY
            )
            # Inflation
            self.retired = add_inflation_to_salaries(self.retired, self.INFLATION_RATE)
            self.azkaroftadeh = add_inflation_to_salaries(self.azkaroftadeh, self.INFLATION_RATE)
            self.bazmandeh = add_inflation_to_salaries(self.bazmandeh, self.INFLATION_RATE)
            self.bimehPardaz = add_inflation_to_salaries(self.bimehPardaz, self.INFLATION_RATE)

            # Kills
            self.retired = add_death_rate(self.retired, self.DEATH_RATES)
            self.retired = calculate_deaths(self.retired)

            # Bazneshastegi
            self.retired = calculate_retirments(self.bimehPardaz, self.retired, basic_bazneshastegi_rule)

            # New bimeh pardaz
            self.bimehPardaz = calculate_new_people(self.bimehPardaz, self.ADDED_PEAOPLE_RATE)

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
    
    def report(self):
        print(self.reporter.jsonReporter.memory)