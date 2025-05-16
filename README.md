
# 🎯 Intelligent Job Recommender

An end-to-end **resume-to-job recommendation** system that leverages a **Two-Tower SBERT** architecture and **Cross-Encoder re-ranking** to deliver highly personalized job matches. It supports structured resume parsing, fine-grained filtering, real-time recommendation, and automated job scraping through a fully integrated pipeline.

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)  
2. [Key Features](#key-features)  
3. [Tech Stack](#tech-stack)  
4. [Directory Structure](#directory-structure)  
5. [Prerequisites](#prerequisites)  
6. [Installation & Setup](#installation--setup)  
7. [Data Collection & Preprocessing](#data-collection--preprocessing)  
8. [Model Training & Indexing](#model-training--indexing)  
9. [Running the Streamlit App](#running-the-streamlit-app)  
10. [AWS Lambda Automation](#aws-lambda-automation)  
11. [Extending the System](#extending-the-system)  
12. [Evaluation Metrics](#evaluation-metrics)  
13. [Contributing](#contributing)  
14. [License](#license)

---

## 🔍 Project Overview

This project solves the problem of resume-job mismatch in traditional search engines by applying **semantic retrieval** techniques. Rather than relying on exact keyword matching, our system semantically understands the content of resumes and job descriptions using deep learning-based embeddings.

- Resumes are **parsed** and structured using NLP.
- Job descriptions are **scraped**, **cleaned**, and **vectorized**.
- A **Two-Tower SBERT** model encodes resumes and jobs separately for scalable retrieval.
- A **Cross-Encoder** further reranks jobs with joint representation learning.
- Users can apply **filters for location and salary**, improving personalization.
- The platform is accessible through a **Streamlit UI**.
- Job listings are **automatically updated using AWS Lambda** and stored in S3.

---

## ✔️ Key Features

- 📄 Supports `.txt`, `.pdf`, and `.docx` resume parsing.
- 🧠 Semantic matching using pretrained transformer models (SBERT + Cross-Encoder).
- 🔍 Filter jobs by **location** (city/state) and **salary** (value/range).
- 🖥️ Streamlit-powered UI with sample profile selector and upload interface.
- ☁️ Serverless job updates using AWS Lambda and RapidAPI.
- 📊 Built-in evaluation module for model benchmarking.

---

## 🛠️ Tech Stack

- **Language**: Python 3.9+  
- **UI**: Streamlit  
- **NLP**: Sentence-Transformers (SBERT), BERT Cross-Encoder, spaCy  
- **Parsing**: PyPDF2, python-docx  
- **Data Handling**: pandas, BeautifulSoup4, rapidfuzz  
- **Deployment**: AWS Lambda, Serverless Framework, S3  
- **Version Control**: Git & GitHub  

---

## 🗂️ Directory Structure

```text
job_recommender/
├── app/                          # Streamlit UI
│   └── streamlit_app.py
├── data/
│   ├── raw/                      # Scraped CSVs
│   ├── processed/                # Embeddings, cleaned data
│   └── skills/                   # Skills by profession (JSON)
├── src/
│   ├── resume_parser/            # Resume extraction
│   │   └── parser.py
│   ├── data_collection/          # Job scraper
│   │   └── scrape_jobs.py
│   ├── models/                   # Two-Tower and Cross-Encoder
│   │   ├── tower_model.py
│   │   └── train.py
│   ├── utils/                    # Helpers
│   │   └── io_helpers.py
│   └── evaluation/               # Evaluation metrics
│       └── evaluate.py
├── aws/                          # Serverless deployment
│   ├── lambda_scrape.py
│   └── serverless.yml
├── .env
├── requirements.txt
└── README.md
```

---

## ⚙️ Prerequisites

- Python 3.9+  
- pip  
- Git  
- AWS CLI & Serverless Framework  
- RapidAPI account with access to job search APIs  

---

## 🚀 Installation & Setup

### 1. Clone & Set Up Environment

```bash
git clone https://github.com/ss2038/job_recommender.git
cd job_recommender
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 3. Environment Variables

Create a `.env` file at the root:

```env
RAPIDAPI_KEY=your_key
RAPIDAPI_HOST=indeed-scraper-api.p.rapidapi.com
S3_BUCKET=your-bucket-name
```

---

## 🛠️ Data Collection & Preprocessing

### Scrape Job Listings

```bash
python src/data_collection/scrape_jobs.py
```

Stores raw job listings in `data/raw/all_jobs.csv`.

### Clean & Normalize

```bash
python - << EOF
from src.utils.io_helpers import load_raw_jobs, save_processed
df = load_raw_jobs("data/raw/all_jobs.csv")
save_processed(df, "data/processed/jobs_clean.csv")
EOF
```

---

## 🤖 Model Training & Indexing

```bash
python src/models/train.py
```

- Encodes job descriptions using SBERT  
- Builds `jobs_index.pkl` for fast cosine similarity-based lookup  
- Can optionally re-rank results using Cross-Encoder (BERT)

---

## 🌐 Running the Streamlit App

```bash
streamlit run app/streamlit_app.py
```

1. Select a profession or upload a resume  
2. Apply filters for **location** and **salary**  
3. View Top-5 job matches with similarity scores and application links

---

## ☁️ AWS Lambda Automation

```bash
cd aws
serverless deploy
```

- Schedules a daily job to scrape new postings and save them to S3  
- Keeps `data/raw/all_jobs.csv` continuously updated

---

## 🔁 Extending the System

- **Add Professions**: Drop `data/skills/<profession>.json`  
- **Add Sample Resumes**: Place `.txt` files in `data/sample_resumes/`  
- **Retrain Index**: Run scraper and `train.py` again  
- **Add Filters**: Update UI logic in `streamlit_app.py`

---

## 📊 Evaluation Metrics

| Profession            | Precision@5 | Recall@5 | MRR  |
|-----------------------|-------------|----------|------|
| Software Engineer     | 95%         | 92%      | 93%  |
| Teacher               | 93%         | 90%      | 91%  |
| Healthcare Worker     | 90%         | 88%      | 89%  |
| Business Analyst      | 91%         | 87%      | 90%  |
| Data Analyst          | 94%         | 91%      | 92%  |
| Chartered Accountant  | 89%         | 86%      | 87%  |
| Researcher            | 92%         | 89%      | 90%  |

---

## 🤝 Contributing

- Fork this repo  
- Create a new feature branch  
- Add your code and test it  
- Submit a pull request with a clear explanation  

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
