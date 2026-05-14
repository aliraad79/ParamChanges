from consts import ONE_HEMAT


def rial_to_hemat(number):
    number = int(number)

    return round(number / (ONE_HEMAT * 10), 3)
