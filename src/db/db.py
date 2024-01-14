from typing import List

import numpy as np
import pandas as pd
from sqlmodel import Session, SQLModel, create_engine, select, func

from src.models.data_models import Claims, Policies

np.random.seed(41)
n_policies = 100
classes = ["Marine", "Property", "Aviation"]
uw_years = [2021, 2022, 2023]
policy_ids = [f"p_{i}" for i in range(1, n_policies + 1)]
class_ids = np.random.choice(classes, n_policies)

uw_year_ids = sorted(
    np.random.choice([2021, 2022, 2023], n_policies, p=(1 / 6, 2 / 6, 3 / 6))
)

policy_exposures = [x * 1000000 for x in np.random.randint(1, 10, n_policies)]
policy_premium = [x * 0.05 for x in policy_exposures]

policy_df = pd.DataFrame(
    {
        "policy_id": policy_ids,
        "class_id": class_ids,
        "uw_year": uw_year_ids,
        "premium_gbp": policy_premium,
    }
)

n_claims = 30
large_loss_amount = 300000
claim_countries = ["UK", "USA", "China", "Mexico", "France"]
claim_ids = [f"c_{i}" for i in range(1, n_claims + 1)]
claim_country_ids = np.random.choice(claim_countries, n_claims)

claim_policy_ids = [f"p_{x}" for x in np.random.randint(1, n_policies + 1, n_claims)]

claim_premiums = [
    policy_df.loc[policy_df["policy_id"] == x, "premium_gbp"].item()
    for x in claim_policy_ids
]
claim_amounts = [x * np.random.randint(1, 12) / 10 for x in claim_premiums]
large_loss_indicator = [1 if x >= large_loss_amount else 0 for x in claim_amounts]

claim_df = pd.DataFrame(
    {
        "claim_id": claim_ids,
        "country": claim_country_ids,
        "claim_gbp": claim_amounts,
        "policy_id": claim_policy_ids,
    }
)

def get_engine():
    return create_engine(
        "sqlite://", echo=True, connect_args={"check_same_thread": False}
)

def sqlmodel_to_df(objs: List[SQLModel]) -> pd.DataFrame:
    """Convert a SQLModel objects into a pandas DataFrame."""
    records = [i.dict() for i in objs]
    df = pd.DataFrame.from_records(records)
    return df


def create_db_and_tables(engine):
    SQLModel.metadata.create_all(engine)


def create_policy_data(session):
    policies = [Policies(**row) for row in policy_df.to_dict("records")]
    session.add_all(policies)
    session.commit()


def create_claims_data(session):
    claims = [Claims(**row) for row in claim_df.to_dict("records")]
    session.add_all(claims)
    session.commit()


def select_policies():
    engine = get_engine()
    with Session(engine) as session:
        create_db_and_tables(engine=engine)
        create_policy_data(session=session)
        policy_data = session.exec(select(Policies)).all()

    return policy_data


def select_policies_order_by():
    engine = get_engine()
    with Session(engine) as session:
        create_db_and_tables(engine=engine)
        create_policy_data(session=session)
        policy_data = session.exec(
            select(Policies).order_by(Policies.premium_gbp.desc())
        ).all()

    return policy_data


def select_policy_id():
    engine=get_engine()
    with Session(engine) as session:
        create_db_and_tables(engine=engine)
        create_policy_data(session=session)
        policy_data = session.exec(select(Policies.policy_id)).all()

        return policy_data


def select_policy_id_premium():
    engine = get_engine()
    with Session(engine) as session:
        create_db_and_tables(engine=engine)
        create_policy_data(session=session)
        policy_data = session.exec(
            select(Policies.policy_id, Policies.premium_gbp)
        ).all()

    return policy_data


def select_claims():
    engine = get_engine()
    with Session(engine) as session:
        create_db_and_tables(engine=engine)
        create_claims_data(session=session)
        claims_data = session.exec(select(Claims)).all()

    return claims_data


def select_claims_order_by():
    engine = get_engine()
    with Session(engine) as session:
        create_db_and_tables(engine=engine)
        create_claims_data(session=session)
        claims_data = session.exec(
            select(Claims).order_by(Claims.claim_gbp.desc())
        ).all()

    return claims_data


def select_claims_id():
    engine = get_engine()
    with Session(engine) as session:
        create_db_and_tables(engine=engine)
        create_claims_data(session=session)
        claims_data = session.exec(select(Claims.claim_id)).all()

    return claims_data


def select_claims_id_claim_gbp():
    engine = get_engine()
    with Session(engine) as session:
        create_db_and_tables(engine=engine)
        create_claims_data(session=session)
        claims_data = session.exec(select(Claims.claim_id, Claims.claim_gbp)).all()

    return claims_data


