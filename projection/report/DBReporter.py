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
        report_as_json
    ):
        bazneshasteh_row = pd.DataFrame(
            {
                "year": [report_as_json["year"]],
                "payment_obligation": [report_as_json["bazneshasteh_payment_obligation"]],
                "alive": [report_as_json["bazneshasteh_population"]],
            }
        )
        bimeh_pardaz_row = pd.DataFrame(
            {
                "year": [report_as_json["year"]],
                "sandogh_income": [report_as_json["sandogh_income"]],
                "alive": [report_as_json["insured_population"]],
            }
        )
        sandogh_inbalance_df = pd.DataFrame({"inbalance": [report_as_json["sandogh_inbalance"]]})

        bazneshasteh_row.to_sql(
            "bazneshaste",
            self.engine,
            if_exists="append",
            dtype={"payment_obligation": DECIMAL()},
        )
        bimeh_pardaz_row.to_sql(
            "insured",
            self.engine,
            if_exists="append",
            dtype={"sandogh_income": DECIMAL()},
        )
        sandogh_inbalance_df.to_sql("inbalance", self.engine, if_exists="append")
