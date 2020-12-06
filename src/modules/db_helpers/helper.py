from datetime import datetime
from io import StringIO

import psycopg2

from src.modules.db_helpers.utils import currency_data_to_df


COLUMNS = [
    'open',
    'high',
    'low',
    'close',
    'volume',
    'number_of_trades',
    'unix_timestamp'
]


credentials = {
   'host': '34.91.54.163',
   'port': '5432',
   'user': 'stockx-team',
   'password': 'AAFj2RKy9PxPadMEEBGv',
   'database': 'cryptodata'
}

currency_db = psycopg2.connect(**credentials)
currency_db.autocommit = True


def get_columns_name(currency_table):
    cursor = currency_db.cursor()
    cursor.execute(
        f"SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS "
        f"WHERE table_name = '{currency_table.value}';"
    )

    names = [v[0] for v in cursor.fetchall()]
    return names


def get_currency_data(currency_table, days_step=None, hours_step=None, minutes_step=None):
    nones_count = (days_step is None) + (hours_step is None)
    nones_count += minutes_step is None
    if nones_count <= 1:
        raise Exception('Only one type of steps can be used.')

    if nones_count == 3:
        raise Exception('Steps are not used.')

    if days_step:
        time_step = 60 ** 2 * 24 * days_step
    if hours_step:
        time_step = 60 ** 2 * hours_step
    if minutes_step:
        time_step = 60 * minutes_step

    table_name = currency_table.value

    cursor = currency_db.cursor()
    cursor.execute(
        f'SELECT * FROM "{table_name}" WHERE '
        f'MOD("unix_timestamp", {time_step}) = 0 ORDER BY "unix_timestamp";'
    )
    raw_data = cursor.fetchall()

    return currency_data_to_df(raw_data, get_columns_name(currency_table))


def get_time_for_row(currency_table, position='end'):
    """If not exist, return 1970.**"""
    cursor = currency_db.cursor()
    table_name = currency_table.value

    if position == 'end':
        cursor.execute(
            f'SELECT "unix_timestamp" FROM "{table_name}"'
            f' ORDER BY "unix_timestamp" DESC LIMIT 1;'
        )
    else:
        cursor.execute(
            f'SELECT "unix_timestamp" FROM "{table_name}"'
            f' ORDER BY "unix_timestamp" ASC LIMIT 1;'
        )

    res = cursor.fetchone()
    if res:
        return datetime.fromtimestamp(res[0])
    else:
        return datetime.fromtimestamp(0)


def upload_prediction_data(currency_table, data):
    cursor = currency_db.cursor()

    table_name = currency_table.value
    cursor.execute(
        f'DELETE FROM "{table_name}" WHERE true;'
    )

    time_values = [v.timestamp() for v in data.index]
    rate_values = data['close'].tolist()
    zipped = list(zip(time_values, rate_values))

    cursor.executemany(f'INSERT INTO "{table_name}" ("unix_timestamp", "value")'
                       f' VALUES (%s, %s)', zipped)

    currency_db.commit()


def get_last_timestamp(currency_pair):
    with currency_db.cursor() as cursor:
        cursor.execute(f'SELECT MAX(unix_timestamp) FROM public."{currency_pair}"')

        timestamp = next(cursor)[0]
        if timestamp:
            return timestamp
        else:
            return 0


def load_candlestick_data(df, currency_pair):
    with currency_db.cursor() as cursor:
        cursor.copy_from(
            StringIO(
                df.to_csv(
                    sep='\t',
                    header=False,
                    index=False,
                    columns=COLUMNS
                )
            ),
            f'"{currency_pair}"',
            columns=COLUMNS
        )
