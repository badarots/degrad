# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import datetime as dt

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_daq as daq

from app_utils import update_whether


app = dash.Dash(__name__)

colors = {
    'background': '#ffffff',
    'text': '#333333'
}


app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1('Degrad DashBoard',
            style={'textAlign': 'center', 'color': colors['text']}
            ),

    html.Div('Dash: A web application framework for Python.',
             style={'textAlign': 'center', 'color': colors['text']}
             ),

    # This will fire every interval and update the plots data
    dcc.Interval(
        id='interval-component',
        interval=10*1000,  # in milliseconds
        n_intervals=0
    ),

    html.Div(
        style={"display": "flex", 'justifyContent': 'space-around'},
        children=[
            dcc.DatePickerRange(
                id='date-range',
                min_date_allowed=dt.date(2021, 6, 1),
                start_date=dt.date.today() - dt.timedelta(weeks=1),
                end_date=dt.date.today(),
                style={'textAlign': 'center'}
            ),
            daq.BooleanSwitch(
                id='live_update_switch',
                on=False,
                label="Auto update",
                labelPosition="top"
            )
        ]
    ),

    html.Div(
        style={"display": "flex", 'justifyContent': 'center'},
        children=[
            dcc.Graph(id='temperature-graph'),
            dcc.Graph(id='pressure-graph'),
            dcc.Graph(id='humidity-graph')
        ])
])


@app.callback(
    Output('temperature-graph', 'figure'),
    Output('pressure-graph', 'figure'),
    Output('humidity-graph', 'figure'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date'),
    Input('interval-component', 'n_intervals')
)
def update_graphs(start: str, end: str, n_intervals):
    return update_whether(start, end)


@app.callback(
    Output('interval-component', 'disabled'),
    Input('live_update_switch', 'on')
)
def disable_live_update(on: bool):
    return not on


if __name__ == '__main__':
    app.run_server(debug=True)
