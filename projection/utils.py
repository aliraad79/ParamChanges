import numpy as np
import pandas as pd

ONE_HEMAT = 1_000_000_000_000


def add_death_rate(df, death_percents):
    conditions = [
        (50 > df["age"]) & (df["age"] >= 40),
        (60 > df["age"]) & (df["age"] >= 50),
        (70 > df["age"]) & (df["age"] >= 60),
        (80 > df["age"]) & (df["age"] >= 70),
        (90 > df["age"]) & (df["age"] >= 80),
        (df["age"] >= 90),
    ]

    df["death_percentage"] = np.select(conditions, death_percents)
    return df


def get_df_salary_sum(df):
    return (df["average_salary"] * df["number"]).sum()


def rial_to_hemat(number):
    number = int(number) / 10

    return round(number / ONE_HEMAT, 3)


def convert_income_to_sandogh_income(number, RATE):
    return number * RATE


def format_three_digit(number):
    number = str(int(number))

    result = ""
    for i, value in enumerate(number[::-1]):
        if i % 3 == 0 and i != 0:
            result += "_"
        result += value
    return result[::-1]


def add_inflation_to_salaries(df: pd.DataFrame, rate: int):
    df["average_salary"] = df["average_salary"] * (1 + rate)
    return df


def calculate_deaths(df: pd.DataFrame):
    df["number"] = (df["number"] * (1 - df["death_percentage"])).astype(int)
    return df


def add_to_ages(df):
    df["age"] += 1
    return df

def add_to_record_age(df):
    df["insurance_record"] += 1
    return df


def calculate_retirments(
    bimehPardaz: pd.DataFrame, past_bazneshasteha: pd.DataFrame, formula
):
    current_bazneshasteha = formula(bimehPardaz)
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


def calculate_new_people(bimehPardaz: pd.DataFrame, rate):
    row = pd.DataFrame(
        {
            "age": [bimehPardaz.iloc[0]["age"]],
            "average_salary": [bimehPardaz.iloc[0]["average_salary"]],
            "number": [bimehPardaz["number"].sum() * rate],
            "insurance_record": [0],
        }
    )
    return pd.concat([row, bimehPardaz], ignore_index=True)
