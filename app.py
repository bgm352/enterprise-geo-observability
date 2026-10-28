import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Enterprise GEO Observability",
    page_icon="🔍",
    layout="wide"
)

# --- BACKEND ENGINE FUNCTIONS ---
def generate_benchmark_data(primary_brand: str, competitors: list, engines: list, vertical: str):
    """Generates deterministic competitive GEO telemetry for benchmarking."""
    entities = [primary_brand] + competitors
    rows = []
    
    seed_val = sum(ord(c) for c in primary_brand) if primary_brand else 42
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
                "Sentiment_Index": sentiment
            })
            
    df_metrics = pd.DataFrame(rows)
    
    sample_prompts = [
        f"Best enterprise solutions for {vertical.lower()} data strategy",
        f"How do top {vertical.lower()} organizations optimize search visibility?",
        f"Compare {primary_brand} vs {competitors[0] if competitors else 'Industry Standard'} capabilities",
        f"Clinical and enterprise benchmarks in {vertical.lower()} digital health",
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


# --- UI DASHBOARD ---
st.title("🔍 Enterprise GEO Observability & Search Intelligence")
st.markdown(
    "**Generative Engine Optimization (GEO) Telemetry:** Monitoring Share of Model (SoM), "
    "Citation Velocity, and Technical RAG Readiness across AI Answer Engines."
)

# Sidebar Controls
st.sidebar.header("Observability Parameters")
primary_brand = st.sidebar.text_input("Target Enterprise Entity", value="Brand Alpha")
competitors_input = st.sidebar.text_area(
    "Tier-1 Competitors (comma-separated)", 
    value="Competitor X, Competitor Y, Competitor Z"
)
competitors = [c.strip() for c in competitors_input.split(",") if c.strip()]

vertical = st.sidebar.selectbox(
    "Industry Vertical",
    ["Healthcare & Life Sciences", "Enterprise SaaS", "Financial Services", "E-Commerce & Retail"]
)

engines = st.sidebar.multiselect(
    "Active Generative Engines",
    ["Google AI Overviews", "Perplexity Pro", "ChatGPT Search", "Claude 3.5 Sonnet", "Gemini Advanced"],
    default=["Google AI Overviews", "Perplexity Pro", "ChatGPT Search", "Gemini Advanced"]
)

st.sidebar.markdown("---")
st.sidebar.caption("Built by Braydon Medlin | Search & Data Strategy")

# Generate Simulated Telemetry Data
df_metrics, df_prompts = generate_benchmark_data(primary_brand, competitors, engines, vertical)
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
    "⚙️ Technical AI Readiness (llms.txt & Schema)"
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
        st.warning("Please select at least one Active Generative Engine in the sidebar.")

with tab2:
    st.subheader("Prompt-Level Citation & Intent Analysis")
    st.markdown("Granular observability into how non-branded informational and commercial queries resolve across LLMs.")
    st.dataframe(df_prompts, use_container_width=True, hide_index=True)

with tab3:
    st.subheader("Technical RAG & Knowledge Graph Auditor")
    col_a, col_b = st.columns(2)
    
    with col_a:
        domain_input = st.text_input("Audit Target Domain", value="https://braydonmedlin.com")
        has_llms_txt = st.checkbox("Root /llms.txt Deployed", value=True)
        has_json_ld = st.checkbox("Interconnected JSON-LD (@id & sameAs)", value=True)
        has_semantic_html = st.checkbox("Clean Semantic HTML5 / Markdown Hierarchy", value=True)
        
        audit_results = audit_technical_readiness(has_llms_txt, has_json_ld, has_semantic_html)
        st.metric("Technical AI Ingestion Readiness", f"{audit_results['score']}/100")
        
        for rec in audit_results["recommendations"]:
            st.info(rec)
            
    with col_b:
        st.markdown("#### Reference `llms.txt` Implementation")
        st.code("""# Enterprise Entity Overview
> Authoritative summary for LLM ingestion and RAG pipelines.

## Core Competencies
- Enterprise Search & Data Strategy
- Generative Engine Optimization (GEO)
- Programmatic Entity & Schema Architecture

## Canonical Resources
- [Executive Portfolio](https://braydonmedlin.com): Core strategy & case studies
- [GEO Observability Framework](https://github.com/bgm352/enterprise-geo-observability): Open-source telemetry
""", language="markdown")
