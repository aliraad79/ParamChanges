import pandas as pd
from utils import *
from formulas import basic_bazneshastegi_rule
from report.reporter import Reporter

# Bazneshasteha
retired = pd.read_excel("./csv/bazneshaste_bimepardaz_just_all.xlsx")
# Azkaroftadeh
azkaroftadeh = pd.read_excel("./csv/azkaroftadeh.xlsx")
# Bazmandeh
bazmandeh = pd.read_excel("./csv/bazmandeh.xlsx")
# Bimeh pardazha
bimehPardaz = pd.read_excel("./csv/sabeghe_bimepardaz_just_all.xlsx")

# =======================================
# Assumtions:
#       1. No new bimeh pardaz
#       2. Just retired people dies
#       3. Inflation rate is static through years
# =======================================

# Start Simulation
INFLATION_RATE = 0.0
INSURANCE_FEE_FROM_SALARY = 0.8
SIMULATION_YEARS = 20
#             40-50  50-60 60-70 70-80 80-90 90-
DEATH_RATES = [0.01, 0.01, 0.01, 0.02, 0.03, 0.5]

reporter = Reporter(cli=True, csv=True, db=True)

year = 1400
for i in range(SIMULATION_YEARS):
    reporter.generate_report(
        retired, azkaroftadeh, bazmandeh, bimehPardaz, year, INSURANCE_FEE_FROM_SALARY
    )
    # Inflation
    retired = add_inflation_to_salaries(retired, INFLATION_RATE)
    azkaroftadeh = add_inflation_to_salaries(azkaroftadeh, INFLATION_RATE)
    bazmandeh = add_inflation_to_salaries(bazmandeh, INFLATION_RATE)
    bimehPardaz = add_inflation_to_salaries(bimehPardaz, INFLATION_RATE)

    # Kills
    retired = add_death_rate(retired, DEATH_RATES)
    retired = calculate_deaths(retired)

    # Bazneshastegi
    retired = calculate_retirments(bimehPardaz, retired, basic_bazneshastegi_rule)

    # Aging
    retired = add_to_ages(retired)
    retired = add_to_record_age(retired)
    azkaroftadeh = add_to_ages(retired)
    azkaroftadeh = add_to_record_age(retired)
    bazmandeh = add_to_ages(bazmandeh)
    bazmandeh = add_to_record_age(bazmandeh)

    bimehPardaz = add_to_ages(bimehPardaz)
    bimehPardaz = add_to_record_age(bimehPardaz)

    # NEXT year
    year += 1
