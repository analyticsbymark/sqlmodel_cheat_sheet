sqlmodel_create_policies = """
                            ```python
                            class Policies(SQLModel, table=True):
                                policy_id: str = Field(primary_key=True)
                                class_id: str
                                uw_year: int
                                premium_gbp: int
                            ```
                            """

sql_create_policies = """
                        ```sql
                        CREATE TABLE policies (
                            policy_id VARCHAR NOT NULL, 
                            class_id VARCHAR NOT NULL, 
                            uw_year INTEGER NOT NULL, 
                            premium_gbp INTEGER NOT NULL, 
                            PRIMARY KEY (policy_id)
                        )
                        ```
                        """

sqlmodel_create_claims = """
                            ```python
                            class Claims(SQLModel, table=True):
                                claim_id: str = Field(primary_key=True)
                                country: str
                                claim_gbp: int

                                policy_id: str = Field(foreign_key='policies.policy_id')
                            """

sql_create_claims = """
                    ```sql
                    CREATE TABLE claims (
                        claim_id VARCHAR NOT NULL, 
                        country VARCHAR NOT NULL, 
                        claim_gbp INTEGER NOT NULL, 
                        policy_id VARCHAR NOT NULL, 
                        PRIMARY KEY (claim_id), 
                        FOREIGN KEY(policy_id) REFERENCES policies (policy_id)
                    )
                    ```
                """

sqlmodel_select_policies = """
                    ```python
                    select(Policies)
                    """

sql_select_policies = """
                    ```sql
                    SELECT policy_id, class_id, uw_year, premium_gbp 
                    FROM policies
                    """


sql_select_claims = """
                    ```sql
                    SELECT claim_id, country, claim_gbp, policy_id 
                    FROM claims
                    """

sqlmodel_select_claims = """
                    ```python
                    select(Claims)
                    """

sqlmodel_select_policies_order_by = """
                    ```python
                    select(Policies).order_by(Policies.premium_gbp.desc())
                    """

sql_select_policies_order_by = """
                    ```sql
                    SELECT policy_id, class_id, uw_year, premium_gbp 
                    FROM policies
                    ORDER BY premium_gbp DESC
                    """


sqlmodel_select_claims_order_by = """
                    ```python
                    select(Claims).order_by(Claims.claim_gbp.desc())
                    """

sql_select_claims_order_by = """
                    ```sql
                    SELECT claim_id, country, claim_gbp, policy_id 
                    FROM claims
                    ORDER BY gbp DESC
                    """

sqlmodel_select_policy_id = """
                    ```python
                    select(Policies.policy_id)
                    """

sql_select_policy_id = """
                    ```sql
                    SELECT policy_id 
                    FROM policies
                    """

sqlmodel_select_policy_id_premium = """
                    ```python
                    select(Policies.policy_id, Policies.premium_gbp)
                    """

sql_select_policy_id_premium = """
                    ```sql
                    SELECT policy_id, premium_gbp 
                    FROM policies
                    """

sqlmodel_select_claims_id = """
                    ```python
                    select(Claims.claim_id)
                    """

sql_select_claims_id = """
                    ```sql
                    SELECT claim_id
                    FROM claims
                    """

sqlmodel_select_claims_id_claim_gbp = """
                    ```python
                    select(Claims.claim_id, Claims.claim_gbp)
                    """


sql_select_claims_id_claim_gbp = """
                    ```sql
                    SELECT claim_id, claim_gbp
                    FROM claims
                    """


sqlmodel_filter_marine_policies = """
                    ```python
                    select(Policies).where(Policies.class_id == 'Marine')
                    """

sql_filter_marine_policies = """
                    ```sql
                    SELECT policy_id, class_id, uw_year, premium_gbp 
                    FROM policies 
                    WHERE class_id = 'Marine'
                    """

sqlmodel_filter_claims_over_300k = """
                    ```python
                    select(Claims).where(Claims.claim_gbp > 300000)
                    """

sql_filter_claims_over_300k = """
                    ```sql
                    SELECT claim_id, country, claim_gbp, policy_id 
                    FROM claims 
                    WHERE claim_gbp > 300000
                    """

sqlmodel_filter_marine_and_2021_policies = """
                    ```python
                    select(Policies).where(Policies.class_id == 'Marine').where(Policies.uw_year == 2021)
                    """

sql_filter_marine_and_2021_policies = """
                    ```sql
                    SELECT policy_id, class_id, uw_year, premium_gbp 
                    FROM policies 
                    WHERE class_id = 'Marine' AND uw_year = 2021
                    """

