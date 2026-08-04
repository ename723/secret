import streamlit as st

st.set_page_config(page_title="AI Chart Detector", layout="centered")

# CSS aggiornato con griglia per i parametri di Trade Setup
st.markdown("""
<style>
    .stApp {
        background-color: #0b0f19;
        color: #f3f4f6;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    .ui-card {
        background-color: #151c2c;
        border-radius: 16px;
        padding: 16px;
        margin-bottom: 16px;
        border: 1px solid #232d42;
    }

    .card-title {
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #94a3b8;
        font-weight: 700;
        margin-bottom: 12px;
    }

    /* Strategia Header */
    .strategy-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }

    .badge-buy {
        background-color: #22c55e;
        color: #052e16;
        font-weight: 800;
        padding: 4px 14px;
        border-radius: 6px;
        font-size: 14px;
    }

    .winrate-tag {
        background-color: #1e293b;
        border: 1px solid #10b981;
        color: #10b981;
        font-weight: 700;
        font-size: 12px;
        padding: 4px 10px;
        border-radius: 20px;
    }

    /* Griglia livelli di Entry, TP, SL */
    .trade-grid {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 8px;
        margin-top: 10px;
    }

    .trade-box {
        background: #0f172a;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #1e293b;
        text-align: center;
    }

    .trade-label {
        font-size: 10px;
        color: #64748b;
        font-weight: 700;
        text-transform: uppercase;
    }

    .trade-value {
        font-size: 13px;
        font-weight: 700;
        margin-top: 2px;
    }

    .val-entry { color: #38bdf8; }
    .val-tp { color: #22c55e; }
    .val-sl { color: #ef4444; }

    .rationale-text {
        font-size: 12px;
        color: #94a3b8;
        margin-top: 10px;
        line-height: 1.4;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- UI COMPONENTE TRADE SETUP -----------------

# Dati di esempio (da sostituire dinamicamente con il JSON restituito da Claude)
signal = "BUY"
win_rate = "74%"
entry_price = "1.08450"
tp_price = "1.08900"
sl_price = "1.08220"
rationale = "Liquidity sweep completato sui minimi asiatici. Presenza di un FVG rialzista con reazione sul POI H1."

st.markdown(f"""
<div class="ui-card">
    <div class="card-title">AI Strategy & Execution</div>
    
    <!-- Badges Direzione e Win Rate -->
    <div class="strategy-header">
        <span class="badge-buy">{signal}</span>
        <span class="winrate-tag">Win Rate: {win_rate}</span>
    </div>

    <!-- Parametri operativi: Entry, TP, SL -->
    <div class="trade-grid">
        <div class="trade-box">
            <div class="trade-label">Entry</div>
            <div class="trade-value val-entry">{entry_price}</div>
        </div>
        <div class="trade-box">
            <div class="trade-label">Take Profit</div>
            <div class="trade-value val-tp">{tp_price}</div>
        </div>
        <div class="trade-box">
            <div class="trade-label">Stop Loss</div>
            <div class="trade-value val-sl">{sl_price}</div>
        </div>
    </div>

    <!-- Motivazione tecnica -->
    <div class="rationale-text">
        <strong>Analisi:</strong> {rationale}
    </div>
</div>
""", unsafe_allow_html=True)
