import time
from datetime import datetime

import schedule

from src.modules.binace import update_candlestick_data
from src.modules.db_helpers.helper import get_currency_tables_pairs


CURRENCIES_PAIRS = (
    'BTCUSDT',
    'ETHUSDT',
    'XRPUSDT'
)


def update():
    for pair in CURRENCIES_PAIRS:
        print(
            f'{datetime.now().strftime("%d-%m-%Y %H:%M:%S")}: Updating data for {pair} pair.'
        )

        last_timestamp, data_length = update_candlestick_data(pair)

        last_timestamp_formatted = datetime.fromtimestamp(last_timestamp / 1e3).strftime("%d-%m-%Y %H:%M:%S")
        print(f'{datetime.now().strftime("%d-%m-%Y %H:%M:%S")}: Updated {data_length} data point(s) from {last_timestamp_formatted} till now.')


if __name__ == '__main__':
    schedule.every(1).minutes.do(update)

    while True:
        schedule.run_pending()
        time.sleep(1)
