from calculations.basic_utils import rial_to_yearly_hemat


class HumanJSONReporter:
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
        population,
    ):
        report = {
            "year": year,
            "survivor": {
                "survivor_payment_obligation": rial_to_yearly_hemat(
                    survivor_obligation
                ),
                "survivor_alive_population": int(survivor_population),
            },
            "azkaroftadeh": {
                "azkaroftadeh_payment_obligation": rial_to_yearly_hemat(
                    azkaroftadeh_obligation
                ),
                "azkaroftadeh_alive_population": int(azkaroftadeh_population),
            },
            "bazneshasteh": {
                "bazneshasteh_payment_obligation": rial_to_yearly_hemat(
                    retired_obligation
                ),
                "bazneshasteh_alive_population": int(retired_population),
            },
            "sum_mostamary_begir": {
                "sum_payment_obligation": rial_to_yearly_hemat(
                    survivor_obligation + retired_obligation + azkaroftadeh_obligation
                ),
                "sum_alive_population": int(
                    retired_population + azkaroftadeh_population + survivor_population
                ),
            },
            "bimeh_pardaz": {
                "insured_income": rial_to_yearly_hemat(people_income),
                "insured_sandogh_income": rial_to_yearly_hemat(sandogh_income),
                "insured_alive_population": int(insured_population),
            },
            "sandogh": {
                "inbalance": rial_to_yearly_hemat(sandogh_inbalance),
            },
            "deads_number": int(deads_number),
            "new_population": int(new_added_population),
            "all_population": int(population),
        }
        self.memory.append(report)

        return report
