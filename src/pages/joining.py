import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, State, callback, dcc, html

from src.db.code_explanation import (sql_join_inner, sql_join_outer,
                                     sqlmodel_join_inner, sqlmodel_join_outer)
from src.db.db import (join_premium_inner_claims,
                       join_premium_leftouter_claims, select_claims,
                       select_policies, sqlmodel_to_df)
from src.reusable.components import create_grid, id_factory
from src.reusable.layouts import (code_exlanation, col_order_claims,
                                  col_order_policies, further_reading_layout,
                                  raw_data_layout, selection_output_layout)

join_filters = ["Policies inner join claims", "Policies outer join claims"]

further_reading_descriptions = [
    "Create connected tables with SQLModel",
    "Read connected tables with SQLModel",
    "Relationship Attributes SQLModel",
    "Many-to-Many Relationships"
]

further_reading_urls = [
    "https://sqlmodel.tiangolo.com/tutorial/connect/create-connected-tables/",
    "https://sqlmodel.tiangolo.com/tutorial/connect/read-connected-data/",
    "https://sqlmodel.tiangolo.com/tutorial/relationship-attributes/define-relationships-attributes/",
    "https://sqlmodel.tiangolo.com/tutorial/many-to-many/"
]

dash.register_page(__name__, path="/joining_data", name="Joining Data", order=4)

_id = id_factory("joining-data")

output_layout = selection_output_layout(id_func=_id)

raw_data_component = raw_data_layout(id_func=_id)
further_reading_component = further_reading_layout(
    descriptions=further_reading_descriptions, urls=further_reading_urls
)

joined_col_order = col_order_policies + col_order_claims
empty_claims_dict = {col: None for col in col_order_claims}

number_cols = ["premium_gbp", "claim_gbp"]

layout = [
    dcc.Store(id=_id("code-explanation-items")),
    html.H1("Joining Data"),
    html.H2("Data:"),
    raw_data_component,
    html.H2("Joining Options:"),
    html.P("Select the data table and choose from the filters below"),
    dbc.Row(
        [
            dcc.Dropdown(
                options=join_filters,
                value=join_filters[0],
                multi=False,
                id=_id("selection-dropdown"),
            ),
        ],
        style={"margin-bottom": "1rem"},
    ),
    html.H2("Joined Output:"),
    output_layout,
    html.P(id=_id("joined-output-text")),
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
    Output(component_id=_id("joined-output-text"), component_property="children"),
    Input(component_id=_id("selection-dropdown"), component_property="value"),
)
def join_data_tables(dropdown_selection):
    if dropdown_selection == join_filters[0]:
        data = join_premium_inner_claims()
        records = [{**x[0].dict(), **x[1].dict()} for x in data]
        text = None
    else:
        data = join_premium_leftouter_claims()
        records = [
            {**x[0].dict(), **x[1].dict()} if x[1] else {**x[0].dict()} for x in data
        ]
        text = "Note two entries for p_70"

    filter_df = pd.DataFrame(records)
    filter_df = filter_df.loc[:, joined_col_order]
    filter_df = filter_df.iloc[:, :-1]

    grid = create_grid(
        _id=_id("output-grid"),
        df=filter_df,
        number_cols=number_cols,
        columnSize="autoSize",
    )

    return grid, text


@callback(
    Output(component_id=_id("code-explanation"), component_property="children"),
    Input(component_id=_id("selection-dropdown"), component_property="value"),
)
def code_explanation(dropdown_selection):
    if dropdown_selection == join_filters[0]:
        code_explanation_component = code_exlanation(
            _id,
            sqlmodel_markdown=sqlmodel_join_inner,
            sql_markdown=sql_join_inner,
        )
    elif dropdown_selection == join_filters[1]:
        code_explanation_component = code_exlanation(
            _id,
            sqlmodel_markdown=sqlmodel_join_outer,
            sql_markdown=sql_join_outer,
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
