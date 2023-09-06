import numpy as np
import pandas as pd
from .formulas import basic_bazneshastegi_rule

ONE_HUNDERD = 1_000


def add_death_rate(df, death_percents):
    conditions = [
        (50 > df["age"]) & (df["age"] >= 40),
        (60 > df["age"]) & (df["age"] >= 50),
        (70 > df["age"]) & (df["age"] >= 60),
        (80 > df["age"]) & (df["age"] >= 70),
        (90 > df["age"]) & (df["age"] >= 80),
        (100 > df["age"]) & (df["age"] >= 90),
        (df["age"] >= 100),
    ]

    df["death_percentage"] = np.select(conditions, death_percents)
    return df


def calculate_retirments(
    bimehPardaz: pd.DataFrame, past_bazneshasteha: pd.DataFrame, RETIREMENTMENT_AGE
):
    current_bazneshasteha = basic_bazneshastegi_rule(bimehPardaz, RETIREMENTMENT_AGE)
    bimehPardaz.drop(current_bazneshasteha.index, inplace=True)

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
    population_projection_in_milion: pd.DataFrame, bimehPardaz: pd.DataFrame, rate, year
):
    population_diffrence = population_projection_in_milion.loc[
        population_projection_in_milion["year"] == year
    ].get("population")

    if population_diffrence.isnull().values.any():
        population_diffrence = 0
    else:
        population_diffrence = population_diffrence.item()

    row = pd.DataFrame(
        {
            "age": [bimehPardaz.iloc[0]["age"]],
            "average_salary": [bimehPardaz.iloc[0]["average_salary"]],
            "number": [population_diffrence * rate * ONE_HUNDERD],
            "insurance_record": [0],
        }
    )
    return pd.concat([row, bimehPardaz], ignore_index=True)


def add_to_bazmandeh(bazmandeh: pd.DataFrame, deads_number: int, rate):
    row = pd.DataFrame(
        {
            "age": [bazmandeh.iloc[0]["age"]],
            "average_salary": [bazmandeh.iloc[0]["average_salary"]],
            "number": [deads_number * rate],
            "insurance_record": [0],
        }
    )
    return pd.concat([row, bazmandeh], ignore_index=True)


def remove_bazmandeh_from_payrool(df: pd.DataFrame, final_year_of_payrool):
    return df.loc[df["insurance_record"] <= final_year_of_payrool]
