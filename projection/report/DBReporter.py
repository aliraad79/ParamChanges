import pandas as pd
from sqlalchemy import create_engine


class DBReporter:
    def __init__(self) -> None:
        # Init engine
        self.engine = create_engine(
            "postgresql://postgres:postgres@localhost:5432/param_changes"
        )

    def add_report(
        self,
        bazneshasteh_payment_obligation,
        bazneshasteh_population,
        sandogh_income,
        bimehPardaz_population,
        year,
    ):
        bazneshasteh_row = pd.DataFrame(
            {
                "year": [year],
                "payment_obligation": [bazneshasteh_payment_obligation],
                "alive": [bazneshasteh_population],
            }
        )
        bimeh_pardaz_row = pd.DataFrame(
            {
                "year": [year],
                "sandogh_income": [sandogh_income],
                "alive": [bimehPardaz_population],
            }
        )

        a = bazneshasteh_row.to_sql("bazneshaste", self.engine, if_exists="append")
        b = bimeh_pardaz_row.to_sql("bimehpardaz", self.engine, if_exists="append")
