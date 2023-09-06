from calculations.basic_utils import rial_to_hemat


class JSONReporter:
    def __init__(self) -> None:
        self.memory = []

    def add_report(
        self,
        retired_obligation,
        azkaroftadeh_obligation,
        survivor_obligation,
        retired_population,
        azkaroftadeh_population,
        survivor_population,
        people_income,
        sandogh_income,
        insured_population,
        sandogh_inbalance,
        year,
        deads_number,
        new_added_population,
        population
    ):
        report = {
            "year": year,
            "survivor_payment_obligation": rial_to_hemat(survivor_obligation),
            "bazneshasteh_payment_obligation": rial_to_hemat(retired_obligation),
            "azkaroftadeh_payment_obligation": rial_to_hemat(azkaroftadeh_obligation),
            "bazneshasteh_alive_population": int(retired_population),
            "azkaroftadeh_alive_population": int(azkaroftadeh_population),
            "survivor_alive_population": int(survivor_population),
            "sum_payment_obligation": rial_to_hemat(
                survivor_obligation + retired_obligation + azkaroftadeh_obligation
            ),
            "sum_alive_population": int(
                retired_population + azkaroftadeh_population + survivor_population
            ),
            "deads_number": int(deads_number),
            "new_population": int(new_added_population),
            "insured_income": rial_to_hemat(people_income),
            "insured_sandogh_income": rial_to_hemat(sandogh_income),
            "insured_alive_population": int(insured_population),
            "inbalance": rial_to_hemat(sandogh_inbalance),
            "all_population" : int(population)
        }
        self.memory.append(report)

        return report
