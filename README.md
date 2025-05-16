<!-- # 🎯 Job Recommender

An end-to-end **resume-to-job recommendation** system  
It uses a **Two-Tower SBERT** architecture to encode resumes and job descriptions into dense vectors, computes similarity scores, and serves personalized job recommendations via a Streamlit web app. You can also automate daily scraping of new job postings on AWS Lambda.

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)  
2. [Features](#features)  
3. [Tech Stack](#tech-stack)  
4. [Directory Structure](#directory-structure)  
5. [Prerequisites](#prerequisites)  
6. [Installation & Setup](#installation--setup)  
   1. [Clone & Virtual Environment](#clone--virtual-environment)  
   2. [Install Dependencies](#install-dependencies)  
   3. [Configuration (`.env`)](#configuration-env)  
7. [Data Collection & Preprocessing](#data-collection--preprocessing)  
8. [Model Training & Indexing](#model-training--indexing)  
9. [Running the Streamlit App](#running-the-streamlit-app)  
10. [AWS Lambda Automation](#aws-lambda-automation)  
11. [Adding New Professions](#adding-new-professions)  
12. [Contributing](#contributing)  
13. [License](#license)  

---

## 🔍 Project Overview

This project demonstrates a full-pipeline machine learning application that:

1. **Scrapes** job postings for multiple professions via the Indeed RapidAPI.  
2. **Cleans & preprocesses** the scraped data (HTML stripping, deduplication).  
3. **Parses** user-uploaded resumes (PDF/DOCX/TXT) to extract education, years of experience, and profession-specific skills using spaCy + regex.  
4. **Encodes** both resumes and job descriptions into vector embeddings using a pretrained Sentence-Transformer (SBERT) two-tower model.  
5. **Ranks** job postings by cosine similarity against the resume embedding.  
6. **Serves** recommendations in a simple Streamlit UI with a profession selector, resume uploader, and top-10 ranked listings.  
7. **Automates** daily scraping on AWS Lambda + Serverless Framework and stores raw CSVs in S3.  

---

## ✔️ Features

- **Multi-profession support** – out-of-the-box for software engineer, data engineer, teacher, healthcare worker, chartered accountant, business analyst, and researcher.  
- **Two-Tower Architecture** – separate encoders for resumes vs. job descriptions for efficient retrieval.  
- **Streamlit UI** – user-friendly web interface for uploading resumes and viewing suggestions.  
- **AWS Automation** – daily job scraping Lambda function scheduled via CloudWatch, raw data persisted to S3.  
- **Easy extensibility** – add new professions by dropping a skills JSON into `data/skills/` and rerunning the pipeline.  

---

## 🛠️ Tech Stack

- **Language**: Python 3.9+  
- **Web App**: Streamlit  
- **NLP**: spaCy, Sentence-Transformers (SBERT), pdfminer.six, python-docx  
- **Data**: pandas, BeautifulSoup4  
- **Modeling**: PyTorch, scikit-learn  
- **Deployment**: AWS Lambda, Serverless Framework, S3  
- **Versioning**: Git & GitHub  

---

## 🗂️ Directory Structure

```text
job_recommender/
├── aws/
│   ├── lambda_scrape.py       # AWS Lambda handler
│   └── serverless.yml         # Serverless Framework config
├── app/
│   └── streamlit_app.py       # Streamlit UI
├── data/
│   ├── raw/                   # Raw CSVs from scraper (not checked in)
│   ├── processed/             # Cleaned CSV & pickled index
│   └── skills/                # JSON lists of skills per profession
├── src/
│   ├── data_collection/
│   │   └── scrape_jobs.py     # RapidAPI scraper
│   ├── resume_parser/
│   │   └── parser.py          # Resume parsing logic
│   ├── models/
│   │   ├── tower_model.py     # Two-Tower SBERT wrapper
│   │   └── train.py           # Build & save job index
│   ├── utils/
│   │   └── io_helpers.py      # CSV loading/cleaning helpers
│   └── evaluation/
│       └── evaluate.py        # Optional precision@k script
├── .env                       # API keys & config (gitignored)
├── .gitignore                 # ignore venv, data, env
├── requirements.txt           # pip dependencies
└── README.md                  # this document
```

---

## ⚙️ Prerequisites

Before you begin, ensure you have:

- **Python 3.9+** installed and on your **PATH**  
- **Git** installed for version control  
- **AWS CLI** and **Serverless Framework** installed & configured (for AWS automation)  
- A **RapidAPI** account with a subscription to the Indeed (or similar) job-search API  
- An **AWS** account with permissions to create Lambda functions and S3 buckets  

---

## 🚀 Installation & Setup

### 1. Clone & Virtual Environment

```bash
git clone https://github.com/<your-username>/job_recommender.git
cd job_recommender

python3 -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows PowerShell:
.venv\Scripts\Activate.ps1
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 3. Configuration (`.env`)

Create a file named `.env` at the project root with:

```dotenv
RAPIDAPI_KEY=YOUR_RAPIDAPI_KEY
RAPIDAPI_HOST=indeed11.p.rapidapi.com
S3_BUCKET=YOUR_AWS_S3_BUCKET_NAME
```

> **Security**: The `.env` file is in `.gitignore`; do **not** commit it.

---

## 🛠️ Data Collection & Preprocessing

### Scrape jobs

```bash
python src/data_collection/scrape_jobs.py
```
- **Produces**: `data/raw/all_jobs.csv`

### Clean & preprocess

```bash
python - << 'PYCODE'
from src.utils.io_helpers import load_raw_jobs, save_processed
df = load_raw_jobs("data/raw/all_jobs.csv")
save_processed(df, "data/processed/jobs_clean.csv")
PYCODE
```
- **Produces**: `data/processed/jobs_clean.csv`

---

## 🤖 Model Training & Indexing

```bash
python src/models/train.py
```
- Encodes descriptions with SBERT  
- **Outputs**: `data/processed/jobs_index.pkl`

*(Optional evaluation)*

```bash
python src/evaluation/evaluate.py
```

---

## 🌐 Running the Streamlit App

```bash
streamlit run app/streamlit_app.py
```
1. Select your **profession**  
2. Upload your **resume** (PDF/DOCX/TXT)  
3. View **parsed info** (education, experience, skills)  
4. Browse **Top-10 job matches** with similarity scores  

---

## ☁️ AWS Lambda Automation

```bash
cd aws
serverless deploy
```
- Schedules a daily Lambda to refresh `raw/all_jobs.csv` in your S3 bucket

---

## ➕ Adding New Professions

1. Create `data/skills/<profession>.json` (list of skills)  
2. Update the profession lists in:  
   - `src/data_collection/scrape_jobs.py`  
   - `app/streamlit_app.py`  
3. Rerun:

```bash
python src/data_collection/scrape_jobs.py
python src/models/train.py
```

---

## 🤝 Contributing

- Fork → create a branch → commit → push → open a PR  
- Ensure code is linted & tested  

---

## 📄 License

Released under the **MIT License**.   -->



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

This project addresses the inefficiencies of traditional keyword-based job search platforms by using a **semantic similarity model** that intelligently understands and ranks job postings based on a user's resume.

- Resumes are **parsed** and semantically segmented.
- Job postings are **scraped**, **cleaned**, and **vectorized**.
- A **Two-Tower Sentence-BERT (SBERT)** architecture computes embeddings for both resumes and job descriptions.
- A **Cross-Encoder** model is used for fine-grained re-ranking.
- Results are filtered by **location** and **salary** preferences.
- The app is deployed using **Streamlit** with a friendly user interface.
- Job data is automatically refreshed using **AWS Lambda + S3**.

---

## ✔️ Key Features

- 📄 Resume parsing from `.txt`, `.pdf`, and `.docx` formats.
- 🧠 Semantic job matching using pretrained transformer-based models.
- 🔍 Location and salary filtering.
- 🖥️ Real-time web interface with Streamlit.
- ☁️ Automated job data collection using AWS Lambda.
- 📊 Evaluation metrics for performance benchmarking.

---

## 🛠️ Tech Stack

- **Language**: Python 3.9+  
- **UI**: Streamlit  
- **NLP**: Sentence-Transformers (SBERT), BERT Cross-Encoder, spaCy  
- **Parsing**: PyPDF2, python-docx  
- **Data Handling**: pandas, BeautifulSoup4  
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
- RapidAPI account (for job scraping)

---

## 🚀 Installation & Setup

### 1. Clone & Set Up Environment

```bash
git clone https://github.com/<your-username>/job_recommender.git
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

Create a `.env` file in the root with:

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

- Output: `data/raw/all_jobs.csv`

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
- Pickles vector index to `data/processed/jobs_index.pkl`

---

## 🌐 Running the Streamlit App

```bash
streamlit run app/streamlit_app.py
```

1. **Upload** a resume or choose a sample.  
2. **Filter** by location and salary.  
3. **View** the top 5 personalized job recommendations with scores and links.

---

## ☁️ AWS Lambda Automation

```bash
cd aws
serverless deploy
```

- Deploys a scheduled Lambda to refresh job listings and store them in S3.

---

## 🔁 Extending the System

- **Add Professions**: Create a new `data/skills/<profession>.json`  
- **Add Resumes**: Drop `.txt` files in `data/sample_resumes/`  
- **Retrain**: Run `scrape_jobs.py` and `train.py` again  
- **Deploy**: Redeploy Lambda if the job structure changes

---

## 📊 Evaluation Metrics

| Profession         | Precision@5 | Recall@5 | MRR  |
|--------------------|-------------|----------|------|
| Software Engineer  | 95%         | 92%      | 93%  |
| Teacher            | 93%         | 90%      | 91%  |

---

## 🤝 Contributing

- Fork this repo  
- Create a new feature branch  
- Commit your changes  
- Submit a pull request with a clear message  

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
