import pandas as pd
from consts import GOVERN_PERCENTAGE
from enums import MaxWageUpgrade
from helper import calc_govern_share, print_govern_total, rial_to_hundred_toman
from insurance_premium_ceil import insurancePremiumCeil
from plot import plot_insurance_premium_diff

print_govern_total(GOVERN_PERCENTAGE)

table_4 = pd.DataFrame(
    {
        "min_wage": [2006314, 26_554_950],
        "1_2x": [9000649, 37606547],
        "2_3x": [2073051, 65309427],
        "3_4x": [1084292, 91277697],
        "4_5x": [466518, 117642390],
        "5_6x": [223549, 144758064],
        "6_7x": [275624, 177765024],
    },
    index=["total_number", "avg_wage"],
)

table_4.loc["original_govern_share (hundred toman)"] = rial_to_hundred_toman(
    calc_govern_share(table_4.loc["avg_wage"], GOVERN_PERCENTAGE)
)

plot_insurance_premium_diff(table_4)

insurancePremiumCeil(
    MaxWageUpgrade.One_x, table_4, GOVERN_PERCENTAGE, save_as_csv=True
).main()
insurancePremiumCeil(
    MaxWageUpgrade.Two_x, table_4, GOVERN_PERCENTAGE, save_as_csv=True
).main()
insurancePremiumCeil(
    MaxWageUpgrade.Three_x, table_4, GOVERN_PERCENTAGE, save_as_csv=True
).main()
