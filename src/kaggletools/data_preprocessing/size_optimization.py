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

        elif column_type == 'string':
            n_items = len(df)
            n_unique = df[column].nunique(dropna=True)

            if n_unique / n_items < 0.1:
                df[column] = df[column].astype('category')
        else:
            ...
