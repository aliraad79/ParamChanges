from consts import MIN_MONTHLY_INCOME_1396_RIAL
from helper import rial_to_hemat
import pandas as pd


def calc_monthly_unemployment_wage():
    return round(MIN_MONTHLY_INCOME_1396_RIAL * 0.55, 3)


def direct_unemployment():
    unemp = pd.Series(
        {
            "1396": rial_to_hemat(40_329_138 * 1000_000),
            "1395": rial_to_hemat(33_244_992 * 1000_000),
            "1394": rial_to_hemat(25_641_847 * 1000_000),
            "1393": rial_to_hemat(20_002_089 * 1000_000),
            "1392": rial_to_hemat(17_597_887 * 1000_000),
        },
    )  # All in Hemat
    print("Cost for unemployment Insurance (Hemat)=>")
    print(unemp)
    unemp.to_csv("./csv/unemployment_direct.csv")
    print("-" * 50)


direct_unemployment()
