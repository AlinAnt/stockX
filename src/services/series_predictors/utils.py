import os
from datetime import timedelta, datetime

import pandas as pd


def generate_future_dates(start_date, days_count):
    step = timedelta(minutes=60)
    total_minutes = days_count * 24

    start_date = start_date.replace(minute=0, second=0)
    date_range = [start_date + step * i for i in range(total_minutes)]

    return pd.DataFrame(index=date_range)


def get_last_model_update(model):
    timestamp = os.path.getctime(model.model_path)
    return datetime.fromtimestamp(timestamp)