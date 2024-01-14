import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback, dcc, html

from src.db.code_explanation import (
    sql_filter_claims_like_U, sql_filter_claims_over_300k,
    sql_filter_claims_over_300k_in_mexico, sql_filter_marine_and_2021_policies,
    sql_filter_marine_policies, sql_filter_policies_in_2021_2022,
    sql_filter_premium_between_50k_100k, sqlmodel_filter_claims_like_U,
    sqlmodel_filter_claims_over_300k,
    sqlmodel_filter_claims_over_300k_in_mexico,
    sqlmodel_filter_marine_and_2021_policies, sqlmodel_filter_marine_policies,
    sqlmodel_filter_policies_in_2021_2022,
    sqlmodel_filter_premium_between_50k_100k)
from src.db.db import (filter_claims_like_U, filter_claims_over_300k,
                       filter_claims_over_300k_in_mexico,
                       filter_marine_and_2021_policies, filter_marine_policies,
                       filter_policies_in_2021_2022,
                       filter_premium_between_50k_100k, select_claims,
                       select_policies, sqlmodel_to_df)
from src.reusable.components import create_grid, id_factory
from src.reusable.layouts import (code_exlanation, col_order_claims,
                                  col_order_policies, further_reading_layout,
                                  raw_data_layout, selection_output_layout)

policy_filters = [
    "Filter class_id = Marine",
    "Filter class_id = Marine and year = 2021",
    "Filter Year in 2021 and 2022",
    "Filter premium between £50k and £100k",
]
claim_filters = [
    "Filter claim_gbp > £300k",
    "Filter claim_gbp > £300k and country = Mexico",
    "Filter country like 'U%'",
]

further_reading_descriptions = [
    "Filter data with SQL",
    "Filter data with SQLModel",
    "Expression comparisons SQLModel",
    "Multiple Where SQLModel",
]
further_reading_urls = [
    "https://sqlmodel.tiangolo.com/tutorial/where/#filter-data-with-sql",
    "https://sqlmodel.tiangolo.com/tutorial/where/#filter-rows-using-where-with-sqlmodel",
    "https://sqlmodel.tiangolo.com/tutorial/where/#other-comparisons",
    "https://sqlmodel.tiangolo.com/tutorial/where/#multiple-where",
]

dash.register_page(__name__, path="/filtering_data", name="Filtering Data", order=3)

_id = id_factory("filtering_data")

output_layout = selection_output_layout(id_func=_id)

raw_data_component = raw_data_layout(id_func=_id)
further_reading_component = further_reading_layout(
    descriptions=further_reading_descriptions, urls=further_reading_urls
)

layout = [
    dcc.Store(id=_id("filter-ids")),
    dcc.Store(id=_id("code-explanation-items")),
    html.H1("Filtering Data"),
    html.H2("Data:"),
    raw_data_component,
    html.H2("Filter Options:"),
    html.P("Select the data table and choose from the filters below"),
    dbc.Row(
        [
            dcc.Dropdown(
                options=policy_filters,
                value=policy_filters[0],
                multi=False,
                id=_id("selection-dropdown"),
            ),
        ],
        style={"margin-bottom": "1rem"},
    ),
    html.H2("Filter Output:"),
    output_layout,
    html.H2("Code:"),
    dbc.Row(id=_id("code-explanation")),
    html.H2("Further Reading:"),
    further_reading_component,
]


@callback(
    Output(component_id=_id("data-card-content"), component_property="children"),
    Input(component_id=_id("raw-data-tabs"), component_property="active_tab"),
    Input(component_id=_id("selection-dropdown"), component_property="value"),
    Input(component_id=_id("filter-ids"), component_property="data"),
)
def raw_data_tables(data_tab, dropdown_selection, filter_ids):
    if "policy" in data_tab:
        data = select_policies()
        cols = col_order_policies
        number_cols = ["premium_gbp"]
        conditional_filter = " || ".join(
            [f"params.data.policy_id == '{x}'" for x in filter_ids]
        )
    else:
        data = select_claims()
        cols = col_order_claims
        number_cols = ["claim_gbp"]
        conditional_filter = " || ".join(
            [f"params.data.claim_id == '{x}'" for x in filter_ids]
        )

    tab_df = sqlmodel_to_df(data)
    tab_df = tab_df.loc[:, cols]

    getRowStyle = {
        "styleConditions": [
            {
                "condition": conditional_filter,
                "style": {"backgroundColor": "#F8C2A9", "color": "white"},
            }
        ]
    }

    grid = create_grid(
        _id=_id("data-grid"),
        df=tab_df,
        number_cols=number_cols,
        getRowStyle=getRowStyle,
    )

    return grid


