import dash
import dash_bootstrap_components as dbc
from dash import Dash

from src.reusable.components import add_navbar

external_stylesheets = [dbc.themes.BOOTSTRAP]

app = Dash(
    __name__,
    title="SQLModel Cheatsheet",
    external_stylesheets=external_stylesheets,
    use_pages=True,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    suppress_callback_exceptions=True,
)


server = app.server

app.layout = dbc.Container(
    [
        dbc.Container(
            [
                add_navbar(
                    link_dict=dash.page_registry.values(),
                    expand="xs",
                    fluid=True,
                    links_left=True,
                ),
                dash.page_container,
            ]
        )
    ],
    fluid=True,
)


if __name__ == "__main__":
    app.run_server(debug=True)
