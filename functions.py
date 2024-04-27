from typing import Optional
import pandas as pd


def crypto_dataset(dataset_path: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
    """
    This function processes a CSV file containing the historical data of cryptocurrencies, having an optional date range
    filter data within the given dates in '%Y-%m-%d' format.

    :param dataset_path: Path to the crypto dataset
    :param start_date: Optional parameter to filter the dataset from a given range.
    :param end_date: Optional parameter to filter the dataset from a given range.
    :returns: pd.Dataframe: Pandas DataFrame for the given Cryptocurrency
    :raises ValueError: If the dataset path is invalid, or if the date range is invalid.


>>> fs = crypto_dataset("./Crypto Dataset/bitcoin_2013-01-01_2024-04-22.csv", start_date='2022-01-01', end_date='2022-01-04')
>>> print(fs.shape)
(4, 7)

    """

    if not isinstance(dataset_path, str):
        raise ValueError("dataset_path must be a string.")

    try:
        df = pd.read_csv(dataset_path)
    except FileNotFoundError:
        raise ValueError(f"File not found at: {dataset_path}")

    df = df.drop('End', axis=1)

    df.rename(columns={'Start': 'Date'}, inplace=True)

    df['Date'] = pd.to_datetime(df['Date'])

    if start_date and end_date:
        df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    if start_date and not end_date:
        df = df[df['Date'] >= start_date]
    if end_date and not start_date:
        df = df[df['Date'] <= end_date]
    if df.empty:
        raise ValueError(f"No data found within the specified date range: "
                         f"{start_date} to {end_date}")

    df.sort_values(by='Date', ascending=True, inplace=True)
    return df


bitcoin = crypto_dataset("./Crypto Dataset/bitcoin_2013-01-01_2024-04-22.csv", start_date='2022-01-01',
                         end_date='2022-02-04')

print(bitcoin)

ethereum = crypto_dataset("./Crypto Dataset/ethereum_2016-01-01_2024-04-22.csv")

print(ethereum.head())

