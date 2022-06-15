from typing import Callable

from kaggletools.core.visualisation.pandas import GradientBackgroundFiller
import pandas as pd


def correlation_heatmap(
    df: pd.DataFrame,
    method: str = 'spearman',
    display: Callable[[pd.DataFrame], None] = None,
) -> pd.DataFrame:
    corr = df.corr(method=method)
    corr.style.pipe(GradientBackgroundFiller.red_blue)

    if display is not None:
        with pd.option_context(
                'display.max_rows', corr.shape[0],
                'display.max_columns', corr.shape[1],
        ):
            display(corr)

    return corr
