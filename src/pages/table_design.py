import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback, dcc, html

from src.db.code_explanation import (sql_create_claims, sql_create_policies,
                                     sqlmodel_create_claims,
                                     sqlmodel_create_policies)
from src.db.db import select_claims, select_policies, sqlmodel_to_df
from src.reusable.components import create_grid, id_factory
from src.reusable.layouts import (code_exlanation, col_order_claims,
                                  col_order_policies, further_reading_layout,
                                  raw_data_layout)

further_reading_descriptions = ["Create Table with SQL", "Create Table with SQLModel"]
further_reading_urls = [
    "https://sqlmodel.tiangolo.com/tutorial/create-db-and-table-with-db-browser",
    "https://sqlmodel.tiangolo.com/tutorial/create-db-and-table",
]

dash.register_page(__name__, path="/table-design", name="Table Design", order=1)

_id = id_factory("table-design")

raw_data_component = raw_data_layout(id_func=_id)
further_reading_component = further_reading_layout(
    descriptions=further_reading_descriptions, urls=further_reading_urls
)

layout = [
    dcc.Location(id=_id("url")),
    dcc.Store(id=_id("code-explanation-items")),
    html.H1("Table Design"),
    html.H2("Data:"),
    raw_data_component,
    html.H2("Code:"),
    dbc.Row(id=_id("code-explanation")),
    html.H2("Further Reading:"),
    further_reading_component,
]


@callback(
    Output(component_id=_id("data-card-content"), component_property="children"),
    Input(component_id=_id("raw-data-tabs"), component_property="active_tab"),
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

    grid = create_grid(_id=_id("data-grid"), df=tab_df, number_cols=number_cols)

    return grid


@callback(
    Output(component_id=_id("code-explanation"), component_property="children"),
    Input(component_id=_id("raw-data-tabs"), component_property="active_tab"),
)
def code_explanation(data_tab):
    if "policy" in data_tab:
        code_explanation_component = code_exlanation(
            _id,
            sqlmodel_markdown=sqlmodel_create_policies,
            sql_markdown=sql_create_policies,
        )

    else:
        code_explanation_component = code_exlanation(
            _id,
            sqlmodel_markdown=sqlmodel_create_claims,
            sql_markdown=sql_create_claims,
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
    State(component_id=_id("code-explanation-items"), component_property="data"),
    prevent_initial_call=True,
)
def return_active_items(active_tab, accordion_items):
    return accordion_items
