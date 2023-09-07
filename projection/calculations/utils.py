import numpy as np
import pandas as pd
from .formulas import basic_bazneshastegi_rule

ONE_HUNDERD = 1_000


def add_death_rate(df, death_percents):
    conditions = [
        (0 == df["age"]),
        (4 > df["age"]) & (df["age"] >= 1),
        (9 > df["age"]) & (df["age"] >= 5),
        (14 > df["age"]) & (df["age"] >= 10),
        (19 > df["age"]) & (df["age"] >= 14),
        (24 > df["age"]) & (df["age"] >= 20),
        (29 > df["age"]) & (df["age"] >= 24),
        (34 > df["age"]) & (df["age"] >= 30),
        (39 > df["age"]) & (df["age"] >= 34),
        (44 > df["age"]) & (df["age"] >= 40),
        (49 > df["age"]) & (df["age"] >= 44),
        (54 > df["age"]) & (df["age"] >= 50),
        (59 > df["age"]) & (df["age"] >= 54),
        (64 > df["age"]) & (df["age"] >= 60),
        (69 > df["age"]) & (df["age"] >= 64),
        (74 > df["age"]) & (df["age"] >= 70),
        (79 > df["age"]) & (df["age"] >= 74),
        (99 > df["age"]) & (df["age"] >= 80),
        (119 > df["age"]) & (df["age"] >= 100),
        (140 > df["age"]) & (df["age"] >= 120),
        (df["age"] >= 140),
    ]

    df["death_percentage"] = np.select(conditions, death_percents)
    return df


def calculate_retirments(
    insured: pd.DataFrame, past_bazneshasteha: pd.DataFrame, RETIREMENTMENT_AGE
):
    current_bazneshasteha = basic_bazneshastegi_rule(insured, RETIREMENTMENT_AGE)
    insured.drop(current_bazneshasteha.index, inplace=True)

    merged = pd.merge(
        past_bazneshasteha,
        current_bazneshasteha[["age", "number"]],
        on="age",
        how="left",
    )
    merged["number"] = merged["number_x"].fillna(0) + merged["number_y"].fillna(0)
    merged = merged.drop(columns=["number_x", "number_y"])

    return merged


def calculate_new_people(
    population_projection_in_milion: pd.DataFrame,
    insured: pd.DataFrame,
    population_df: pd.DataFrame,
    rate,
    year,
    dead_people,
    new_people_age,
):
    population_diffrence = population_projection_in_milion.loc[
        population_projection_in_milion["year"] == year
    ].get("population")

    if population_diffrence.isnull().values.any():
        population_diffrence = 0
    else:
        population_diffrence = population_diffrence.item()

    new_population = (population_diffrence * ONE_HUNDERD) + dead_people

    population_df.loc[0, "number"] += new_population

    if population_df.loc[0, "age"] == 0:
        population_df.loc[0, "number"] += new_population
    else:
        new_borns = pd.DataFrame({"age": [0], "number": [new_population]})
        population_df = pd.concat([new_borns, population_df], ignore_index=True)

    added_population = (
        population_df.loc[population_df["age"] == new_people_age].get("number")
    ) * rate
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


def remove_survivor_from_payrool(df: pd.DataFrame, final_year_of_payrool):
    return df.loc[df["insurance_record"] <= final_year_of_payrool]
