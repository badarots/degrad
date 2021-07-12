from urllib.parse import urlencode, quote_plus
import datetime as dt
from typing import List

import pandas as pd
import plotly.express as px


path = "http://127.0.0.1:8000/reading/"


def request_url(path: str, params: dict):
    query = urlencode(params, quote_via=quote_plus)
    return path + "?" + query


def get_data(property: str, start: str, end: str, limit=1000):
    start_date = dt.date.fromisoformat(start)
    start_datetime = dt.datetime.combine(start_date, dt.time())

    end_date = dt.date.fromisoformat(end)
    end_datetime = dt.datetime.combine(end_date, dt.time(23, 59, 59))

    prop_path = path + property
    url = request_url(
        prop_path, {"start": start_datetime, "end": end_datetime, "limit": limit})
    try:
        data = pd.read_json(url)
        if data.empty:
            return None
        else:
            return data

    except:
        return None


def update_whether(start: str, end: str):
    df = get_data('whether', start, end)
    properties = ['temperature', 'pressure',  'humidity']
    figures = []
    if df is not None:
        for prop in properties:
            fig = px.scatter(df, x="date", y=prop, title=prop)
            # Enable scatter + connecting lines
            fig.update_traces(mode='lines+markers')
            figures.append(fig)
        return figures
    else:
        return [px.scatter(title=prob) for prob in properties] 
