"""Common functions"""
from typing import Dict, Union

import dask.dataframe as dd
import numpy as np
import pandas as pd


NULL_VALUES = {
    np.nan,
    float("NaN"),
    "#N/A",
    "#N/A N/A",
    "#NA",
    "-1.#IND",
    "-1.#QNAN",
    "-NaN",
    "-nan",
    "1.#IND",
    "1.#QNAN",
    "<NA>",
    "N/A",
    "NA",
    "NULL",
    "NaN",
    "n/a",
    "nan",
    "null",
    "",
}


def to_dask(df: Union[pd.DataFrame, dd.DataFrame]) -> dd.DataFrame:
    """Convert a dataframe to a dask dataframe."""
    if isinstance(df, dd.DataFrame):
        return df

    df_size = df.memory_usage(deep=True).sum()
    npartitions = np.ceil(df_size / 128 / 1024 / 1024)  # 128 MB partition size
    return dd.from_pandas(df, npartitions=npartitions)


def report(stats: Dict[str, int], nrows: int) -> None:
    """
    Describe what was done in the cleaning process
    """
    # pylint: disable=line-too-long
    print("Latitude and Longitude Cleaning Report:")
    if stats["cleaned"] > 0:
        nclnd = stats["cleaned"]
        pclnd = round(nclnd / nrows * 100, 2)
        print(f"\t{nclnd} values cleaned ({pclnd}%)")
    if stats["unknown"] > 0:
        nunknown = stats["unknown"]
        punknown = round(nunknown / nrows * 100, 2)
        print(f"\t{nunknown} values unable to be parsed ({punknown}%), set to NaN")
    nnull = stats["null"] + stats["unknown"]
    pnull = round(nnull / nrows * 100, 2)
    ncorrect = nrows - nnull
    pcorrect = round(100 - pnull, 2)
    print(
        f"""Result contains {ncorrect} ({pcorrect}%) values in the correct format and {nnull} null values ({pnull}%)"""
    )
