import pandas as pd
from pandas.api.types import infer_dtype
import numpy as np


def optimize_dtypes(df: pd.DataFrame) -> None:
    """
    Tries to reduce memory consumption by downcasting floats and integers and by converting strings to categories.

    :param df:
    :return:
    """
    if len(df) == 0:
        return

    for column in df.columns:
        column_type = infer_dtype(df[column], skipna=True)
        has_na = df[column].isnull().sum() > 0

        if column_type == 'floating' or (column_type == 'integer' and has_na) or column_type == 'mixed-integer-float':
            max_value = df[column].abs().max()
            max_value *= 1.99

            new_type = np.min_scalar_type(max_value)
            df[column] = df[column].astype(new_type)

        elif column_type == 'integer':
            max_value = df[column].abs().max()
            if np.any(df[column] < 0):
                max_value *= -2
            else:
                max_value *= 2

            new_type = np.min_scalar_type(max_value)
            df[column] = df[column].astype(new_type)

        elif:







        elif
        'string'
        'bytes'
        ''
        'mixed-integer'

        'decimal'
        'complex'
        'categorical'
        'boolean'
        'datetime64'
        'datetime'
        'date'
        'timedelta64'
        'timedelta'
        'time'
        'period'
        'mixed'
        'unknown-array'



         = df.dtypes[column]

        if column_type == 'object':
            n_items = len(df)
            n_unique = df[column].nunique(dropna=True)

            if n_unique/n_items < 0.05:
                df[column] = df[column].astype('category')

        elif column_type == 'float' or column_type == 'int':
            has_negative_values = np.any(df[column] < 0)
            has_nans = 0 < df[column].isnull().sum()
            max_value = df[column].abs().max()

            if column_type == 'float' or has_nans:
                multiplier = 1.99
            else:
                multiplier = 2

            if has_negative_values:
                new_type = np.min_scalar_type(-multiplier*max_value)
            else:
                new_type = np.min_scalar_type(multiplier*max_value)

            if new_type < column_type:
                df[column] = df[column].astype(new_type)
        else:
            pass
