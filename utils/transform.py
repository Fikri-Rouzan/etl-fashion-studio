import logging
import pandas as pd

logger = logging.getLogger(__name__)


def transform_data(df):
    logger.info("Starting the transformation process...")

    try:
        if df.empty:
            logger.info("Data is empty, transformation process is skipped.")
            return df

        df = df[df["Title"] != "Unknown Product"].copy()

        def clean_price(value):
            if pd.isna(value) or "Price Unavailable" in str(value):
                return None
            try:
                return float(str(value).replace("$", "").strip()) * 16000
            except:
                return None

        def clean_rating(value):
            if pd.isna(value) or "Invalid" in str(value):
                return None
            try:
                parts = str(value).split()
                for part in parts:
                    try:
                        return float(part)
                    except:
                        continue
                return None
            except:
                return None

        def clean_colors(value):
            if pd.isna(value):
                return None
            try:
                return int(str(value).replace("Colors", "").strip())
            except:
                return None

        def clean_size(value):
            if pd.isna(value):
                return None
            try:
                return str(value).replace("Size:", "").strip()
            except:
                return None

        def clean_gender(value):
            if pd.isna(value):
                return None
            try:
                return str(value).replace("Gender:", "").strip()
            except:
                return None

        df["Price"] = df["Price"].apply(clean_price)
        df["Rating"] = df["Rating"].apply(clean_rating)
        df["Colors"] = df["Colors"].apply(clean_colors)
        df["Size"] = df["Size"].apply(clean_size)
        df["Gender"] = df["Gender"].apply(clean_gender)

        initial_len = len(df)
        df = df.dropna()
        df = df.drop_duplicates()

        df["Price"] = df["Price"].astype("float64")
        df["Rating"] = df["Rating"].astype("float64")
        df["Colors"] = df["Colors"].astype("int64")
        df["timestamp"] = pd.to_datetime(df["timestamp"])

        logger.info(
            f"Transformation complete. Clean data: {len(df)} (Data reduced by {initial_len - len(df)})"
        )
        return df
    except Exception as e:
        logger.error(f"An error occurred in the transformation process: {e}")
        return pd.DataFrame()
