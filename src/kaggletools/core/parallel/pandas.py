import logging
import multiprocessing as mp
from typing import Callable

import pandas as pd
from tqdm import tqdm

logger = logging.getLogger(__name__)


def parallel_apply(
    func: Callable[[pd.DataFrame], pd.DataFrame],
    df: pd.DataFrame,
    split_column: str = None,
    verbose: bool = True,
    batch_size: int = None,
    n_jobs: int = None,
) -> pd.DataFrame:
    if n_jobs is None:
        n_jobs = mp.cpu_count()

    if split_column is not None:

        split_values = df[split_column].unique()

        if batch_size is None:
            batch_size = len(split_values) // n_jobs

        batches = []
        for start in range(0, len(split_values), batch_size):
            batch = split_values[start:start + batch_size]
            batches.append(df.query(f'{split_column} in @batch').copy())

    else:
        if batch_size is None:
            batch_size = len(df) // n_jobs

        batches = []
        for start in range(0, len(df), batch_size):
            batches.append(df.iloc[start:start + batch_size, :].copy())

    with mp.Pool(processes=n_jobs) as pool:
        if verbose:
            results = list(tqdm(
                pool.imap(func, batches, chunksize=1),
                total=len(batches),
                desc='processing data',
            ))
        else:
            results = list(pool.imap(func, batches, chunksize=1))

    return pd.concat(results, axis=0)
