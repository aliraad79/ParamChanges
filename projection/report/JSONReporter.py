from calculations.basic_utils import rial_to_hemat


class JSONReporter:
    def __init__(self) -> None:
        self.memory = []

    def add_report(
        self,
        retired_obligation,
        azkaroftadeh_obligation,
        bazmandeh_obligation,
        retired_population,
        azkaroftadeh_population,
        bazmandeh_population,
        people_income,
        sandogh_income,
        bimehPardaz_population,
        sandogh_inbalance,
        year,
        deads_number,
        new_added_population,
        population
    ):
        report = {
            "year": year,
            "bazmandeh_payment_obligation": rial_to_hemat(bazmandeh_obligation),
            "bazneshasteh_payment_obligation": rial_to_hemat(retired_obligation),
            "azkaroftadeh_payment_obligation": rial_to_hemat(azkaroftadeh_obligation),
            "bazneshasteh_alive_population": int(retired_population),
            "azkaroftadeh_alive_population": int(azkaroftadeh_population),
            "bazmandeh_alive_population": int(bazmandeh_population),
            "sum_payment_obligation": rial_to_hemat(
                bazmandeh_obligation + retired_obligation + azkaroftadeh_obligation
            ),
            "sum_alive_population": int(
                retired_population + azkaroftadeh_population + bazmandeh_population
            ),
            "deads_number": int(deads_number),
            "new_population": int(new_added_population),
            "bimehpardaz_income": rial_to_hemat(people_income),
            "bimehpardaz_sandogh_income": rial_to_hemat(sandogh_income),
            "bimehpardaz_alive_population": int(bimehPardaz_population),
            "inbalance": rial_to_hemat(sandogh_inbalance),
            "all_population" : int(population)
        }
        self.memory.append(report)

        return report
