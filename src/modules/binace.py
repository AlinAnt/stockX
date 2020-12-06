import time
import requests

import numpy as np
import pandas as pd

from src.modules.db_helpers.helper import load_candlestick_data, get_last_timestamp

API = 'https://api.binance.com/api/v3/'

CANDLESTICK_COLUMNS = [
    'open_time',
    'open',
    'high',
    'low',
    'close',
    'volume',
    'close_time',
    'quote_asset_volume',
    'number_of_trades',
    'taker_buy_base_asset_volume',
    'taker_buy_quote_asset_volume',
    'ignore'
]


def _get_batch(currency_pair, start_time=0, interval='1m', limit=1000):
    response = requests.get(
        f'{API}klines',
        {
            'symbol': ''.join(currency_pair),
            'interval': interval,
            'startTime': start_time,
            'limit': limit
        }
    )

    if response.status_code == 200:
        return pd.DataFrame(response.json(), columns=CANDLESTICK_COLUMNS)
    else:
        return None


def _get_binace_data(currency_pair, start_time=0, interval='1m', limit=1000):
    last_timestamp = start_time

    batches = []

    while True:
        batch = _get_batch(
            currency_pair,
            start_time=last_timestamp + 1
        )

        if batch.empty:
            break

        last_timestamp = batch['open_time'].max()

        batches.append(batch)

        print(last_timestamp)

        time.sleep(0.1)

    if batches:
        return pd.concat(batches, ignore_index=True)
    else:
        return None


def _preprocess(df):
    df['unix_timestamp'] = (df['open_time'] / 1e3).astype(np.int64)

    return df


def update_candlestick_data(currency_pair):
    last_timestamp = get_last_timestamp(currency_pair) * 1000

    load_candlestick_data(
        _preprocess(
            _get_binace_data(
                currency_pair,
                start_time=last_timestamp + 1
            )
        ),
        currency_pair
    )
