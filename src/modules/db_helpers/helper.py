import psycopg2
from datetime import datetime

from src.modules.db_helpers.config import CurrencyTables
from src.modules.db_helpers.utils import currency_data_to_df

currency_db = psycopg2.connect(
    dbname='cryptodata',
    user='stockx-team',
    password='AAFj2RKy9PxPadMEEBGv',
    host='34.91.54.163',
)


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
        time_step = 60 * 24 * days_step
    if hours_step:
        time_step = 60 * hours_step
    if minutes_step:
        time_step = minutes_step

    table_name = currency_table.value

    cursor = currency_db.cursor()
    cursor.execute(
        f'SELECT * FROM "{table_name}" WHERE '
        f'MOD("unix_timestamp", {time_step}) = 0;'
    )
    raw_data = cursor.fetchall()

    return currency_data_to_df(raw_data, get_columns_name(currency_table))


def get_time_from_last_row(currency_table):
    """If not exist, return 1970.**"""
    cursor = currency_db.cursor()
    table_name = currency_table.value
    cursor.execute(
        f'SELECT "unix_timestamp" FROM "{table_name}"'
        f' ORDER BY "unix_timestamp" DESC LIMIT 1;'
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

    cursor.execute(f'INSERT INTO {table_name} (model_name) VALUES (%s)', values)

    currency_db.commit()
