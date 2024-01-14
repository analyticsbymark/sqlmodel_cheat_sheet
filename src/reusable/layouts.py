import dash_bootstrap_components as dbc
from dash import dcc, html

col_order_policies = ["policy_id", "class_id", "uw_year", "premium_gbp"]
col_order_claims = ["claim_id", "country", "claim_gbp", "policy_id"]


def raw_data_layout(id_func):
    return dbc.Row(
        [
            dbc.Card(
                [
                    dbc.CardHeader(
                        dbc.Tabs(
                            [
                                dbc.Tab(label="Policy Data", tab_id="policy-tab"),
                                dbc.Tab(label="Claims Data", tab_id="claims-tab"),
                            ],
                            id=id_func("raw-data-tabs"),
                            active_tab="policy-tab",
                        )
                    ),
                    dbc.CardBody(id=id_func("data-card-content")),
                ],
                style={"padding": "1.4rem", "border-radius": "1rem"},
            )
        ],
        style={"padding-bottom": "1rem"},
    )


def code_exlanation(id_func, sqlmodel_markdown: str, sql_markdown: str):
    return dbc.Accordion(
        [
            dbc.AccordionItem(
                [
                    dcc.Clipboard(
                        target_id=id_func("sqlmodel-markdown"),
                    ),
                    dcc.Markdown(sqlmodel_markdown, id=id_func("sqlmodel-markdown")),
                ],
                title="SQLModel (Python)",
                item_id=id_func("sqlmodel-item"),
            ),
            dbc.AccordionItem(
                [
                    dcc.Clipboard(
                        target_id=id_func("sql-markdown"),
                    ),
                    dcc.Markdown(sql_markdown, id=id_func("sql-markdown")),
                ],
                title="SQL",
                item_id=id_func("sql-item"),
            ),
        ],
        id=id_func("accordion"),
        active_item=[id_func("sqlmodel-item")],
        always_open=True,
        flush=True,
    )


def further_reading_layout(descriptions: list, urls: list):
    return dbc.Row(
        dbc.Card(
            dbc.CardBody(
                [
                    html.Li(html.A(text, href=url, target="_blank"))
                    for text, url in zip(descriptions, urls)
                ]
            ),
            style={"border-radius": "1rem", "margin-bottom": "1rem"},
        )
    )


def selection_output_layout(id_func):
    return dbc.Row(
        [
            dbc.Card(
                [
                    dbc.CardBody(id=id_func("selection-output-content")),
                ],
                style={"padding": "1.4rem", "border-radius": "1rem"},
            )
        ],
        style={"padding-bottom": "1rem"},
    )
