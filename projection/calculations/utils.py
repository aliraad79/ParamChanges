import numpy as np
import pandas as pd
from .formulas import basic_bazneshastegi_rule

ONE_HUNDERD = 1_000

# (lower_inclusive, upper_exclusive, annual_death_rate).
# Boundaries preserve the original logic in this module; some bands are
# off-by-one against the canonical 5-year groupings (e.g. 15-19 → 14-19),
# and ages 99 and 119 fall into no band (death_percentage defaults to 0).
# Fix bands and rerun the simulation if you intend to change behavior.
DEATH_BANDS = [
    (0, 1, 0.0198),
    (1, 4, 0.0007),
    (5, 9, 0.0004),
    (10, 14, 0.0003),
    (14, 19, 0.0007),
    (20, 24, 0.0009),
    (24, 29, 0.0009),
    (30, 34, 0.0010),
    (34, 39, 0.0014),
    (40, 44, 0.0021),
    (44, 49, 0.0038),
    (50, 54, 0.0064),
    (54, 59, 0.0111),
    (60, 64, 0.0181),
    (64, 69, 0.0297),
    (70, 74, 0.0488),
    (74, 79, 0.0790),
    (80, 99, 0.1590),
    (100, 119, 0.3000),
    (120, 140, 0.5000),
    (140, np.inf, 1.0000),
]


def add_death_rate(df: pd.DataFrame, bands=DEATH_BANDS) -> pd.DataFrame:
    df = df.copy()
    conditions = [(lo <= df["age"]) & (df["age"] < hi) for lo, hi, _ in bands]
    rates = [rate for _, _, rate in bands]
    df["death_percentage"] = np.select(conditions, rates, default=0.0)
    return df


def calculate_retirments(
    insured: pd.DataFrame, past_bazneshasteha: pd.DataFrame, retirement_age
):
    current_bazneshasteha = basic_bazneshastegi_rule(insured, retirement_age)
    new_insured = insured.drop(current_bazneshasteha.index)

    merged = pd.merge(
        past_bazneshasteha,
        current_bazneshasteha[["age", "number", "insurance_record", "average_salary"]],
        on="age",
        how="outer",
    )
    merged["number"] = merged["number_x"].fillna(0) + merged["number_y"].fillna(0)
    merged["insurance_record"] = merged["insurance_record_x"].fillna(0) + merged[
        "insurance_record_y"
    ].fillna(0)
    merged["average_salary"] = merged["average_salary_x"].fillna(0) + merged[
        "average_salary_y"
    ].fillna(0)

    merged = merged.drop(
        columns=[
            "number_x",
            "number_y",
            "average_salary_x",
            "average_salary_y",
            "insurance_record_x",
            "insurance_record_y",
        ]
    ).sort_values("age")
    return new_insured, merged


def calculate_new_people(
    population_projection_in_milion: pd.DataFrame,
    insured: pd.DataFrame,
    population_df: pd.DataFrame,
    rate,
    year,
    dead_people,
    new_people_age,
):
    population_df = population_df.copy()

    population_diffrence = population_projection_in_milion.loc[
        population_projection_in_milion["year"] == year
    ].get("population")

    if population_diffrence.isnull().values.any():
        population_diffrence = 0
    else:
        population_diffrence = population_diffrence.item()

    new_population = (population_diffrence * ONE_HUNDERD) + dead_people

    age0_mask = population_df["age"] == 0
    if age0_mask.any():
        population_df.loc[age0_mask, "number"] += new_population
    else:
        new_borns = pd.DataFrame({"age": [0], "number": [new_population]})
        population_df = pd.concat([new_borns, population_df], ignore_index=True)

    added_population = (
        population_df.loc[population_df["age"] == new_people_age, "number"].sum()
        * rate
    )
    row = pd.DataFrame(
        {
            "age": [new_people_age],
            "average_salary": [insured.iloc[0]["average_salary"]],
            "number": [int(added_population)],
            "insurance_record": [0],
        }
    )
    insured = pd.concat([row, insured], ignore_index=True)

    return insured, population_df


def add_to_survivor(survivor: pd.DataFrame, deads_number: int, rate):
    row = pd.DataFrame(
        {
            "age": [survivor.iloc[0]["age"]],
            "average_salary": [survivor.iloc[0]["average_salary"]],
            "number": [deads_number * rate],
            "insurance_record": [0],
        }
    )
    return pd.concat([row, survivor], ignore_index=True)


def remove_survivor_from_payroll(df: pd.DataFrame, final_year_of_payroll):
    return df.loc[df["insurance_record"] <= final_year_of_payroll]
