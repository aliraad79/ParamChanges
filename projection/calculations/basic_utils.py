import pandas as pd

ONE_HEMAT = 1_000_000_000_000


def get_df_salary_sum(df):
    return (df["average_salary"] * df["number"]).sum()


def rial_to_hemat(number):
    number = int(number) / 10

    return round(number / ONE_HEMAT, 3)

def rial_to_yearly_hemat(number):
    number = int(number * 12) / 10

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
    deads_number = (df["number"] * df["death_percentage"]).sum()
    df["number"] = (df["number"] * (1 - df["death_percentage"])).astype(int)
    df.drop(df[df["number"] == 0].index, inplace=True)
    return df, deads_number


def add_to_ages(df):
    df["age"] += 1
    return df


def add_to_record_age(df):
    df["insurance_record"] += 1
    return df
