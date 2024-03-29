import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, State, callback, dcc, html

from src.db.code_explanation import (sql_group_sum_premium, sql_group_avg_max_min, sql_group_join,
                                     sqlmodel_group_sum_premium, sqlmodel_group_avg_max_min, sqlmodel_group_join)
from src.db.db import (group_premium_by_classid, group_premium_by_classid_uw_year,
                       join_group_premium_with_claims, select_claims,
                       select_policies, sqlmodel_to_df)
from src.reusable.components import create_grid, id_factory
from src.reusable.layouts import (code_exlanation, col_order_claims,
                                  col_order_policies, further_reading_layout,
                                  raw_data_layout, selection_output_layout)

groupby_filters = ["Group policies by class_id and sum premium",
                   "Group policies by class_id, uw_year and count/min/max/average premium",
                   "Join claims and policies and group by class, uw_year and count/sum premium and claims"]

further_reading_descriptions = [
    "Aggregate functions with SQL Alchemy"
]

further_reading_urls = [
    "https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#aggregate-functions-with-group-by-having"
]

dash.register_page(__name__, path="/grouping_data", name="Grouping Data", order=5)

_id = id_factory("grouping-data")

output_layout = selection_output_layout(id_func=_id)

raw_data_component = raw_data_layout(id_func=_id)
further_reading_component = further_reading_layout(
    descriptions=further_reading_descriptions, urls=further_reading_urls
)

joined_col_order = col_order_policies + col_order_claims
empty_claims_dict = {col: None for col in col_order_claims}

number_cols = ["premium_gbp", "claim_gbp", "min_premium", "avg_premium", "max_premium", "sum_premium", "sum_claims"]

layout = [
    dcc.Store(id=_id("code-explanation-items")),
    html.H1("Grouping Data"),
    html.H2("Data:"),
    raw_data_component,
    html.H2("Grouping Options:"),
    html.P("Select the data table and choose from the filters below"),
    dbc.Row(
        [
            dcc.Dropdown(
                options=groupby_filters,
                value=groupby_filters[0],
                multi=False,
                searchable=False,
                optionHeight=50,
                id=_id("selection-dropdown")
            ),
        ],
        style={"margin-bottom": "1rem"},
    ),
    html.H2("Grouped Output:"),
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
)
def group_data_tables(dropdown_selection):
    if dropdown_selection == groupby_filters[0]:
        data = group_premium_by_classid()
    elif dropdown_selection == groupby_filters[1]:
        data = group_premium_by_classid_uw_year()
    else:
        data = join_group_premium_with_claims()

    filter_df = pd.DataFrame(data)

    grid = create_grid(
        _id=_id("output-grid"),
        df=filter_df,
        number_cols=number_cols,
    )

    return grid


@callback(
    Output(component_id=_id("code-explanation"), component_property="children"),
    Input(component_id=_id("selection-dropdown"), component_property="value"),
)
def code_explanation(dropdown_selection):
    if dropdown_selection == groupby_filters[0]:
        code_explanation_component = code_exlanation(
            _id,
            sqlmodel_markdown=sqlmodel_group_sum_premium,
            sql_markdown=sql_group_sum_premium,
        )
    elif dropdown_selection == groupby_filters[1]:
        code_explanation_component = code_exlanation(
            _id,
            sqlmodel_markdown=sqlmodel_group_avg_max_min,
            sql_markdown=sql_group_avg_max_min,
        )
    else:
        code_explanation_component = code_exlanation(
            _id,
            sqlmodel_markdown=sqlmodel_group_join,
            sql_markdown=sql_group_join,
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
