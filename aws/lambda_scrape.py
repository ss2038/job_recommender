import os
import boto3
import pandas as pd
from src.data_collection.scrape_jobs import fetch_jobs_for_professions
from dotenv import load_dotenv

load_dotenv()
S3     = boto3.client("s3")
BUCKET = os.getenv("S3_BUCKET")

def handler(event, context):
    professions = [
      "software engineer","data engineer","teacher",
      "healthcare worker","chartered accountant",
      "business analyst","researcher"
    ]
    df = fetch_jobs_for_professions(professions)
    csv = df.to_csv(index=False).encode()
    S3.put_object(Bucket=BUCKET, Key="raw/all_jobs.csv", Body=csv)
    return {"statusCode":200, "body":f"Scraped {len(df)} jobs."}
