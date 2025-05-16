import pickle
from src.utils.io_helpers import load_raw_jobs, save_processed
from src.models.tower_model import TwoTowerRecommender

def build_job_index():
    # 1. Load & clean
    df = load_raw_jobs()
    save_processed(df)
    # 2. Encode descriptions
    model      = TwoTowerRecommender()
    embeddings = model.encode(df["description"].tolist())
    df["job_embedding"] = list(embeddings)
    # 3. Persist
    with open("data/processed/jobs_index.pkl", "wb") as f:
        pickle.dump(df, f)

if __name__ == "__main__":
    build_job_index()
    print("✅ Job index built and saved to data/processed/jobs_index.pkl")
