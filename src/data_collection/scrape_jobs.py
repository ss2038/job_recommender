# src/data_collection/scrape_jobs.py

import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
KEY  = os.getenv("RAPIDAPI_KEY")
HOST = os.getenv("RAPIDAPI_HOST")  # e.g. indeed-scraper-api.p.rapidapi.com

HEADERS = {
    "Content-Type":    "application/json",
    "x-rapidapi-host": HOST,
    "x-rapidapi-key":  KEY
}

def fetch_jobs_for_professions(profs, location="San Francisco"):
    """
    For each profession in `profs`, POST to /api/job, wait for completion
    and then flatten returnvalue.data into a DataFrame.
    """
    all_jobs = []
    url = f"https://{HOST}/api/job"

    for prof in profs:
        payload = {
            "scraper":  {"maxRows": 10},
            "query":    prof,
            "location": location,
            "jobType":  "fulltime",
            "radius":   "50",
            "sort":     "relevance",
            "fromDays": "7",
            "country":  "us"
        }

        # 1) kick off the scraper + wait for it to finish
        resp = requests.post(url, json=payload, headers=HEADERS)
        print("RAW RESPONSE:", resp.text)
        resp.raise_for_status()
        data = resp.json()

        # 2) get the list of jobs
        jobs = data.get("returnvalue", {}).get("data", [])
        if not jobs:
            print(f"⚠️  No jobs returned for profession={prof!r}")
            continue

        # 3) flatten each job record
        for j in jobs:
            # top‐level fields
            title   = j.get("title")
            jobType = j.get("jobType")
            comp    = j.get("companyName")
            comp_url= j.get("companyUrl")
            logo    = j.get("companyLogoUrl")

            # rating nested
            rating = j.get("rating", {}).get("rating")

            # location nested
            loc = j.get("location", {})
            loc_short = loc.get("formattedAddressShort")
            loc_long  = loc.get("formattedAddressLong")

            # pick whichever description you prefer
            descr = j.get("descriptionText") or j.get("descriptionHtml")

            all_jobs.append({
                "profession":              prof,
                "title":                   title,
                "jobType":                 jobType,
                "companyName":             comp,
                "companyUrl":              comp_url,
                "companyLogoUrl":          logo,
                "companyRating":           rating,
                "locationShort":           loc_short,
                "locationLong":            loc_long,
                "description":             descr,
                "datePublished":           j.get("datePublished"),
                "jobUrl":                  j.get("jobUrl"),
                "source":                  j.get("source")
            })

    # 4) write out
    df = pd.DataFrame(all_jobs)
    os.makedirs("data/raw", exist_ok=True)
    df.to_csv("data/raw/all_jobs.csv", index=False)
    return df


if __name__ == "__main__":
    professions = [
        "software developer"
    ]
    df = fetch_jobs_for_professions(professions)
    print(f"\n✅ Scraped {len(df)} jobs and wrote to data/raw/all_jobs.csv")
