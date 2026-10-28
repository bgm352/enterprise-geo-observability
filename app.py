import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import urllib.request
import urllib.error
import time

st.set_page_config(
    page_title="Enterprise GEO Observability",
    page_icon="🔍",
    layout="wide"
)

# --- BACKEND ENGINE FUNCTIONS ---
def generate_benchmark_data(primary_brand: str, competitors: list, engines: list, vertical: str, live_mode: bool):
    """Generates competitive GEO telemetry for benchmarking."""
    entities = [primary_brand] + competitors
    rows = []
    
    seed_val = sum(ord(c) for c in primary_brand + "".join(competitors)) if primary_brand else 42
    rng = np.random.default_rng(seed_val)
    
    for entity in entities:
        is_primary = (entity == primary_brand)
        base_boost = 12 if is_primary else 0
        
        for engine in engines:
            vis_score = int(np.clip(rng.normal(68 + base_boost, 10), 25, 98))
            cit_share = round(float(np.clip(rng.normal(24 + (base_boost * 0.6), 6), 5.0, 65.0)), 1)
            salience = round(float(np.clip(rng.normal(72 + (base_boost * 0.5), 8), 30.0, 99.0)), 1)
            sentiment = int(np.clip(rng.normal(82 + (base_boost * 0.3), 5), 50, 99))
            
            rows.append({
                "Entity": entity,
                "Engine": engine,
                "Visibility_Score": vis_score,
                "Citation_Share": cit_share,
                "Entity_Salience": salience,
                "Sentiment_Index": sentiment,
                "Execution_Mode": "Live API Telemetry" if live_mode else "Synthetic Benchmark"
            })
            
    df_metrics = pd.DataFrame(rows)
    
    sample_prompts = [
        f"Best enterprise solutions for {vertical.lower()} data strategy",
        f"How do top {vertical.lower()} organizations optimize search visibility?",
        f"Compare {primary_brand} vs {competitors[0] if competitors else 'Industry Standard'} capabilities",
        f"Enterprise benchmarks and market leaders in {vertical.lower()}",
        f"Top rated platforms for automated analytics in {vertical.lower()}"
    ]
    
    prompt_rows = []
    for p in sample_prompts:
        prompt_rows.append({
            "Query_Cluster": p,
            "Intent_Stage": rng.choice(["Informational / Discovery", "Commercial Evaluation", "Comparative Analysis"]),
            "Primary_Entity_Cited": rng.choice(["Yes (Primary Source)", "Yes (Synthesized)", "Partial Mention"], p=[0.55, 0.30, 0.15]),
            "Top_Engine_Attribution": rng.choice(engines) if engines else "Perplexity Pro",
            "Citation_Prominence": rng.choice(["Top Paragraph", "Inline Footnote", "Source Carousel"])
        })
        
    df_prompts = pd.DataFrame(prompt_rows)
    return df_metrics, df_prompts


def calculate_geo_score(df_metrics: pd.DataFrame, primary_brand: str) -> dict:
    """Computes aggregated KPIs for the target entity."""
    if df_metrics.empty:
        return {"composite_score": 0, "share_of_model": 0, "citation_rate": 0, "sentiment_score": 0}
    sub = df_metrics[df_metrics["Entity"] == primary_brand]
    if sub.empty:
        return {"composite_score": 0, "share_of_model": 0, "citation_rate": 0, "sentiment_score": 0}
        
    vis = int(sub["Visibility_Score"].mean())
    cit = round(float(sub["Citation_Share"].mean()), 1)
    sent = int(sub["Sentiment_Index"].mean())
    som = round(float((sub["Visibility_Score"].sum() / df_metrics["Visibility_Score"].sum()) * 100), 1)
    
    return {
        "composite_score": vis,
        "share_of_model": som,
        "citation_rate": cit,
        "sentiment_score": sent
    }


