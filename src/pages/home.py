import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback, dcc, html

from src.reusable.components import id_factory
from src.reusable.layouts import further_reading_layout

dash.register_page(__name__, path="/", name="Home", order=0)

_id = id_factory("home")

socials = ["LinkedIn", "Cheat Sheet Source Code"]

social_urls = [
    "https://www.linkedin.com/in/mark-cooper-b8878686",
    "https://github.com/analyticsbymark/sqlmodel_cheat_sheet",
]

social_component = further_reading_layout(
    descriptions=socials, urls=social_urls
)


layout = [
    html.H1("Home"),
    dcc.Markdown("""
    ##### 👋 Welcome to the SQLModel Cheatsheet.
    This is an interactive cheatsheet showcasing some of the features offered by [SQLModel](https://sqlmodel.tiangolo.com/).
    
    It covers the basics of creating tables, selecting columns, filtering, joining and grouping data. 
    
    See python code applied to the data and the equivalent SQL.
    """,
    link_target="_blank"),
    html.H2("Socials:"),
    social_component
]
