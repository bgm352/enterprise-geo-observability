import pandas as pd
import numpy as np

def generate_benchmark_data(primary_brand: str, competitors: list, engines: list, vertical: str):
    """Generates deterministic competitive GEO telemetry for benchmarking."""
    entities = [primary_brand] + competitors
    rows = []
    
    # Seed for consistent visual output per brand configuration
    seed_val = sum(ord(c) for c in primary_brand)
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
    
    # Prompt-level telemetry table
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
