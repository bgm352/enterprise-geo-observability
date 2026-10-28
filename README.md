# Enterprise GEO Observability Engine

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://geosearch-7ps4jbhmptqetyyefnavtu.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

An enterprise-grade framework for **Generative Engine Optimization (GEO)** and AI Search Observability. As discovery shifts from traditional SERPs to generative answer engines (Perplexity, SearchGPT, Google AI Overviews, Gemini, Claude), traditional rank tracking falls short. This repository provides programmatic observability into **AI Share of Model (SoM)**, **Citation Authority**, **Entity Salience**, and **Technical AI Readiness (`llms.txt` & JSON-LD)**.

🔗 **Live Interactive Dashboard:** [Launch Streamlit App](https://geosearch-7ps4jbhmptqetyyefnavtu.streamlit.app/)

---

## Core Capabilities

1. **Share of Model (SoM) & Citation Tracking:** Measures how frequently a brand or clinical/enterprise entity is cited, mentioned, and recommended across simulated LLM prompts across top generative engines.
2. **Competitive AI Gap Analysis:** Benchmarks target brand visibility, sentiment alignment, and citation prominence against Tier-1 competitors.
3. **Entity & Schema Graph Validator:** Evaluates interconnected JSON-LD structured data (`Organization`, `MedicalWebPage`, `FAQPage`, `Person`) to ensure deterministic knowledge graph ingestion.
4. **`llms.txt` Readiness Auditor:** Validates the presence and token-efficiency of root-level `llms.txt` documentation designed for LLM crawlers and retrieval-augmented generation (RAG) pipelines.

---

## Architecture & Methodology

Traditional SEO measures *positions* on a deterministic list of links. **GEO Observability** measures probabilistic *inclusion, attribution, and sentiment* inside synthesized natural language responses.

### Key Metrics Calculated:
* **Citation Rate ($C_r$):** Percentage of relevant prompt executions yielding an explicit source link or brand citation.
* **Entity Prominence Score ($E_p$):** Weighted metric based on where the brand appears in the generated response (e.g., primary recommendation vs. footnote).
* **RAG Readiness Index ($R_i$):** Composite technical score evaluating `llms.txt` structure, JSON-LD entity linking (`@id`, `sameAs`), and semantic HTML hierarchy.

---

## Quickstart & Local Installation

```bash
# Clone the repository
git clone [https://github.com/bgm352/enterprise-geo-observability.git](https://github.com/bgm352/enterprise-geo-observability.git)
cd enterprise-geo-observability

# Install dependencies
pip install -r requirements.txt

# Launch the observability dashboard
streamlit run app.py