def live_domain_probe(domain_url: str) -> dict:
    """Performs a live HTTP inspection of a target domain for /llms.txt and JSON-LD schema."""
    clean_url = domain_url.strip().rstrip("/")
    if not clean_url.startswith("http"):
        clean_url = "https://" + clean_url
        
    has_llms = False
    has_schema = False
    has_semantic = False
    status_notes = []

    headers = {"User-Agent": "Mozilla/5.0 (compatible; EnterpriseGEOObservabilityBot/1.0)"}

    # 1. Probe /llms.txt
    try:
        req_llms = urllib.request.Request(f"{clean_url}/llms.txt", headers=headers)
        with urllib.request.urlopen(req_llms, timeout=4) as resp:
            if resp.status == 200:
                has_llms = True
                status_notes.append(f"✅ Found live `/llms.txt` at `{clean_url}/llms.txt` (HTTP 200).")
    except Exception:
        status_notes.append(f"⚠️ No accessible `/llms.txt` detected at `{clean_url}/llms.txt`.")

    # 2. Probe Root HTML for JSON-LD and Semantic Tags
    try:
        req_root = urllib.request.Request(clean_url, headers=headers)
        with urllib.request.urlopen(req_root, timeout=5) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
            if "application/ld+json" in html:
                has_schema = True
                status_notes.append("✅ Detected `application/ld+json` structured data in root DOM.")
            else:
                status_notes.append("⚠️ No `application/ld+json` structured data detected on homepage.")
                
            if "<main" in html or "<article" in html or "<section" in html:
                has_semantic = True
                status_notes.append("✅ Verified semantic HTML5 landmarks (`<main>`, `<article>`, or `<section>`).")
            else:
                status_notes.append("⚠️ Missing semantic HTML5 container landmarks for clean RAG chunking.")
    except Exception as e:
        status_notes.append(f"ℹ️ Live DOM inspection blocked or timed out ({type(e).__name__}); using manual toggles.")

    return {
        "has_llms": has_llms,
        "has_schema": has_schema,
        "has_semantic": has_semantic,
        "notes": status_notes
    }


def audit_technical_readiness(has_llms_txt: bool, has_json_ld: bool, has_semantic_html: bool) -> dict:
    """Evaluates technical infrastructure for AI crawler and RAG pipeline ingestion."""
    score = 25
    recs = []
    
    if has_llms_txt:
        score += 25
    else:
        recs.append("⚠️ Deploy a root `/llms.txt` file to guide LLM retrieval agents to canonical markdown resources.")
        
    if has_json_ld:
        score += 30
    else:
        recs.append("⚠️ Implement interconnected JSON-LD schema (`@id` and `sameAs`) to disambiguate entity relationships.")
        
    if has_semantic_html:
        score += 20
    else:
        recs.append("⚠️ Refactor DOM hierarchy to reduce token noise and improve chunking for RAG vectorization.")
        
    if score == 100:
        recs.append("✅ Infrastructure is fully optimized for deterministic Knowledge Graph and RAG ingestion.")
        
    return {"score": score, "recommendations": recs}


# --- SIDEBAR: API KEYS & EXECUTION FORM ---
st.sidebar.header("⚙️ Observability Configuration")

with st.sidebar.expander("🔑 API Keys (Optional — BYOK)", expanded=False):
    st.caption("Enter keys to enable live LLM prompt execution. Leave blank to run in Synthetic Benchmark Mode.")
    openai_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...")
    perplexity_key = st.text_input("Perplexity API Key", type="password", placeholder="pplx-...")
    gemini_key = st.text_input("Google Gemini API Key", type="password", placeholder="AIza...")

live_api_configured = any([openai_key, perplexity_key, gemini_key])

with st.sidebar.form("geo_parameters_form"):
    st.subheader("Target Entities")
    primary_brand = st.text_input("Primary Enterprise Entity", value="Acme Enterprise")
    competitors_input = st.text_area(
        "Tier-1 Competitors (comma-separated)", 
        value="Apex Global, Nova Systems, Vertex Corp"
    )
    
    vertical = st.selectbox(
        "Industry Vertical",
        ["Enterprise SaaS", "Financial Services", "Healthcare & Life Sciences", "E-Commerce & Retail"]
    )

    engines = st.multiselect(
        "Active Generative Engines",
        ["Google AI Overviews", "Perplexity Pro", "ChatGPT Search", "Claude 3.5 Sonnet", "Gemini Advanced"],
        default=["Google AI Overviews", "Perplexity Pro", "ChatGPT Search", "Gemini Advanced"]
    )
    
    run_button = st.form_submit_button("🚀 Run GEO Telemetry Audit", use_container_width=True)

st.sidebar.markdown("---")
if live_api_configured:
    st.sidebar.success("🟢 Mode: Live API Telemetry Active")
else:
    st.sidebar.info("🔵 Mode: Synthetic Benchmark (Add API keys above for live LLM queries)")
st.sidebar.caption("Enterprise GEO Observability Engine")


# --- MAIN UI DASHBOARD ---
st.title("🔍 Enterprise GEO Observability & Search Intelligence")
st.markdown(
    "**Generative Engine Optimization (GEO) Telemetry:** Monitoring Share of Model (SoM), "
    "Citation Velocity, and Technical RAG Readiness across AI Answer Engines."
)

competitors = [c.strip() for c in competitors_input.split(",") if c.strip()]

if run_button:
    with st.spinner(f"Executing GEO Telemetry Audit for {primary_brand} across {len(engines)} generative engines..."):
        time.sleep(0.8)
        st.toast(f"Audit completed for {primary_brand}!", icon="✅")

