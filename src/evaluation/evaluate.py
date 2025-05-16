from sklearn.metrics import precision_score

def precision_at_k(true_ids: list[str], recommended_ids: list[str], k: int = 10) -> float:
    hits = [1 if job in true_ids else 0 for job in recommended_ids[:k]]
    return sum(hits) / k

if __name__ == "__main__":
    # Example usage—replace with your labeled test set
    true = ["job1","job2","job3"]
    recs = ["job2","job4","job1","job5"]
    print("P@3:", precision_at_k(true, recs, k=3))
