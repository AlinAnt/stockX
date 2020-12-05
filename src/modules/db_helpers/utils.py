import pandas as pd


def currency_data_to_df(result, column_names):
    result = pd.DataFrame(result, columns=column_names)
    result['unix_timestamp'] = pd.to_datetime(
        result['unix_timestamp'], unit='s'
    )
    return result