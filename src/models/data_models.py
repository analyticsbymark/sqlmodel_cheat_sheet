from sqlmodel import Field, SQLModel


class Policies(SQLModel, table=True):
    policy_id: str = Field(primary_key=True)
    class_id: str
    uw_year: int
    premium_gbp: int


class Claims(SQLModel, table=True):
    claim_id: str = Field(primary_key=True)
    country: str
    claim_gbp: int

    policy_id: str = Field(foreign_key="policies.policy_id")
