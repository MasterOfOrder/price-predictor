import pandas as pd


def prepare_training_data(raw_scraped_data: list):
    if raw_scraped_data is None or len(raw_scraped_data) == 0:
        return None, None, None

    df = pd.DataFrame(raw_scraped_data)
    df['Date_Parsed'] = pd.to_datetime(df['date'])
    df['Day_Index'] = (df['Date_Parsed'] - df['Date_Parsed'].min()).dt.days

    X = df[['Day_Index']].values
    y = df['price'].values

    return X, y, df
