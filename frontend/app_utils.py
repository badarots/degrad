from urllib.parse import urlencode, quote_plus
import datetime as dt

import pandas as pd
import plotly.express as px


path = "http://127.0.0.1:8000/reading/"


def request_url(path: str, params: dict):
    query = urlencode(params, quote_via=quote_plus)
    return path + "?" + query


def get_data(property: str, start_date: dt.datetime, end_date: dt.datetime, limit=1000):
    prop_path = path + property
    url = request_url(prop_path, {"start": start_date, "end": end_date, "limit": limit})
    try:
        data = pd.read_json(url)
        if data.empty:
            return None
        else:
            return data

    except:
        return None

def update_figure(property: str, start: str, end: str):
    start_date = dt.date.fromisoformat(start)
    start_datetime = dt.datetime.combine(start_date, dt.time())

    end_date = dt.date.fromisoformat(end)
    end_datetime = dt.datetime.combine(end_date, dt.time(23, 59, 59))
    
    df = get_data(property, start_datetime, end_datetime)
    if df is not None:
        fig = px.scatter(df, x="date", y="value", title=property)
        # Enable scatter + connecting lines
        fig.update_traces(mode='lines+markers')
        return fig
    else:
        return px.scatter(title=property)
