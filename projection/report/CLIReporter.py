from colorama import Fore, Style
from utils import rial_to_hemat, format_three_digit


class CLIReporter:
    def add_report(
        self,
        bazneshasteh_payment_obligation,
        bazneshasteh_population,
        people_income,
        sandogh_income,
        bimehPardaz_population,
        year,
    ):
        self.print_seprated_red_line()
        print(f"     YEAR : {year}")
        print(
            f"""Bazneshaste Report:
        Payment Obligation : {rial_to_hemat(bazneshasteh_payment_obligation)} Hemat
        Alive Population:    {format_three_digit(bazneshasteh_population)}"""
        )
        self.print_seprated_red_line()

        print(
            f"""Bimeh pardaz Report:
        People Income  : {rial_to_hemat(people_income)} Hemat
        Sandogh Income : {rial_to_hemat(sandogh_income)} Hemat
        Alive Population:    {format_three_digit(bimehPardaz_population)} """
        )
        self.print_seprated_red_line()

    def print_seprated_red_line():
        print(
            Fore.GREEN
            + "----------------------------------------------------------------"
        )
        print(Style.RESET_ALL + "", end="")
