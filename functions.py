from typing import Optional
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def crypto_dataset(dataset_path: str, period_one: Optional[str] = None,
                   period_two: Optional[str] = None) -> pd.DataFrame:
    """
    This function extracts all the historical data of any given cryptocurrency and returns a Dataframe containing
    extracted data sorted by dates. It also has an optional period range of dates to filter data within the given
    period in '%Y-%m-%d' format.

    :param dataset_path: Path to the cryptocurrency dataset.
    :param period_one: Optional parameter to filter the dataset from a given range (range1).
    :param period_two: Optional parameter to filter the dataset from a given range (range2).
    :returns: pd.Dataframe: Pandas DataFrame for the given Cryptocurrency
    :raises ValueError: If the given dataset path is incorrect or if the period of dates is not in range of the dataset.


>>> c = crypto_dataset("./Crypto Dataset/bitcoin_2013-01-01_2024-04-22.csv", period_one='2022-01-01',
                            period_two='2022-01-04')
>>> print(c.shape)
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
    crypto_df['PercentChange'] = crypto_df['close'].pct_change() * 100
    crypto_df['date'] = pd.to_datetime(crypto_df['date'])

    plt.figure(figsize=(15, 10))
    plt.plot(crypto_df['date'], crypto_df['close'], label='Closing Price', color='black', linestyle='solid')

    positive_date = crypto_df[(crypto_df['sentiment_type'] == 'POSITIVE') & (crypto_df['PercentChange'] > 2)]['date']
    positive_close = crypto_df[(crypto_df['sentiment_type'] == 'POSITIVE') & (crypto_df['PercentChange'] > 2)]['close']
    plt.scatter(positive_date, positive_close, color='blue', label='Positive Sentiment', marker='^', s=100)

    negative_date = crypto_df[(crypto_df['sentiment_type'] == 'NEGATIVE') & (crypto_df['PercentChange'] < 0)]['date']
    negative_close = crypto_df[(crypto_df['sentiment_type'] == 'NEGATIVE') & (crypto_df['PercentChange'] < 0)]['close']
    plt.scatter(negative_date, negative_close, color='red', label='Negative Sentiment', marker='v', s=100)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %d, %Y'))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())

    plt.xlabel('Dates')
    plt.ylabel('Crypto Closing Price in $')
    plt.title('Changes in Price with respect to Market Sentiment')
    plt.grid(True, linestyle='dotted', linewidth=1)
    plt.legend()
    plt.tight_layout()
    plt.show()


def unemployment_data(dataset_path: str, period_one: str, period_two: str) -> pd.DataFrame:
    """

    :param dataset_path: Path to the unemployment dataset
    :param period_one: Optional parameter to filter the dataset from a given range
    :param period_two: Optional parameter to filter the dataset from a given range
    :return: pd.Dataframe: Pandas Dataframe for the given Cryptocurrency
    """

    unemployment_dataset = pd.read_csv(dataset_path)
    unemployment_dataset = unemployment_dataset[(unemployment_dataset['TIME_PERIOD'] >= period_one) &
                                                (unemployment_dataset['TIME_PERIOD'] <= period_two)]
    return unemployment_dataset


def plot_unemployment_trends(crypto_df: pd.DataFrame) -> None:
    """
    This functions plots the unemployment data for the given Cryptocurrency
    :param crypto_df: Dataset to plot
    :return: None
    """
    fig, ax1 = plt.subplots(figsize=(15, 8))
    ax1.plot(crypto_df["Date"], crypto_df["OBS_VALUE"], color="blue", label="Unemployment Rate")
    ax1.set_xlabel("Time Frame")
    ax1.set_ylabel("Unemployment Rate %", color="blue")

    ax2 = ax1.twinx()
    ax2.plot(crypto_df["Date"], crypto_df["Close"], color="red", label="Crypto Price $")
    ax2.set_ylabel("Crypto Price", color="red")

    plt.title("Unemployment Rate % vs Crypto Prices $")
    plt.show()


def combine_inflation_crypto(inflation_file: str, crypto: pd.DataFrame) -> pd.DataFrame:
    """
    This function combines the world inflation dataset with the given Cryptocurrency
    :param inflation_file: Path to the dataset
    :param crypto: Dataframe containing cryptocurrency
    :return: Dataframe containing the combined data
    """

    inflation_data = pd.read_csv(inflation_file, skiprows=16)

    inflation_data = inflation_data[inflation_data['date'] >= '2015-12-31']

    inflation_data['date'] = pd.to_datetime(inflation_data['date'])

    combined_data = pd.merge(inflation_data, crypto, left_on='date', right_on='Date', how='left')
    return combined_data


def plot_inflation_trends(combined_data: pd.DataFrame) -> None:
    """
    This function plots the inflation trends for the given Cryptocurrency
    :param combined_data: The merged_dataset of Inflation and Cryptocurrency
    :return: None
    """
    fig, ax1 = plt.subplots(figsize=(15, 8))

    ax1.plot(combined_data['date'], combined_data[' Inflation Rate (%)'], color='blue', label=' Inflation Rate %')
    ax1.set_xlabel('Date')
    ax1.set_ylabel(' Inflation Rate (%)', color='blue')
    ax1.tick_params('y', colors='blue')

    ax2 = ax1.twinx()

    ax2.plot(combined_data['date'], combined_data['Close'], color='red', label='Close Price')
    ax2.set_ylabel('Close Price', color='red')
    ax2.tick_params('y', colors='red')

    plt.title('Inflation Rate v/s Crypto Price')
    plt.xticks(rotation=45)
    plt.show()


def combine_fed_rates_crypto(federal_rates: str, crypto: pd.DataFrame, period_one: Optional[str] = None,
                             period_two: Optional[str] = None) -> pd.DataFrame:
    """

    This function combines the Federal Interest rates and the given Cryptocurrency, and returns combined Dataframe
    :param federal_rates: The federal interest rate dataset
    :param crypto: Cryptocurrency Dataset
    :param period_one: Optional parameter to filter the dataset from a given range
    :param period_two: Optional parameter to filter the dataset from a given range
    :return: pd.DataFrame : Combined Dataframe
    """
    fedfunds = pd.read_csv(federal_rates)
    fedfunds['DATE'] = pd.to_datetime(fedfunds['DATE'])

    combine_both = pd.merge(fedfunds, crypto, left_on='DATE', right_on="Date", how='left')
    if period_one and period_two:
        combine_both = combine_both[(combine_both['DATE'] >= period_one) & (combine_both['DATE'] <= period_two)]
    if period_one and not period_two:
        combine_both = combine_both[combine_both['DATE'] >= period_one]
    if period_one and not period_one:
        combine_both = combine_both[combine_both['DATE'] <= period_two]
    if combine_both.empty:
        raise ValueError(f"No data found within the specified date range: "
                         f"{period_one} to {period_two}")
    return combine_both


def plot_federal_interest_trends(combined_data: pd.DataFrame) -> None:
    """
    This function plots the Federal Interest Rate trends for the given Cryptocurrency
    :param combined_data: The merged_dataset of Inflation and Cryptocurrency
    :return: None
    """
    fig, ax1 = plt.subplots(figsize=(15, 8))

    ax1.plot(combined_data['Date'], combined_data['FEDFUNDS'], color='blue', label='Federal Interest Rate')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Federal Interest Rate', color='blue')
    ax1.tick_params('y', colors='blue')

    ax2 = ax1.twinx()

    ax2.plot(combined_data['Date'], combined_data['Close'], color='red', label='Close Price')
    ax2.set_ylabel('Close Price', color='red')
    ax2.tick_params('y', colors='red')

    plt.title('Federal Interest v/s Crypto Price')
    plt.xticks(rotation=45)
    plt.show()


def combine_usd_crypto(usd_file: str, crypto: pd.DataFrame, period_one: Optional[str] = None,
                       period_two: Optional[str] = None) -> pd.DataFrame:
    """

    :param usd_file: US Dollar Dataset
    :param crypto: Cryptocurrency Dataset
    :param period_one: Optional parameter to filter the dataset from a given range
    :param period_two: Optional parameter to filter the dataset from a given range
    :return:
    """
    usd = pd.read_csv(usd_file)
    usd['Date'] = pd.to_datetime(usd['Date'])
    usd = usd.sort_values("Date")

    combine_both = pd.merge(usd, crypto, left_on='Date', right_on="Date", how='left')
    if period_one and period_two:
        combine_both = combine_both[(combine_both['Date'] >= period_one) & (combine_both['Date'] <= period_two)]
    if period_one and not period_two:
        combine_both = combine_both[combine_both['Date'] >= period_one]
    if period_one and not period_one:
        combine_both = combine_both[combine_both['Date'] <= period_two]
    if combine_both.empty:
        raise ValueError(f"No data found within the specified date range: "
                         f"{period_one} to {period_two}")
    return combine_both


def plot_usd_trends(combined_data: pd.DataFrame) -> None:
    """
    This function plots the US Dollar trends for the given Cryptocurrency
    :param combined_data: The merged_dataset of Inflation and Cryptocurrency
    :return: None
    """
    fig, ax1 = plt.subplots(figsize=(15, 8))

    ax1.plot(combined_data['Date'], combined_data['Price'], color='blue', label='Federal Interest Rate')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Federal Interest Rate', color='blue')
    ax1.tick_params('y', colors='blue')

    ax2 = ax1.twinx()

    ax2.plot(combined_data['Date'], combined_data['Close'], color='red', label='Close Price')
    ax2.set_ylabel('Close Price', color='red')
    ax2.tick_params('y', colors='red')

    plt.title('Federal Interest v/s Crypto Price')
    plt.xticks(rotation=45)
    plt.show()


if __name__ == "__main__":
    bitcoin = crypto_dataset("./Crypto Dataset/bitcoin_2013-01-01_2024-04-22.csv", period_one='2022-01-01',
                             period_two='2022-02-04')

    print(bitcoin)

    ethereum = crypto_dataset("./Crypto Dataset/ethereum_2016-01-01_2024-04-22.csv")

    print(ethereum.head())
