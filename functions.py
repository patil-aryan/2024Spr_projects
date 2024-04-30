from typing import Optional
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def crypto_dataset(dataset_path: str, period_one: Optional[str] = None,
                   period_two: Optional[str] = None) -> pd.DataFrame:
    """
    This function extracts data from a CSV file which containts the historical data of a certaincryptocurrency,
    while having an optional period range of dates to filter data within the given period in '%Y-%m-%d' format.

    :param dataset_path: Path to the crypto dataset
    :param period_one: Optional parameter to filter the dataset from a given range.
    :param period_two: Optional parameter to filter the dataset from a given range.
    :returns: pd.Dataframe: Pandas DataFrame for the given Cryptocurrency
    :raises ValueError: If the given dataset path is incorrect or if the period of dates is not in range.


>>> fs = crypto_dataset("./Crypto Dataset/bitcoin_2013-01-01_2024-04-22.csv", period_one='2022-01-01', period_two='2022-01-04')
>>> print(fs.shape)
(4, 7)

    """

    if not isinstance(dataset_path, str):
        raise ValueError("dataset_path must be a string.")

    try:
        crypto_df = pd.read_csv(dataset_path)
    except FileNotFoundError:
        raise ValueError(f"File not found at: {dataset_path}")

    crypto_df = crypto_df.drop('End', axis=1)
    crypto_df.rename(columns={'Start': 'Date'}, inplace=True)
    crypto_df['Date'] = pd.to_datetime(crypto_df['Date'])

    if period_one and period_two:
        crypto_df = crypto_df[(crypto_df['Date'] >= period_one) & (crypto_df['Date'] <= period_two)]
    if period_one and not period_two:
        crypto_df = crypto_df[crypto_df['Date'] >= period_one]
    if period_one and not period_one:
        crypto_df = crypto_df[crypto_df['Date'] <= period_two]
    if crypto_df.empty:
        raise ValueError(f"No data found within the specified date range: "
                         f"{period_one} to {period_two}")

    crypto_df.sort_values(by='Date', ascending=True, inplace=True)
    return crypto_df


def crypto_sentiment(dataset_path: str) -> None:
    """
    This function extracts data from the crypto file containing sentiment and plots the price changes with
    respect to the overall sentiment of the cryptocurrency.
    :param dataset_path: Path to the csv file containing the crypto dataset with sentiment
    :return: None

    """
    crypto_df = pd.read_csv(dataset_path)
    crypto_df['PercentChange'] = crypto_df['Close'].pct_change() * 100
    crypto_df['date'] = pd.to_datetime(crypto_df['date'])

    plt.figure(figsize=(15, 10))
    plt.plot(crypto_df['date'], crypto_df['close'], label='Closing Price', color='black', linestyle='solid')

    positive_date = crypto_df[(crypto_df['changes'] == 'positive') & (crypto_df['PercentChange'] > 2)]['date']
    positive_close = crypto_df[(crypto_df['changes'] == 'positive') & (crypto_df['PercentChange'] > 2)]['close']
    plt.scatter(positive_date, positive_close, color='blue', label='Positive Sentiment', marker='^', s=100)

    negative_date = crypto_df[(crypto_df['changes'] == 'negative') & (crypto_df['PercentChange'] < -2)]['date']
    negative_close = crypto_df[(crypto_df['changes'] == 'negative') & (crypto_df['PercentChange'] < -2)]['close']
    plt.scatter(negative_date, negative_close, color='red', label='Negative Sentiment', marker='v', s=100)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %d, %Y'))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())

    plt.xlabel('Dates')
    plt.ylabel('Bitcoin Closing Price in $')
    plt.title('Changes in Price with respect to Market Sentiment')
    plt.grid(True, linestyle='dotted', linewidth=1)
    plt.legend()
    plt.tight_layout()
    plt.show()



if __name__ == "__main__":
    bitcoin = crypto_dataset("./Crypto Dataset/bitcoin_2013-01-01_2024-04-22.csv", period_one='2022-01-01',
                             period_two='2022-02-04')

    print(bitcoin)

    ethereum = crypto_dataset("./Crypto Dataset/ethereum_2016-01-01_2024-04-22.csv")

    print(ethereum.head())

