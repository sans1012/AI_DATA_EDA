# 🤖 AI EDA Copilot

An AI-powered Exploratory Data Analysis (EDA) application that automatically profiles datasets, performs statistical analysis, discovers relationships, and generates business insights using a local Large Language Model (Qwen via Ollama).

---

# Features

* 📊 Automatic Dataset Profiling
* 🧠 AI-based Dataset Understanding
* 📈 Numerical Analysis
* 🏷️ Categorical Analysis
* 🔗 Correlation Analysis
* 📉 Statistical Relationship Discovery
* 💡 AI Executive Summary
* 🎯 Business Metrics & Dimension Detection
* 📑 Interactive Streamlit Dashboard
* 🔒 Fully Local & Open Source (No external API required)

---

# Project Architecture

```text
                    CSV Dataset
                         │
                         ▼
                 DataLoader (utils)
                         │
                         ▼
                ProfilerAgent
                         │
        ┌────────────────┴───────────────┐
        ▼                                ▼
Dataset Profile                 Column Profiler
                                         │
                                         ▼
                               Semantic Reasoner
                                         │
                                         ▼
                                  Planner Agent
                                         │
                                         ▼
                           Dataset Understanding
                         (Business + AI Metadata)

────────────────────────────────────────────────────────

                    Individual Analyzers

        ┌─────────────────────────────────────────────┐
        │                                             │
        ▼                                             ▼

 Overview Analyzer              Data Quality Analyzer

 Numerical Analyzer             Categorical Analyzer

 Correlation Analyzer           Relationship Analyzer

        └─────────────────────────────────────────────┘
                         │
                         ▼

                 Analysis Results
                         │
                         ▼

                Structured Evidence
                         │
                         ▼

                  Insight Agent
               (Qwen via Ollama)
                         │
                         ▼

                 AI Executive Report
                         │
                         ▼

               Visualization Agent
                         │
                         ▼

                Streamlit Frontend
```

---

# Folder Structure

```text
AI-EDA-Copilot/

│
├── agents/
│   ├── planner_agent.py
│   ├── profiler_agent.py
│   ├── report_agent.py
│   └── insight_agent.py
│
├── analyzer/
│   ├── overview.py
│   ├── data_quality.py
│   ├── numerical.py
│   ├── categorical.py
│   ├── correlation.py
│   └── relationships.py
│
├── profiling/
│   ├── column_profiler.py
│   └── semantic_reasoner.py
│
├── core/
│   ├── analysis_result.py
│   ├── evidence.py
│   └── base_analyzer.py
│
├── llm/
│   ├── ollama_client.py
│   ├── parser.py
│   └── prompts.py
│
├── utils/
│   ├── statistics.py
│   ├── helpers.py
│   └── logger.py
│
├── data/
│
├── app.py
│
└── requirements.txt
```

---

# Technology Stack

* Python 3.13+
* Streamlit
* Pandas
* NumPy
* Plotly
* SciPy
* Ollama
* Qwen 2.5 3B
* Scikit-Learn

---

# Installation

## 1. Clone Repository

```bash
git clone https://github.com/<username>/AI-EDA-Copilot.git

cd AI-EDA-Copilot
```

---

## 2. Create Virtual Environment

Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

Linux / Mac

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Install Ollama

Download Ollama from

https://ollama.com/download

---

## 5. Pull Qwen Model

```bash
ollama pull qwen2.5:3b
```

Verify

```bash
ollama list
```

Expected output

```text
qwen2.5:3b
```

---

## 6. Start Ollama

```bash
ollama serve
```

(If Ollama is already running as a background service on your system, you can skip this step.)

---

## 7. Run the Application

```bash
streamlit run app.py
```

The application will be available at

```text
http://localhost:8501
```

---

# Example Workflow

1. Upload a CSV file.
2. Dataset profiling starts automatically.
3. Semantic reasoning identifies business entities.
4. Statistical analyzers run.
5. Structured evidence is generated.
6. Qwen produces AI-driven insights.
7. Interactive visualizations are displayed.

---

# Current Capabilities

* Automatic profiling
* Missing value detection
* Duplicate detection
* Outlier detection
* Distribution analysis
* High-cardinality detection
* Correlation analysis
* Statistical relationship discovery
* Business metric identification
* AI executive summary
* Feature engineering suggestions

---

# Future Enhancements

* Time Series Analysis
* Geospatial Analysis
* Automated ML Readiness Scoring
* Dataset Chat Interface
* PDF Report Export
* Multi-file Comparison
* Dashboard Export

---

# License

MIT License
