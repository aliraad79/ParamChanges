from calculations.utils import rial_to_hemat


class JSONReporter:
    def __init__(self) -> None:
        self.memory = []

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
        self.memory.append(
            {
                "year": year,
                "bazneshasteh_payment_obligation": rial_to_hemat(
                    bazneshasteh_payment_obligation
                ),
                "bazneshasteh_alive_population": int(bazneshasteh_population),
                "bimehpardaz_income": rial_to_hemat(people_income),
                "bimehpardaz_sandogh_income": rial_to_hemat(sandogh_income),
                "bimehpardaz_alive_population": int(bimehPardaz_population),
                "inbalance": rial_to_hemat(sandogh_inbalance),
            }
        )
