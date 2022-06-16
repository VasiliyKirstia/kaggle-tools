from typing import Callable

from kaggletools.core.visualisation.pandas import GradientBackgroundFiller, NumericalDataTransformer
import pandas as pd


__all__ = ['correlation_heatmap']


def correlation_heatmap(
    df: pd.DataFrame,
    method: str = 'spearman',
    display: Callable[[pd.DataFrame], None] = None,
) -> pd.DataFrame:
    corr = df.corr(method=method)
    corr.style.pipe(GradientBackgroundFiller.red_blue(vmin=-1, vmax=1))
    corr.style.pipe(NumericalDataTransformer.round(precision=2, truncate_leading_zero=True))

    if display is not None:
        with pd.option_context(
                'display.max_rows', corr.shape[0],
                'display.max_columns', corr.shape[1],
        ):
            display(corr)

    return corr
