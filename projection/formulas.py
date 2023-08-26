def basic_bazneshastegi_rule(df, RETIREMENTMENT_AGE):
    return df[df["insurance_record"] >= RETIREMENTMENT_AGE]
