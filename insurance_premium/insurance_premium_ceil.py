import pandas as pd
from enums import MaxWageUpgrade
from tabulate import tabulate

from helper import (
    calc_govern_share,
    format_three_digit,
    get_percentage,
    rial_to_hundred_toman,
)


class insurancePremiumCeil:
    def __init__(
        self,
        ceil: MaxWageUpgrade,
        data: pd.DataFrame,
        govern_percentage: float,
        save_as_csv: bool = True,
    ) -> None:
        self.ceil = ceil
        self.data = data
        self.govern_percentage = govern_percentage
        self.save_as_csv = save_as_csv

        self.total_number_of_people = data.loc["total_number"].sum()

    def main(self):

        if self.ceil == MaxWageUpgrade.One_x:
            unsupported = self.data.drop("min_wage", axis=1)
            self.data = self.data[["min_wage"]]
            max_supported_salary = self.data["min_wage"]["avg_wage"]

        elif self.ceil == MaxWageUpgrade.Two_x:
            unsupported = self.data.drop(["min_wage", "1_2x"], axis=1)
            self.data = self.data[["min_wage", "1_2x"]]
            max_supported_salary = self.data["min_wage"]["avg_wage"] * 2

        elif self.ceil == MaxWageUpgrade.Three_x:
            unsupported = self.data.drop(columns=["min_wage", "1_2x", "2_3x"])
            self.data = self.data[["min_wage", "1_2x", "2_3x"]]
            max_supported_salary = self.data["min_wage"]["avg_wage"] * 3

        max_govern_share_pay = rial_to_hundred_toman(
            calc_govern_share(max_supported_salary, self.govern_percentage)
        )

        affected_people = unsupported.loc["total_number"].sum()
        self.percentage_of_affected_people = get_percentage(
            affected_people, self.total_number_of_people
        )

        unsupported.loc["Should pay on new ceil (hundred toman)"] = round(
            unsupported.loc["original_govern_share (hundred toman)"]
            - max_govern_share_pay
        )
        unsupported.loc["Should pay on new ceil (Percentage of wage)"] = get_percentage(
            unsupported.loc["Should pay on new ceil (hundred toman)"],
            unsupported.loc["avg_wage"],
        )

        unsupported.loc["Government pay per group"] = (
            unsupported.loc["Should pay on new ceil (hundred toman)"]
            * unsupported.loc["total_number"]
        )

        total_govern_pay = unsupported.loc["Government pay per group"].sum()

        self.print_log(max_govern_share_pay, unsupported, total_govern_pay)

    def print_log(self, max_govern_share_pay, unsupported_people, total_govern_pay):
        print(
            f"\n\nThe {self.ceil.name} ceil will affect {self.percentage_of_affected_people}% of current people"
        )
        print(
            f"For those people govern only pay {format_three_digit(max_govern_share_pay)} Hundred Toman per person"
        )

        print(tabulate(unsupported_people, headers="keys", tablefmt="psql"))

        print(
            f"Government save on new ceil {format_three_digit(total_govern_pay)} Hundreds Toman"
        )

        if self.save_as_csv:
            unsupported_people.to_csv(f"./csv/unsupported_people_{self.ceil.name}.csv")