sqlmodel_filter_claims_over_300k_in_mexico = """
                    ```python
                    select(Claims).where(Claims.claim_gbp > 300000).where(Claims.country == 'Mexico')
                    """

sql_filter_claims_over_300k_in_mexico = """
                    ```sql
                    SELECT claim_id, country, claim_gbp, policy_id 
                    FROM claims 
                    WHERE claim_gbp > 300000 AND country = 'Mexico'
                    """

sqlmodel_filter_policies_in_2021_2022 = """
                    ```python
                    select(Policies).where(Policies.uw_year.in_([2021, 2022]))
                    """

sql_filter_policies_in_2021_2022 = """
                    ```sql
                    SELECT policy_id, class_id, uw_year, premium_gbp 
                    FROM policies 
                    WHERE uw_year IN (2021, 2022)
                    """

sqlmodel_filter_premium_between_50k_100k = """
                    ```python
                    select(Policies).where(Policies.premium_gbp.between(50000, 100000))
                    """

sql_filter_premium_between_50k_100k = """
                    ```sql
                    SELECT policy_id, class_id, uw_year, premium_gbp 
                    FROM policies 
                    WHERE premium_gbp BETWEEN 50000 AND 100000
                    """

sqlmodel_filter_claims_like_U = """
                    ```python
                    select(Claims).where(Claims.country.like('U%'))
                    """


sql_filter_claims_like_U = """
                    ```sql
                    SELECT claim_id, country, claim_gbp, policy_id 
                    FROM claims 
                    WHERE country LIKE 'U%'
                    """

sqlmodel_join_inner = """
                    ```python
                    select(Policies, Claims).join(Claims)
                    """


sql_join_inner = """
                    ```sql
                    SELECT policy_id, class_id, uw_year, premium_gbp, claim_id, country, claim_gbp 
                    FROM policies 
                    JOIN claims ON policies.policy_id = claims.policy_id
                    """

sqlmodel_join_outer = """
                    ```python
                    select(Policies, Claims).join(Claims, isouter=True)
                    """


sql_join_outer = """
                    ```sql
                    SELECT policy_id, class_id, uw_year, premium_gbp, claim_id, country, claim_gbp 
                    FROM policies 
                    LEFT OUTER JOIN claims ON policies.policy_id = claims.policy_id
                    """

sqlmodel_group_sum_premium = """
                    ```python
                    select(Policies.class_id, func.sum(Policies.premium_gbp).label("sum_premium"))
                    .group_by(Policies.class_id)
                    """

sql_group_sum_premium = """
                ```sql
                SELECT policies.class_id, sum(policies.premium_gbp) AS sum_premium 
                FROM policies 
                GROUP BY policies.class_id
                """

sqlmodel_group_avg_max_min = """
                    ```python
                    select(Policies.class_id,
                        Policies.uw_year,
                        func.sum(Policies.premium_gbp).label("sum_premium"),
                        func.count(Policies.policy_id).label("policy_count"),
                        func.avg(Policies.premium_gbp).label("avg_premium"),
                        func.max(Policies.premium_gbp).label("max_premium"),
                        func.min(Policies.premium_gbp).label("min_premium"))
                    .group_by(Policies.class_id, Policies.uw_year)
                    """

sql_group_avg_max_min = """
                ```sql
                SELECT policies.class_id, 
                    policies.uw_year, 
                    sum(policies.premium_gbp) AS sum_premium, 
                    count(policies.policy_id) AS policy_count, 
                    avg(policies.premium_gbp) AS avg_premium, 
                    max(policies.premium_gbp) AS max_premium, 
                    min(policies.premium_gbp) AS min_premium 
                FROM policies 
                GROUP BY policies.class_id, policies.uw_year
                """

sqlmodel_group_join = """
                    ```python
                       select(Policies.class_id,
                           Policies.uw_year,
                           func.sum(Policies.premium_gbp).label("sum_premium"),
                           func.sum(Claims.claim_gbp).label("sum_claims"),
                           func.count(Policies.policy_id).label("policy_count"),
                           func.count(Claims.claim_id).label("count_claims"))
                       .join(Claims, isouter=True)
                       .group_by(Policies.class_id, Policies.uw_year)
                    """

sql_group_join = """
                ```sql
                SELECT policies.class_id, 
                    policies.uw_year, sum(policies.premium_gbp) AS sum_premium, 
                    sum(claims.claim_gbp) AS sum_claims, 
                    count(policies.policy_id) AS policy_count, 
                    count(claims.claim_id) AS count_claims 
                FROM policies 
                LEFT OUTER JOIN claims ON policies.policy_id = claims.policy_id 
                GROUP BY policies.class_id, policies.uw_year
                """
