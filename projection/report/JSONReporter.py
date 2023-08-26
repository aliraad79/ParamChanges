from calculations.utils import rial_to_hemat


class JSONReporter:
    def __init__(self) -> None:
        self.memory = {}

    def add_report(
        self,
        bazneshasteh_payment_obligation,
        bazneshasteh_population,
        people_income,
        sandogh_income,
        bimehPardaz_population,
        sandogh_inbalance,
        year,
    ):
        self.memory[year] = {
            "bazneshasteh": {
                "payment_obligation": rial_to_hemat(bazneshasteh_payment_obligation),
                "alive_population": bazneshasteh_population,
            },
            "bimehpardaz": {
                "people_income": rial_to_hemat(people_income),
                "sandogh_income": rial_to_hemat(sandogh_income),
                "alive_population": bimehPardaz_population,
            },
            "inbalance": {"value": sandogh_inbalance},
        }
