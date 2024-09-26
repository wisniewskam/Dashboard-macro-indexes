"""
pip install dash
pip install plotly
pip install dash-bootstrap-templates
pip install dash_bootstrap_components
pip install pandas
"""
import dash
from dash import dcc, html
from dash_bootstrap_templates import ThemeSwitchAIO
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components as dbc

# Templaty do zmiany stylu
dbc_css = ("https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.1/dbc.min.css")
load_figure_template("CERULEAN")

df = pd.DataFrame()
# Wczytanie danych
gdp_df = pd.read_csv("GDP.csv")
inflation_df = pd.read_csv("Inflation.csv")
unemployment_df = pd.read_csv("Unemployment.csv")

# Tworzenie aplikacji Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN, dbc_css, dbc.icons.BOOTSTRAP])

# Layout aplikacji
app.layout = dbc.Container([
    html.H1("Economic Indicators Dashboard", style={"text-align": "center"}),
    dbc.Row([
            dbc.Col([
                    ThemeSwitchAIO(
                        aio_id="theme",
                        icons={"left": "bi bi-moon", "right": "bi bi-sun"},
                        themes=[dbc.themes.CERULEAN, dbc.themes.SLATE],
                        ),
                    ]
                )]
        ),
    dcc.Tabs([
# Tab 1 zawiera wykres główny z elementami pozwalającymi na wybór wskaźników i państw
        dcc.Tab(
            dbc.Row([
                html.H4("Select indicator and countries"),
                dbc.Col(
# Lista rozwijalna z jednokrotnym wyborem wskaźnika
                    dcc.Dropdown(
                        id='indicator-dropdown',
                        options=[
                            {'label': 'GDP', 'value': 'GDP'},
                            {'label': 'Inflation', 'value': 'Price Index'},
                            {'label': 'Unemployment', 'value': 'Unemployment'}
                        ],
                        value='GDP',
                        clearable=False,
                        className='dbc',
                        style={'margin-bottom': '20px'}
                    ),width=4
                ),
                dbc.Col(
# Lista rozwijalna z wielokrotnym wyborem państwa
                    dcc.Dropdown(
                        id='country-dropdown',
                        multi=True,
                        className='dbc',
                        style={'margin-bottom': '20px'}
                    ),width=8
                ),
                dbc.Row([
                    dbc.Col(
# Wykres główny
                        dcc.Graph(id='indicator-graph',
                                  style={'margin-bottom': '20px'}),
                        width=12
                    ),
                ])
            ])
            , label='Main chart'),
# Tab 2 zawiera informacje o projekcie w postaci tekstu
        dcc.Tab(html.Div([
            html.H3('Information about the Project'),
            html.P('This project aims to analyze economic data such as GDP, inflation and unemployment.'
                   'Data from the European Statistical Office (Eurostat) was used and an interactive '
                   'dashboard was created on their basis. '
                   'The user can select indicators and view data from 2004-2023 on countries that '
                   'joined the European Union in 2004.'
                   ),
            html.P('The technologies used in the project are Python, Dash, Pandas and Plotly, '
                   'which allow you to create interactive web applications for '
                   'data analysis and visualization.'),
            html.H4('Dictionary'),
            html.P('GDP (Gross domestic product) - the project presents the percentage change '
                   'in GDP compared to the previous period, '),
            html.P('Inflation - the harmonized index of consumer prices (HICP) is presented -'
                   ' changes in prices of representatives of consumer goods and services are calculated by member '
                   'countries according to the unified methodology of the European Union'),
            html.P('Unemployment - unemployment rate for women and men aged 15-74 presented.'),
            html.H5('Data sources'),
            html.P('https://ec.europa.eu/eurostat/databrowser/view/nama_10_gdp/default/table?lang=en '
                   'https://ec.europa.eu/eurostat/databrowser/view/prc_hicp_aind/default/table?lang=en&category=prc.prc_hicp '
                   'https://ec.europa.eu/eurostat/databrowser/view/lfsq_urgan/default/table?lang=en'),

        ]), label='About Me', value='tab-2'),
    ],
        className='dbc'),
# Dostosowanie się aplikacji do okna
], fluid=True)

# Callback do aktualizacji listy krajów w zależności od wybranego wskaźnika
@app.callback(
    Output('country-dropdown', 'options'),
    Input('indicator-dropdown', 'value')
)

def set_country_options(selected_indicator):
    if selected_indicator == 'GDP':
        countries = gdp_df['geo'].unique()
    elif selected_indicator == 'Inflation':
        countries = inflation_df['geo'].unique()
    elif selected_indicator == 'Unemployment':
        countries = unemployment_df['geo'].unique()
    else:
        countries = []

    return [{'label': country, 'value': country} for country in countries]

# Callback do aktualizacji wykresu
@app.callback(
    Output('indicator-graph', 'figure'),
    [Input('indicator-dropdown', 'value'),
     Input('country-dropdown', 'value'),
     Input(ThemeSwitchAIO.ids.switch("theme"), 'value')]
)

def update_graph(selected_indicator, selected_countries, toggle):
    if selected_indicator == 'GDP':
        df = gdp_df
    elif selected_indicator == 'Inflation':
        df = inflation_df
    elif selected_indicator == 'Unemployment':
        df = unemployment_df
    else:
        df = pd.DataFrame()

    if not selected_countries:
        selected_countries = df['geo'].unique()

    template = dbc.themes.CERULEAN if toggle else dbc.themes.SLATE

    filtered_df = df[df['geo'].isin(selected_countries)]
    fig = px.line(filtered_df, x='TIME_PERIOD', y='OBS_VALUE', color='geo', title=f'{selected_indicator} of Selected Countries',
                  labels={'TIME_PERIOD': 'Year', 'OBS_VALUE': 'Value (%)', 'geo': 'Country Code'})

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
