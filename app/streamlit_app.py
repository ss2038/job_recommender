# import streamlit as st
# import pickle
# import numpy as np
# from src.resume_parser.parser import read_resume, parse_resume
# from src.models.tower_model import TwoTowerRecommender
# from src.resume_parser.parser import parse_resume_text


# st.set_page_config(page_title="Job Recommender")
# st.title("📄 Resume → Job Recommender")

# # 1. Profession selector
# profession = st.sidebar.selectbox(
#     "Select your profession",
#     [
#       "software engineer","data engineer","teacher",
#       "healthcare worker","chartered accountant",
#       "business analyst","researcher"
#     ]
# )

# # 2. Resume upload
# uploaded = st.file_uploader("Upload your resume", type=["pdf","docx","txt"])
# if uploaded:
#     raw_text = read_resume(uploaded.read(), uploaded.type.split("/")[-1])
#     info     = parse_resume(raw_text, profession)
#     st.sidebar.subheader("Parsed Resume Info")
#     st.sidebar.write(info)

#     # 3. Load job index & filter
#     with open("data/processed/jobs_index.pkl","rb") as f:
#         jobs_df = pickle.load(f)
#     subset = jobs_df[jobs_df["profession"] == profession]
#     embs   = np.vstack(subset["job_embedding"].to_list())

#     # 4. Rank
#     model = TwoTowerRecommender()
#     rvec  = model.encode([raw_text])[0]
#     sims  = model.rank(rvec, embs)
#     top10 = np.argsort(sims)[::-1][:10]

#     # 5. Display
#     st.subheader("Top 10 Job Matches")
#     for idx in top10:
#         job = subset.iloc[idx]
#         st.markdown(f"**{job.title}** at *{job.company}*  —  {job.location}")
#         st.write(job.description[:200] + "…")
#         st.caption(f"Score: {sims[idx]:.3f}")
#         st.write("---")


# app/streamlit_app.py
# ────────────────────────────────────────────────

# import os
# import sys

# # ────────────────────────────────────────────────
# # 1) Make the project root importable so "src/..." works
# #    (this must come before any `from src...` lines)
# # ────────────────────────────────────────────────
# # __file__ is ".../job_recommender/app/streamlit_app.py"
# PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# if PROJECT_ROOT not in sys.path:
#     sys.path.insert(0, PROJECT_ROOT)

# # ────────────────────────────────────────────────
# # 2) Now we can safely import from src/
# # ────────────────────────────────────────────────
# import streamlit as st
# import pandas as pd
# from src.resume_parser.parser import parse_resume_text
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

# # ────────────────────────────────────────────────
# # 3) Cache loader for your dummy job data
# # ────────────────────────────────────────────────
# @st.cache_data
# def load_job_data(path: str = "data/raw/jobs_dummy.csv") -> pd.DataFrame:
#     return pd.read_csv(path)


# # ────────────────────────────────────────────────
# # 4) Simple TF-IDF + cosine recommender
# # ────────────────────────────────────────────────
# def recommend_jobs(
#     resume_text: str,
#     jobs_df: pd.DataFrame,
#     top_n: int = 5
# ) -> pd.DataFrame:
#     corpus = [resume_text] + jobs_df["description"].fillna("").tolist()
#     vect = TfidfVectorizer(stop_words="english")
#     tfidf_matrix = vect.fit_transform(corpus)

#     resume_vec = tfidf_matrix[0]
#     job_vecs   = tfidf_matrix[1:]
#     scores     = cosine_similarity(resume_vec, job_vecs)[0]

#     out = jobs_df.copy()
#     out["score"] = scores
#     return out.nlargest(top_n, "score")[["title","company","location","jobUrl","score"]]


# # ────────────────────────────────────────────────
# # 5) Streamlit UI
# # ────────────────────────────────────────────────
# def main():
#     st.set_page_config(page_title="📄→💼 Job Recommender", layout="wide")
#     st.title("📝 Resume → Job Recommender 💼")
#     st.markdown(
#         "Upload a **.txt** resume to see your top 5 matches, or leave it blank "
#         "to use the provided sample."
#     )

#     uploaded = st.file_uploader("Upload your resume (.txt only)", type=["txt"])
#     if uploaded:
#         tmp = ".__uploaded_resume.txt"
#         with open(tmp, "wb") as f:
#             f.write(uploaded.getvalue())
#         resume_text = parse_resume_text(tmp)
#         os.remove(tmp)
#     else:
#         st.info("No upload detected — using `sample_resume.txt`")
#         resume_text = parse_resume_text("sample_resume.txt")

#     st.subheader("Extracted Resume Text")
#     st.write(resume_text)

#     st.subheader("Job Recommendations")
#     jobs_df = load_job_data()
#     st.write(f"Loaded **{len(jobs_df)}** jobs from `jobs_dummy.csv`.")

#     recs = recommend_jobs(resume_text, jobs_df, top_n=5)
#     recs["score"] = recs["score"].map(lambda x: f"{x:.2f}")
#     st.table(recs)


# if __name__ == "__main__":
#     main()


import os, sys

# 1) Make `src/` importable
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
import pandas as pd
from src.resume_parser.parser import parse_resume_text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# — cache your job dataset —
@st.cache_data
def load_job_data(path="data/raw/jobs_dummy.csv") -> pd.DataFrame:
    return pd.read_csv(path)

def recommend_jobs(resume_text, jobs_df, top_n=5):
    corpus = [resume_text] + jobs_df["description"].fillna("").tolist()
    vect = TfidfVectorizer(stop_words="english")
    tfidf = vect.fit_transform(corpus)
    sims = cosine_similarity(tfidf[0], tfidf[1:])[0]
    df = jobs_df.copy()
    df["score"] = sims
    return df.nlargest(top_n, "score")[["title","company","location","jobUrl","score"]]

def main():
    st.set_page_config("📄→💼 Job Recommender", layout="wide")
    st.title("📝 Intelligent Job Recommender 💼")

    # 2) Let user upload OR pick from samples
    uploaded = st.file_uploader("Upload .txt resume", type="txt")
    sample_files = {
        "Software Engineer": "sample_resume_software.txt",
        "Teacher":              "sample_resume_teacher.txt",
        "Healthcare Nurse":     "sample_resume_healthcare.txt",
        "Data Scientist":       "sample_resume_data_science.txt",
        "Marketing Specialist": "sample_resume_marketing.txt",
    }

    if uploaded:
        # write to temp and parse
        tmp = "temp_resume.txt"
        with open(tmp, "wb") as f:
            f.write(uploaded.getvalue())
        resume_text = parse_resume_text(tmp)
        os.remove(tmp)
    else:
        choice = st.selectbox("Or pick a sample resume:", list(sample_files.keys()))
        st.info(f"Using **{choice}** sample")
        resume_text = parse_resume_text(sample_files[choice])

    # show extracted
    st.subheader("Extracted Resume Text")
    st.write(resume_text)

    # recommendations
    st.subheader("Job Recommendations")
    jobs = load_job_data()
    st.write(f"Loaded **{len(jobs)}** jobs from `jobs_dummy.csv`.")
    recs = recommend_jobs(resume_text, jobs, top_n=5)
    recs["score"] = recs["score"].map(lambda x: f"{x:.2f}")
    st.table(recs)

if __name__ == "__main__":
    main()
