from pathlib import Path
from typing import Callable

import numpy as np
import pandas as pd
from tqdm import tqdm


class ClassificationDataSplitter:
    @staticmethod
    def _save_group_data_to_parquet(destination_dir: Path, n_splits):
        for i in range(n_splits):
            (destination_dir / str(i)).mkdir(exist_ok=True, parents=True)

        def _saver(df, split_ix, group_id):
            df.to_parquet(destination_dir / str(split_ix) / f'{group_id}.parquet')

        return _saver

    @staticmethod
    def _save_group_data_to_csv(destination_dir: Path, n_splits):
        for i in range(n_splits):
            (destination_dir / str(i)).mkdir(exist_ok=True, parents=True)

        def _saver(df, split_ix, group_id):
            df.to_csv(destination_dir / str(split_ix) / f'{group_id}.csv', index=False)

        return _saver

    @staticmethod
    def random_split(
            df: pd.DataFrame,
            group_column: str,
            n_splits: int,
            batch_size: int,
            data_saver: Callable[[pd.DataFrame, int, str], None],
            seed: int,
    ):
        state = np.random.RandomState(seed)
        groups = df[group_column].unique()
        state.shuffle(groups)

        current_split = 0
        for b_start in tqdm(range(0, len(groups), batch_size), total=len(groups) / batch_size):
            b = groups[b_start:b_start + batch_size]

            g_data = df.query(f'{group_column} in @b')
            data_saver(g_data, current_split, str(b_start))

            current_split += 1
            current_split = current_split % n_splits