def filter_marine_policies():
    engine = get_engine()
    with Session(engine) as session:
        create_db_and_tables(engine=engine)
        create_policy_data(session=session)
        policy_data = session.exec(
            select(Policies).where(Policies.class_id == "Marine")
        ).all()

    return policy_data


def filter_claims_over_300k():
    engine = get_engine()
    with Session(engine) as session:
        create_db_and_tables(engine=engine)
        create_claims_data(session=session)
        claims_data = session.exec(
            select(Claims).where(Claims.claim_gbp > 300000)
        ).all()

    return claims_data


def filter_marine_and_2021_policies():
    engine = get_engine()
    with Session(engine) as session:
        create_db_and_tables(engine=engine)
        create_policy_data(session=session)
        policy_data = session.exec(
            select(Policies)
            .where(Policies.class_id == "Marine")
            .where(Policies.uw_year == 2021)
        ).all()

    return policy_data


def filter_claims_over_300k_in_mexico():
    engine = get_engine()
    with Session(engine) as session:
        create_db_and_tables(engine=engine)
        create_claims_data(session=session)
        claims_data = session.exec(
            select(Claims)
            .where(Claims.claim_gbp > 300000)
            .where(Claims.country == "Mexico")
        ).all()

    return claims_data


def filter_policies_in_2021_2022():
    engine = get_engine()
    with Session(engine) as session:
        create_db_and_tables(engine=engine)
        create_policy_data(session=session)
        policy_data = session.exec(
            select(Policies).where(Policies.uw_year.in_([2021, 2022]))
        ).all()

    return policy_data


def filter_premium_between_50k_100k():
    engine = get_engine()
    with Session(engine) as session:
        create_db_and_tables(engine=engine)
        create_policy_data(session=session)
        policy_data = session.exec(
            select(Policies).where(Policies.premium_gbp.between(50000, 100000))
        ).all()

    return policy_data


def filter_claims_like_U():
    engine = get_engine()
    with Session(engine) as session:
        create_db_and_tables(engine=engine)
        create_claims_data(session=session)
        claims_data = session.exec(
            select(Claims).where(Claims.country.like("U%"))
        ).all()

    return claims_data


def join_premium_inner_claims():
    engine = get_engine()
    with Session(engine) as session:
        create_db_and_tables(engine=engine)
        create_policy_data(session=session)
        create_claims_data(session=session)
        policy_data = session.exec(select(Policies, Claims).join(Claims)).all()

    return policy_data


def join_premium_leftouter_claims():
    engine = get_engine()
    with Session(engine) as session:
        create_db_and_tables(engine=engine)
        create_policy_data(session=session)
        create_claims_data(session=session)
        policy_data = session.exec(
            select(Policies, Claims).join(Claims, isouter=True)
        ).all()

    return policy_data

def group_premium_by_classid():
    engine = get_engine()
    with Session(engine) as session:
        create_db_and_tables(engine=engine)
        create_policy_data(session=session)
        policy_data = session.exec(
            select(Policies.class_id, func.sum(Policies.premium_gbp).label("sum_premium")).group_by(Policies.class_id)
        ).all()

    return policy_data

def group_premium_by_classid_uw_year():
    engine = get_engine()
    with Session(engine) as session:
        create_db_and_tables(engine=engine)
        create_policy_data(session=session)
        policy_data = session.exec(
            select(Policies.class_id,
                   Policies.uw_year,
                   func.sum(Policies.premium_gbp).label("sum_premium"),
                   func.count(Policies.policy_id).label("policy_count"),
                   func.avg(Policies.premium_gbp).label("avg_premium"),
                   func.max(Policies.premium_gbp).label("max_premium"),
                   func.min(Policies.premium_gbp).label("min_premium"))
            .group_by(Policies.class_id, Policies.uw_year)
        ).all()

    return policy_data

def join_group_premium_with_claims():
    engine = get_engine()
    with Session(engine) as session:
        create_db_and_tables(engine=engine)
        create_policy_data(session=session)
        create_claims_data(session=session)

        policy_data = session.exec(
            select(Policies.class_id,
                   Policies.uw_year,
                   func.sum(Policies.premium_gbp).label("sum_premium"),
                   func.sum(Claims.claim_gbp).label("sum_claims"),
                   func.count(Policies.policy_id).label("policy_count"),
                   func.count(Claims.claim_id).label("count_claims")).join(Claims, isouter=True).group_by(Policies.class_id, Policies.uw_year)
        ).all()

    return policy_data