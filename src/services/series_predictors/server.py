import os
import time
from datetime import timedelta, datetime

import schedule

from src.modules.ts_models.runners import FrozenModel
from src.modules.db_helpers.config import CurrencyTables
from src.services.series_predictors.utils import generate_future_dates, get_last_model_update
from src.modules.db_helpers.helper import get_time_for_row, get_currency_data, upload_prediction_data


def poll():
    for currency in currencies_pairs.keys():
        currency_data = currencies_pairs[currency]
        model = models[currency]

        pred_time = get_time_for_row(currency_data['prediction'], 'begin')
        orig_time = get_time_for_row(currency_data['historical'])
        print('First predict time: ', pred_time)
        print('Last historical time: ', orig_time)

        if orig_time - pred_time > timedelta(minutes=30):
            if datetime.now() - get_last_model_update() > timedelta(days=2):
                data = get_currency_data(currency_data['historical'], days_step=2)
                data = data.set_index('unix_timestamp').iloc[-125:, :]
                X = data.drop(data.columns, axis=1)
                y = data['close'].to_list()

                model.fit(X, y)

            future_dates = generate_future_dates(orig_time, 40)
            future_dates['close'] = model.predict(future_dates)
            start = datetime.now()
            upload_prediction_data(currency_data['prediction'], future_dates)
            print('Uploading takes: ', datetime.now() - start)


if __name__ == '__main__':
    global currencies_pairs
    global models
    currencies_pairs = {}
    models = {}

    # find pairs for currencies
    for table in CurrencyTables:
        name = table.name.split('_')
        base_name = name[0]

        if base_name not in currencies_pairs:
            currencies_pairs[base_name] = {}

        if len(name) == 1:
            currencies_pairs[base_name]['historical'] = table
        else:
            currencies_pairs[base_name]['prediction'] = table

    # load models
    for model_name in currencies_pairs.keys():
        models[model_name] = FrozenModel(os.path.join('../../../models', f'{model_name}.ctb'))


    schedule.every(10).minutes.do(poll)
    while True:
        schedule.run_pending()
        time.sleep(1)
