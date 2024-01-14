import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, State, callback, dcc, html

from src.db.code_explanation import (sql_select_claims, sql_select_claims_id,
                                     sql_select_claims_id_claim_gbp,
                                     sql_select_claims_order_by,
                                     sql_select_policies,
                                     sql_select_policies_order_by,
                                     sql_select_policy_id,
                                     sql_select_policy_id_premium,
                                     sqlmodel_select_claims,
                                     sqlmodel_select_claims_id,
                                     sqlmodel_select_claims_id_claim_gbp,
                                     sqlmodel_select_claims_order_by,
                                     sqlmodel_select_policies,
                                     sqlmodel_select_policies_order_by,
                                     sqlmodel_select_policy_id,
                                     sqlmodel_select_policy_id_premium)
from src.db.db import (select_claims, select_claims_id,
                       select_claims_id_claim_gbp, select_claims_order_by,
                       select_policies, select_policies_order_by,
                       select_policy_id, select_policy_id_premium,
                       sqlmodel_to_df)
from src.reusable.components import create_grid, id_factory
from src.reusable.layouts import (code_exlanation, col_order_claims,
                                  col_order_policies, further_reading_layout,
                                  raw_data_layout, selection_output_layout)

policy_filters = [
    "Select all policies",
    "Select policy_id",
    "Select policy_id and premium",
    "Order policies by premium",
]
claim_filters = [
    "Select all claims",
    "Select claim_id",
    "Select claim_id and amount",
    "Order claims by claim amount",
]

further_reading_descriptions = ["Read data with SQL", "Read data with SQLModel"]

further_reading_urls = [
    "https://sqlmodel.tiangolo.com/tutorial/select/#read-data-with-sql",
    "https://sqlmodel.tiangolo.com/tutorial/select/#read-data-with-sqlmodel",
]

dash.register_page(__name__, path="/selecting_data", name="Selecting Data", order=2)

_id = id_factory("selecting-data")

output_layout = selection_output_layout(id_func=_id)

raw_data_component = raw_data_layout(id_func=_id)
further_reading_component = further_reading_layout(
    descriptions=further_reading_descriptions, urls=further_reading_urls
)

layout = [
    dcc.Store(id=_id("code-explanation-items")),
    html.H1("Selecting Data"),
    html.H2("Data:"),
    raw_data_component,
    html.H2("Selection Options:"),
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
    html.H2("Selection Output:"),
    output_layout,
    html.H2("Code:"),
    dbc.Row(id=_id("code-explanation")),
    html.H2("Further Reading:"),
    further_reading_component,
]


@callback(
    Output(component_id=_id("data-card-content"), component_property="children"),
    Input(component_id=_id("raw-data-tabs"), component_property="active_tab")
)
def raw_data_tables(data_tab):
    if "policy" in data_tab:
        data = select_policies()
        cols = col_order_policies
        number_cols = ["premium_gbp"]
    else:
        data = select_claims()
        cols = col_order_claims
        number_cols = ["claim_gbp"]

    tab_df = sqlmodel_to_df(data)
    tab_df = tab_df.loc[:, cols]

    grid = create_grid(
        _id=_id("data-grid"), df=tab_df, number_cols=number_cols, getRowStyle={}
    )
    return grid


@callback(
    Output(component_id=_id("selection-output-content"), component_property="children"),
    Input(component_id=_id("selection-dropdown"), component_property="value"),
    Input(component_id=_id("raw-data-tabs"), component_property="active_tab"),
)
def select_data_tables(dropdown_selection, data_tab):
    if "policy" in data_tab:
        cols = col_order_policies
        number_cols = ["premium_gbp"]
    else:
        cols = col_order_claims
        number_cols = ["claim_gbp"]

    if dropdown_selection == policy_filters[0]:
        data = select_policies()
    elif dropdown_selection == policy_filters[1]:
        data = select_policy_id()
        filter_df = pd.DataFrame({"policy_id": data})
        return create_grid(_id=_id("output-grid"), df=filter_df, number_cols=[])
    elif dropdown_selection == policy_filters[2]:
        data = select_policy_id_premium()
    elif dropdown_selection == policy_filters[3]:
        data = select_policies_order_by()
    elif dropdown_selection == claim_filters[0]:
        data = select_claims()
    elif dropdown_selection == claim_filters[1]:
        data = select_claims_id()
        filter_df = pd.DataFrame({"claim_id": data})
        return create_grid(_id=_id("output-grid"), df=filter_df, number_cols=[])
    elif dropdown_selection == claim_filters[2]:
        data = select_claims_id_claim_gbp()
    else:
        data = select_claims_order_by()

    if dropdown_selection in [
        policy_filters[0],
        policy_filters[-1],
        claim_filters[0],
        claim_filters[-1],
    ]:
        filter_df = sqlmodel_to_df(data)
        filter_df = filter_df.loc[:, cols]

        grid = create_grid(
            _id=_id("output-grid"), df=filter_df, number_cols=number_cols
        )

        return grid
    else:
        filter_df = pd.DataFrame(data)
        grid = create_grid(
            _id=_id("output-grid"), df=filter_df, number_cols=number_cols
        )
        return grid


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
                sqlmodel_markdown=sqlmodel_select_policies,
                sql_markdown=sql_select_policies,
            )
        elif dropdown_selection == policy_filters[1]:
            code_explanation_component = code_exlanation(
                _id,
                sqlmodel_markdown=sqlmodel_select_policy_id,
                sql_markdown=sql_select_policy_id,
            )
        elif dropdown_selection == policy_filters[2]:
            code_explanation_component = code_exlanation(
                _id,
                sqlmodel_markdown=sqlmodel_select_policy_id_premium,
                sql_markdown=sql_select_policy_id_premium,
            )
        else:
            code_explanation_component = code_exlanation(
                _id,
                sqlmodel_markdown=sqlmodel_select_policies_order_by,
                sql_markdown=sql_select_policies_order_by,
            )

    else:
        if dropdown_selection == claim_filters[0]:
            code_explanation_component = code_exlanation(
                _id,
                sqlmodel_markdown=sqlmodel_select_claims,
                sql_markdown=sql_select_claims,
            )
        elif dropdown_selection == claim_filters[1]:
            code_explanation_component = code_exlanation(
                _id,
                sqlmodel_markdown=sqlmodel_select_claims_id,
                sql_markdown=sql_select_claims_id,
            )
        elif dropdown_selection == claim_filters[2]:
            code_explanation_component = code_exlanation(
                _id,
                sqlmodel_markdown=sqlmodel_select_claims_id_claim_gbp,
                sql_markdown=sql_select_claims_id_claim_gbp,
            )
        else:
            code_explanation_component = code_exlanation(
                _id,
                sqlmodel_markdown=sqlmodel_select_claims_order_by,
                sql_markdown=sql_select_claims_order_by,
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
