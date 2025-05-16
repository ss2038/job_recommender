import pandas as pd
from bs4 import BeautifulSoup

def load_raw_jobs(path="data/raw/all_jobs.csv"):
    df = pd.read_csv(path)
    # Drop exact duplicates
    df = df.drop_duplicates(subset=["profession","title","company","description"])
    # Strip HTML from descriptions
    df["description"] = df["description"] \
        .apply(lambda x: BeautifulSoup(x, "html.parser").get_text())
    # Normalize whitespace
    df["description"] = df["description"] \
        .str.replace(r"\s+", " ", regex=True).str.strip()
    return df

def save_processed(df, path="data/processed/jobs_clean.csv"):
    df.to_csv(path, index=False)
