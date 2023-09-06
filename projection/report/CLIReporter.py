from colorama import Fore, Style
from calculations.basic_utils import format_three_digit


class CLIReporter:
    def add_report(self, report_as_json):
        print(f"     YEAR : {report_as_json['year']}")
        print(
            f"""Bazneshaste Report:
        Payment Obligation : {report_as_json["bazneshasteh_payment_obligation"]} Hemat
        Alive Population:    {format_three_digit(report_as_json["bazneshasteh_alive_population"])}"""
        )
        print(
            f"""Azkaroftadeh Report:
        Payment Obligation : {report_as_json["azkaroftadeh_payment_obligation"]} Hemat
        Alive Population:    {format_three_digit(report_as_json["azkaroftadeh_alive_population"])}"""
        )
        print(
            f"""Bazmandeh Report:
        Payment Obligation : {report_as_json["bazmandeh_payment_obligation"]} Hemat
        Alive Population:    {format_three_digit(report_as_json["bazmandeh_alive_population"])}"""
        )
        print(
            f"""Sum Report:
        Payment Obligation : {report_as_json["sum_payment_obligation"]} Hemat
        Alive Population:    {format_three_digit(report_as_json["sum_alive_population"])}"""
        )

        self.print_seprated_red_line()

        print(
            f"""Bimeh pardaz Report:
        People Income  : {report_as_json["bimehpardaz_income"]} Hemat
        Sandogh Income : {report_as_json["bimehpardaz_sandogh_income"]} Hemat
        Alive Population:    {format_three_digit(report_as_json["bimehpardaz_alive_population"])} """
        )
        self.print_seprated_red_line()

        print(
            f"""Sandogh Inbalance:
        Value  : {report_as_json["inbalance"]} Hemat"""
        )
        self.print_seprated_red_line()

    def print_seprated_red_line(self):
        print(
            Fore.GREEN
            + "----------------------------------------------------------------"
        )
        print(Style.RESET_ALL + "", end="")
