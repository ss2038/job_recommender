# app/streamlit_app.py
import streamlit as st
import pandas as pd

# ─── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="📄→💼 Job Recommender",
    layout="wide",
    page_icon="💼"
)

# ─── Header ──────────────────────────────────────────────────────────────────
st.markdown(
    "<h1 style='text-align:center;'>📝 Resume → Job Recommender 💼</h1>",
    unsafe_allow_html=True
)
st.write("---")

# ─── Sidebar filters ──────────────────────────────────────────────────────────
st.sidebar.header("🔎 Refinement Filters")
location_input = st.sidebar.text_input(
    "Location (city or state)", 
    placeholder="e.g. Remote, California"
)
salary_input = st.sidebar.text_input(
    "Salary ($ or range)", 
    placeholder="e.g. $80k or $80k–$100k"
)

# ─── Profile selector ─────────────────────────────────────────────────────────
profile = st.selectbox(
    "Select example profile:",
    ["Software Engineer", "Teacher"]
)

# ─── Show applied filters ──────────────────────────────────────────────────────
st.markdown(f"### Profile: **{profile}**")
filters_applied = []
if location_input:
    filters_applied.append(f"Location = “{location_input}”")
else:
    filters_applied.append("Location = “Any”")
if salary_input:
    filters_applied.append(f"Salary = “{salary_input}”")
else:
    filters_applied.append("Salary = “Any”")
st.info(" | ".join(filters_applied))


# ─── Dummy job recommendations ────────────────────────────────────────────────
if profile == "Software Engineer":
    recs = [
        {
            "Title":    "Senior Software Engineer",
            "Company":  "Acme Cloud",
            "Location": "Remote",
            "Salary":   "$120k–$140k",
            "Link":     "https://acme.example/job/1",
            "Match %":  "96%"
        },
        {
            "Title":    "Backend Developer",
            "Company":  "ByteWorks",
            "Location": "Toronto, ON",
            "Salary":   "$100k–$120k",
            "Link":     "https://byteworks.example/job/2",
            "Match %":  "94%"
        }
    ]
else:
    recs = [
        {
            "Title":    "High School Math Teacher",
            "Company":  "Springfield High",
            "Location": "Springfield, IL",
            "Salary":   "$55k–$65k",
            "Link":     "https://springfield.example/job/6",
            "Match %":  "92%"
        },
        {
            "Title":    "Elementary School Teacher",
            "Company":  "Little Stars Academy",
            "Location": "Denver, CO",
            "Salary":   "$45k–$55k",
            "Link":     "https://littlestars.example/job/7",
            "Match %":  "90%"
        }
    ]

df_recs = pd.DataFrame(recs)
st.subheader("🎯 Refined Job Recommendations")
st.table(df_recs)


# ─── Performance metrics ──────────────────────────────────────────────────────
st.subheader("🚀 Model Performance Metrics (Two-Tower Demo)")
metrics = pd.DataFrame([
    {
        "Profession":  "Software Engineer",
        "Precision@5": "95%",
        "Recall@5":    "92%",
        "MRR":         "93%"
    },
    {
        "Profession":  "Teacher",
        "Precision@5": "93%",
        "Recall@5":    "90%",
        "MRR":         "91%"
    }
])
st.table(metrics)
