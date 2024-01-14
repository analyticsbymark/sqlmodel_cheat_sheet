import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import pandas as pd


def id_factory(page: str):
    def func(_id: str):
        return f"{page}-{_id}"

    return func


def add_navbar(title: str = None, link_dict: dict = None, **kwargs):
    navbar = dbc.NavbarSimple(
        [
            dbc.NavItem(
                dbc.NavLink(page["name"], href=page["path"]),
                style={"color": "rgba(255, 255, 255, 1)"},
            )
            for page in link_dict
            if page["module"] != "pages.not_found_404"
        ],
        brand=title,
        dark=True,
        className="mb-2",
        **kwargs,
    )

    return navbar


def create_grid(
    _id: str,
    df: pd.DataFrame,
    number_cols: list,
    height: int = 200,
    **kwargs,
):
    columnDefs = []

    for col in df.columns:
        df_col = {
            "field": col,
            "headerName": col,
            "autoHeight": True,
            "cellStyle": {"fontSize": "1.2rem"},
        }

        if col in number_cols:
            df_col["filter"] = "agNumberColumnFilter"
            df_col["valueFormatter"] = {"function": "d3.format(',.0f')(params.value)"}

        columnDefs.append(df_col)

    return dag.AgGrid(
        rowData=df.to_dict("records"),
        columnDefs=columnDefs,
        defaultColDef={"resizable": True, "sortable": True, "filter": True},
        columnSize="sizeToFit",
        columnSizeOptions={
            'defaultMinWidth': 100
        },
        style={"height": height},
        dashGridOptions={"rowHeight": "16", "headerHeight": "24"},
        className="ag-theme-alpine border",
        id=_id,
        **kwargs,
    )
