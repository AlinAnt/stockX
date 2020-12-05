import os
from src.modules.db_helpers.config import CurrencyTables
from src.modules.ts_models.runners import FrozenModel


def poll():
    print(currencies_pairs)


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
            currencies_pairs[base_name]['original'] = table
        else:
            currencies_pairs[base_name]['prediction'] = table

    # load models
    for model_name in currencies_pairs.keys():
        models[model_name] = FrozenModel(os.path.join('../../../models', f'{model_name}.ctb'))

    print(models)

    poll()
