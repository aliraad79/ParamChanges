import pandas as pd
from sqlalchemy import create_engine, DECIMAL


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
        sandogh_inbalance,
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
        sandogh_inbalance_df = pd.DataFrame({"inbalance": [sandogh_inbalance]})

        bazneshasteh_row.to_sql(
            "bazneshaste",
            self.engine,
            if_exists="append",
            dtype={"payment_obligation": DECIMAL()},
        )
        bimeh_pardaz_row.to_sql(
            "bimehpardaz",
            self.engine,
            if_exists="append",
            dtype={"sandogh_income": DECIMAL()},
        )
        sandogh_inbalance_df.to_sql("inbalance", self.engine, if_exists="append")
