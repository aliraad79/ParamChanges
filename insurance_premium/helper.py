from consts import (ONE_HEMAT, average_income_1400,
                    number_of_bimey_shodegan_1400)


def format_three_digit(number):
    number = str(int(number))

    result = ""
    for i, value in enumerate(number[::-1]):
        if i % 3 == 0 and i != 0:
            result += "_"
        result += value
    return result[::-1]


def rial_to_hemat(number):
    number = int(number)

    return round(number / ONE_HEMAT, 3)


def rial_to_hundred_toman(number):
    return round(number / 10000)


def calc_govern_share(wage, govern_percentage=0.03):
    return wage * govern_percentage


def print_govern_total(govern_percentage):
    print(
        "Government 3% Insurance premium in 1400:",
        format_three_digit(
            calc_govern_share(average_income_1400, govern_percentage)
            * number_of_bimey_shodegan_1400
        ),
        "Rial",
        "|",
        rial_to_hemat(
            calc_govern_share(average_income_1400, govern_percentage)
            * number_of_bimey_shodegan_1400
        ),
        "Hemat",
    )


def get_percentage(num1, num2) -> float:
    return round(num1 / num2, 3) * 100
