import numpy as np
from sentence_transformers import SentenceTransformer

class TwoTowerRecommender:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.encoder = SentenceTransformer(model_name)

    def encode(self, texts: list[str]) -> np.ndarray:
        return self.encoder.encode(texts, convert_to_numpy=True, show_progress_bar=True)

    def rank(self, resume_vec: np.ndarray, job_vecs: np.ndarray) -> np.ndarray:
        # Cosine similarity
        sims = (job_vecs @ resume_vec) / (
            np.linalg.norm(job_vecs, axis=1) * np.linalg.norm(resume_vec)
        )
        return sims