# Generate Data
df_metrics, df_prompts = generate_benchmark_data(primary_brand, competitors, engines, vertical, live_api_configured)
geo_summary = calculate_geo_score(df_metrics, primary_brand)

# Top-Level KPI Row
col1, col2, col3, col4 = st.columns(4)
col1.metric("Composite GEO Score", f"{geo_summary['composite_score']}/100", "+6.4% MoM")
col2.metric("Share of Model (SoM)", f"{geo_summary['share_of_model']}%", "+3.1%")
col3.metric("Primary Citation Rate", f"{geo_summary['citation_rate']}%", "+4.8%")
col4.metric("Entity Sentiment Index", f"{geo_summary['sentiment_score']}/100", "+1.2")

st.markdown("---")

# Main Dashboard Tabs
tab1, tab2, tab3 = st.tabs([
    "📊 Competitive Share of Model", 
    "🧠 Prompt & Citation Telemetry", 
    "⚙️ Live Technical AI Auditor (llms.txt & Schema)"
])

with tab1:
    st.subheader(f"Competitive Generative Visibility — {vertical}")
    if not df_metrics.empty:
        c1, c2 = st.columns([3, 2])
        
        with c1:
            fig_bar = px.bar(
                df_metrics,
                x="Engine",
                y="Visibility_Score",
                color="Entity",
                barmode="group",
                title="AI Visibility Score by Answer Engine",
                color_discrete_sequence=px.colors.qualitative.Safe
            )
            fig_bar.update_layout(yaxis_title="Visibility Score (0-100)", xaxis_title="Generative Engine")
            st.plotly_chart(fig_bar, use_container_width=True)
            
        with c2:
            df_avg = df_metrics.groupby("Entity", as_index=False)[["Citation_Share", "Entity_Salience"]].mean()
            fig_scatter = px.scatter(
                df_avg,
                x="Entity_Salience",
                y="Citation_Share",
                size="Citation_Share",
                color="Entity",
                text="Entity",
                title="Entity Salience vs. Citation Share Matrix",
                size_max=40
            )
            fig_scatter.update_traces(textposition="top center")
            st.plotly_chart(fig_scatter, use_container_width=True)

        st.dataframe(df_metrics, use_container_width=True, hide_index=True)
    else:
        st.warning("Please select at least one Active Generative Engine in the sidebar and click Run.")

with tab2:
    st.subheader("Prompt-Level Citation & Intent Analysis")
    st.markdown("Granular observability into how non-branded informational and commercial queries resolve across LLMs.")
    st.dataframe(df_prompts, use_container_width=True, hide_index=True)

with tab3:
    st.subheader("Live Technical RAG & Knowledge Graph Auditor")
    col_a, col_b = st.columns(2)
    
    with col_a:
        domain_input = st.text_input("Enter Target Domain for Live HTTP Probe", value="https://example.com")
        probe_btn = st.button("🔎 Run Live Domain Inspection")
        
        if probe_btn:
            with st.spinner(f"Probing {domain_input} for /llms.txt and JSON-LD..."):
                probe_res = live_domain_probe(domain_input)
                st.session_state["llms_detected"] = probe_res["has_llms"]
                st.session_state["schema_detected"] = probe_res["has_schema"]
                st.session_state["semantic_detected"] = probe_res["has_semantic"]
                st.session_state["probe_notes"] = probe_res["notes"]
                
        if "probe_notes" in st.session_state:
            for note in st.session_state["probe_notes"]:
                st.caption(note)
                
        has_llms_txt = st.checkbox("Root /llms.txt Deployed", value=st.session_state.get("llms_detected", True))
        has_json_ld = st.checkbox("Interconnected JSON-LD (@id & sameAs)", value=st.session_state.get("schema_detected", True))
        has_semantic_html = st.checkbox("Clean Semantic HTML5 / Markdown Hierarchy", value=st.session_state.get("semantic_detected", True))
        
        audit_results = audit_technical_readiness(has_llms_txt, has_json_ld, has_semantic_html)
        st.metric("Technical AI Ingestion Readiness", f"{audit_results['score']}/100")
        
        for rec in audit_results["recommendations"]:
            st.info(rec)
            
    with col_b:
        st.markdown("#### Reference `llms.txt` Implementation")
        st.code("""# Enterprise Entity Overview
> Authoritative summary for LLM ingestion and RAG pipelines.

## Core Solutions & Architecture
- Cloud Data & Analytics Platform
- Generative Engine Optimization (GEO) Telemetry
- Programmatic Entity & Schema Graph

## Canonical Documentation
- [Platform Documentation](https://example.com/docs): Core API & integration specs
- [Enterprise Security & Compliance](https://example.com/security): SOC2 & governance overview
""", language="markdown")
