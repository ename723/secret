import streamlit as st

# Impostazione pagina mobile-friendly
st.set_page_config(page_title="AI Chart Detector", layout="centered")

# CSS Personalizzato per replicare l'UI del video
st.markdown("""
<style>
    /* Sfondo scuro principale */
    .stApp {
        background-color: #0b0f19;
        color: #f3f4f6;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* Header SIMBOLO */
    .symbol-header {
        text-align: center;
        font-size: 24px;
        font-weight: 800;
        letter-spacing: 1px;
        margin-bottom: 20px;
        color: #ffffff;
    }

    /* Card Contenitore generale */
    .ui-card {
        background-color: #151c2c;
        border-radius: 16px;
        padding: 16px;
        margin-bottom: 16px;
        border: 1px solid #232d42;
    }

    .card-title {
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #94a3b8;
        font-weight: 600;
        margin-bottom: 12px;
    }

    /* Badge Grid per Insights */
    .badge-grid {
        display: flex;
        justify-content: space-between;
        gap: 8px;
    }

    .badge-item {
        background: #1e293b;
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        flex: 1;
    }

    .badge-label {
        font-size: 11px;
        color: #64748b;
    }

    .badge-value {
        font-size: 14px;
        font-weight: 700;
        color: #38bdf8;
        margin-top: 2px;
    }

    /* Strategy Box (HOLD/BUY/SELL) */
    .strategy-box {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border-left: 4px solid #f59e0b; /* Arancione per HOLD, Verde #22c55e per BUY */
        padding: 14px;
        border-radius: 8px;
        margin-bottom: 12px;
    }

    .strategy-badge {
        display: inline-block;
        background-color: #f59e0b;
        color: #000;
        font-weight: 800;
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 14px;
        margin-bottom: 8px;
    }

    /* Tag dei Pattern Riconosciuti */
    .pattern-chip {
        display: inline-block;
        background-color: #1e293b;
        border: 1px solid #334155;
        color: #cbd5e1;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 12px;
        margin-right: 6px;
        margin-bottom: 6px;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- UI COMPONENTI -----------------

# 1. Header Asset
st.markdown('<div class="symbol-header">EURUSD</div>', unsafe_allow_html=True)

# 2. Card Insights (Trend, Timeframe, Volatilità)
st.markdown("""
<div class="ui-card">
    <div class="card-title">Insights</div>
    <div class="badge-grid">
        <div class="badge-item">
            <div class="badge-label">Trend</div>
            <div class="badge-value">Sideways</div>
        </div>
        <div class="badge-item">
            <div class="badge-label">Timeframe</div>
            <div class="badge-value">1H</div>
        </div>
        <div class="badge-item">
            <div class="badge-label">Volatilità</div>
            <div class="badge-value">Media</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 3. Card AI Strategy
st.markdown("""
<div class="ui-card">
    <div class="card-title">AI Strategy</div>
    <div class="strategy-box">
        <div class="strategy-badge">HOLD</div>
        <p style="font-size: 13px; color: #cbd5e1; margin: 0;">
            Il prezzo si trova all'interno di un range di consolidamento. Si consiglia attesa fino allo sweep della liquidità sui minimi o la rottura della struttura.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# 4. Pattern Riconosciuti
st.markdown("""
<div class="ui-card">
    <div class="card-title">Erkannte Muster / Pattern</div>
    <div>
        <span class="pattern-chip">Double Bottom</span>
        <span class="pattern-chip">Bullish Engulfing</span>
        <span class="pattern-chip">FVG Unfilled</span>
    </div>
</div>
""", unsafe_allow_html=True)

# 5. Dettagli Analisi (Accordions)
st.markdown('<div class="card-title" style="padding-left: 4px;">Detaillierte Analyse</div>', unsafe_allow_html=True)

with st.expander("Price Action & Struttura"):
    st.write("Presenza di una struttura interna ribassista con reazione immediata sul POI a 1.0850.")

with st.expander("Supporti e Resistenze"):
    st.write("• **Resistenza Chiave:** 1.0920\n• **Supporto Chiave:** 1.0810")

with st.expander("Indicatori & Momentum"):
    st.write("RSI in zona neutrale (48). Nessuna divergenza evidente sul timeframe orario.")
