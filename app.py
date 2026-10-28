import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from geo_engine import generate_benchmark_data, audit_technical_readiness, calculate_geo_score

st.set_page_config(
    page_title="Enterprise GEO Observability",
    page_icon="🔍",
    layout="wide"
)

# Header Section
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