@callback(
    Output(component_id=_id("selection-output-content"), component_property="children"),
    Output(component_id=_id("filter-ids"), component_property="data"),
    Input(component_id=_id("selection-dropdown"), component_property="value"),
    Input(component_id=_id("raw-data-tabs"), component_property="active_tab"),
)
def filter_data_tables(dropdown_selection, data_tab):
    if "policy" in data_tab:
        cols = col_order_policies
        number_cols = ["premium_gbp"]
        if dropdown_selection == policy_filters[0]:
            data = filter_marine_policies()
        elif dropdown_selection == policy_filters[1]:
            data = filter_marine_and_2021_policies()
        elif dropdown_selection == policy_filters[2]:
            data = filter_policies_in_2021_2022()
        else:
            data = filter_premium_between_50k_100k()
    else:
        cols = col_order_claims
        number_cols = ["claim_gbp"]
        if dropdown_selection == claim_filters[0]:
            data = filter_claims_over_300k()
        elif dropdown_selection == claim_filters[1]:
            data = filter_claims_over_300k_in_mexico()
        else:
            data = filter_claims_like_U()

    filter_df = sqlmodel_to_df(data)
    filter_df = filter_df.loc[:, cols]

    filter_ids = filter_df.iloc[:, 0].to_list()

    grid = create_grid(_id=_id("output-grid"), df=filter_df, number_cols=number_cols)

    return grid, filter_ids


@callback(
    Output(component_id=_id("selection-dropdown"), component_property="options"),
    Output(component_id=_id("selection-dropdown"), component_property="value"),
    Input(component_id=_id("raw-data-tabs"), component_property="active_tab"),
    prevent_initial_call=True,
)
def update_dropdown_options(data_tab):
    if "policy" in data_tab:
        return policy_filters, policy_filters[0]
    else:
        return claim_filters, claim_filters[0]


@callback(
    Output(component_id=_id("code-explanation"), component_property="children"),
    Input(component_id=_id("raw-data-tabs"), component_property="active_tab"),
    Input(component_id=_id("selection-dropdown"), component_property="value"),
)
def code_explanation(data_tab, dropdown_selection):
    if "policy" in data_tab:
        if dropdown_selection == policy_filters[0]:
            code_explanation_component = code_exlanation(
                _id,
                sqlmodel_markdown=sqlmodel_filter_marine_policies,
                sql_markdown=sql_filter_marine_policies,
            )
        elif dropdown_selection == policy_filters[1]:
            code_explanation_component = code_exlanation(
                _id,
                sqlmodel_markdown=sqlmodel_filter_marine_and_2021_policies,
                sql_markdown=sql_filter_marine_and_2021_policies,
            )
        elif dropdown_selection == policy_filters[2]:
            code_explanation_component = code_exlanation(
                _id,
                sqlmodel_markdown=sqlmodel_filter_policies_in_2021_2022,
                sql_markdown=sql_filter_policies_in_2021_2022,
            )
        else:
            code_explanation_component = code_exlanation(
                _id,
                sqlmodel_markdown=sqlmodel_filter_premium_between_50k_100k,
                sql_markdown=sql_filter_premium_between_50k_100k,
            )

    else:
        if dropdown_selection == claim_filters[0]:
            code_explanation_component = code_exlanation(
                _id,
                sqlmodel_markdown=sqlmodel_filter_claims_over_300k,
                sql_markdown=sql_filter_claims_over_300k,
            )
        elif dropdown_selection == claim_filters[1]:
            code_explanation_component = code_exlanation(
                _id,
                sqlmodel_markdown=sqlmodel_filter_claims_over_300k_in_mexico,
                sql_markdown=sql_filter_claims_over_300k_in_mexico,
            )
        else:
            code_explanation_component = code_exlanation(
                _id,
                sqlmodel_markdown=sqlmodel_filter_claims_like_U,
                sql_markdown=sql_filter_claims_like_U,
            )

    return code_explanation_component


@callback(
    Output(component_id=_id("code-explanation-items"), component_property="data"),
    Input(component_id=_id("accordion"), component_property="active_item"),
    prevent_initial_call=True,
)
def save_active_items(active_items):
    return active_items


@callback(
    Output(component_id=_id("accordion"), component_property="active_item"),
    Input(component_id=_id("raw-data-tabs"), component_property="active_tab"),
    Input(component_id=_id("selection-dropdown"), component_property="value"),
    State(component_id=_id("code-explanation-items"), component_property="data"),
    prevent_initial_call=True,
)
def return_active_items(active_tab, dropdown_selection, accordion_items):
    return accordion_items
