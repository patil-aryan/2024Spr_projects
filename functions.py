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


>>> c = crypto_dataset("./Crypto Dataset/bitcoin_2013-01-01_2024-04-22.csv", period_one='2022-01-01',period_two='2022-01-04')
>>> print(c.shape)
(4, 7)

>>> crypto_dataset("./Crypto Dataset/bitcoin_2013-01-01_2024-04-22.csv", period_one='2025-01-01',period_two='2025-01-04')
Traceback (most recent call last):
...
ValueError: No data found within the specified date range: 2025-01-01 to 2025-01-04

>>> crypto_dataset("./Crypto Dataset/bitcoin_2013-01-01_2024-04-22.csv", period_one='2022-01-01',period_two='2022-01-04')
... # doctest: +NORMALIZE_WHITESPACE
... # doctest: +ELLIPSIS
          Date          Open  ...        Volume    Market Cap
841 2022-01-01  46198.203781  ...  9.941362e+10  8.911811e+11
840 2022-01-02  47722.939700  ...  7.453585e+10  8.936273e+11
839 2022-01-03  47311.946700  ...  1.159970e+11  8.857233e+11
838 2022-01-04  46412.079600  ...  7.467415e+10  8.784294e+11
<BLANKLINE>
[4 rows x 7 columns]

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

>>> c = pd.read_csv('TwitterData/btc_selected_with_sentiment_2023_01_02_2023_06_12.csv')
>>> positive_sentiment = c[(c['sentiment_type'] == 'POSITIVE') &  (c['changes']  == 'positive')]
>>> len(positive_sentiment)
74
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

>>> btc = crypto_dataset("./Crypto Dataset/bitcoin_2013-01-01_2024-04-22.csv")
>>> combine_inflation_crypto('EconomicFactors/world-inflation-rate-cpi.csv', btc)
... # doctest: +NORMALIZE_WHITESPACE
... # doctest: +ELLIPSIS
        date   Inflation Rate (%)  ...        Volume    Market Cap
0 2015-12-31               1.4439  ...  4.341306e+07  6.390443e+09
1 2016-12-31               1.6055  ...  1.335818e+08  1.534369e+10
2 2017-12-31               2.2543  ...  1.181868e+10  2.296027e+11
3 2018-12-31               2.4504  ...  3.648742e+09  6.640670e+10
4 2019-12-31               2.2061  ...  1.923169e+10  1.306356e+11
5 2020-12-31               1.9369  ...  7.927135e+10  5.363150e+11
6 2021-12-31               3.4669  ...  7.810027e+10  8.945653e+11
7 2022-12-31               7.9676  ...  3.406534e+10  3.183907e+11
<BLANKLINE>
[8 rows x 11 columns]

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

>>> btc = crypto_dataset("./Crypto Dataset/bitcoin_2013-01-01_2024-04-22.csv")
>>> combine_fed_rates_crypto('EconomicFactors/FEDFUNDS.csv', btc, period_one = '2025-01-01', period_two= '2025-01-04')
Traceback (most recent call last):
  ...
ValueError: No data found within the specified date range: 2025-01-01 to 2025-01-04

>>> combine_fed_rates_crypto('EconomicFactors/FEDFUNDS.csv', btc, period_one = '2018-01-01', period_two= '2018-12-31')
... # doctest: +NORMALIZE_WHITESPACE
... # doctest: +ELLIPSIS
        DATE  FEDFUNDS       Date  ...         Close        Volume    Market Cap
24 2018-01-01      1.41 2018-01-01  ...  13577.188555  9.527935e+09  2.292229e+11
25 2018-02-01      1.42 2018-02-01  ...   9171.249369  4.557095e+09  1.620348e+11
26 2018-03-01      1.51 2018-03-01  ...  10929.765497  3.441035e+09  1.796653e+11
27 2018-04-01      1.69 2018-04-01  ...   6830.630577  3.598865e+09  1.162929e+11
28 2018-05-01      1.70 2018-05-01  ...   9096.810022  6.156448e+09  1.532087e+11
29 2018-06-01      1.82 2018-06-01  ...   7525.473797  3.534811e+09  1.277794e+11
30 2018-07-01      1.91 2018-07-01  ...   6364.401842  3.508360e+09  1.090069e+11
31 2018-08-01      1.91 2018-08-01  ...   7596.721803  4.823441e+09  1.302081e+11
32 2018-09-01      1.95 2018-09-01  ...   7193.248733  3.736417e+09  1.224339e+11
33 2018-10-01      2.19 2018-10-01  ...   6596.018098  3.103182e+09  1.142173e+11
34 2018-11-01      2.20 2018-11-01  ...   6368.306136  3.290644e+09  1.099704e+11
35 2018-12-01      2.27 2018-12-01  ...   4208.469723  3.729733e+09  7.190973e+10
<BLANKLINE>
[12 rows x 9 columns]

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
    :return: Dataframe with combined US Dollar and Crypto Dataset

>>> btc = crypto_dataset("./Crypto Dataset/bitcoin_2013-01-01_2024-04-22.csv")
>>> combine_usd_crypto('EconomicFactors/US Dollar Index Historical Data.csv', btc, period_one = '2025-01-01', period_two= '2025-01-04')
Traceback (most recent call last):
...
ValueError: No data found within the specified date range: 2025-01-01 to 2025-01-04

>>> combine_usd_crypto('EconomicFactors/US Dollar Index Historical Data.csv', btc, period_one = '2024-01-01', period_two= '2024-01-04')
... # doctest: +NORMALIZE_WHITESPACE
... # doctest: +ELLIPSIS
            Date   Price  Open_x  ...     Close        Volume    Market Cap
2087 2024-01-02  102.20  101.42  ...  44957.63  4.663793e+10  8.859783e+11
2088 2024-01-03  102.49  102.15  ...  42818.03  9.930917e+10  8.601401e+11
2089 2024-01-04  102.42  102.46  ...  44188.15  1.638240e+11  8.514089e+11
<BLANKLINE>
[3 rows x 13 columns]
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
    ax1.set_ylabel('USD', color='blue')
    ax1.tick_params('y', colors='blue')

    ax2 = ax1.twinx()

    ax2.plot(combined_data['Date'], combined_data['Close'], color='red', label='Close Price')
    ax2.set_ylabel('Close Price', color='red')
    ax2.tick_params('y', colors='red')

    plt.title('USD v/s Crypto Price')
    plt.xticks(rotation=45)
    plt.show()


if __name__ == "__main__":
    bitcoin = crypto_dataset("./Crypto Dataset/bitcoin_2013-01-01_2024-04-22.csv", period_one='2022-01-01',
                             period_two='2022-02-04')

    print(bitcoin.head())

    ethereum = crypto_dataset("./Crypto Dataset/ethereum_2016-01-01_2024-04-22.csv", period_one='2022-01-01',
                              period_two='2022-02-04')

    print(ethereum.head())
