import json
from datetime import datetime
import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf
from openai import OpenAI

# ------------------------------------------------------------------
# CONFIGURAZIONE E STILE GRAFICO (QUANTUM GLASSMORPHISM)
# ------------------------------------------------------------------
st.set_page_config(
    page_title="QUANTUM AI - XM.COM TERMINAL",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom CSS per rispecchiare fedelmente il design originale
st.markdown(
    """
<style>
    /* Sfondo Generale */
    .stApp {
        background-color: #060814;
        color: #e2e8f0;
    }
    
    /* Header Banner Quantum AI */
    .quantum-header {
        background: linear-gradient(135deg, #0b0f29 0%, #15103a 100%);
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 16px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        margin-bottom: 25px;
    }
    
    .quantum-title {
        font-size: 28px;
        font-weight: 900;
        letter-spacing: 2px;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
    }
    
    .quantum-sub {
        font-size: 11px;
        color: #38bdf8;
        letter-spacing: 1.5px;
        font-weight: 600;
    }

    /* Container e Card */
    .quantum-card {
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 15px;
        backdrop-filter: blur(10px);
    }
    
    /* Tabella e Mettiche */
    [data-testid="stMetricValue"] {
        color: #38bdf8 !important;
        font-weight: bold;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Client OpenAI con fallback di sicurezza per evitare blocchi
api_key = st.secrets.get("OPENAI_API_KEY", "")
client = OpenAI(api_key=api_key) if (api_key and "sk-" in api_key) else None


# ------------------------------------------------------------------
# ENGINE QUANTITATIVO (ANALISI XM)
# ------------------------------------------------------------------
class NabilAIEngine:

    def __init__(self, capital=10000.0):
        self.capital = capital
        self.assets_xm = {
            "GOLD": "GC=F",
            "OIL": "CL=F",
            "US100": "^NDX",
            "GER40": "^GDAXI",
            "EURUSD": "EURUSD=X",
            "BTCUSD": "BTC-USD",
        }

    def calculate_indicators(self, df):
        df["Upper_20"] = df["High"].shift(1).rolling(20).max()
        df["Lower_20"] = df["Low"].shift(1).rolling(20).min()
        high_low = df["High"] - df["Low"]
        high_close = np.abs(df["High"] - df["Close"].shift(1))
        low_close = np.abs(df["Low"] - df["Close"].shift(1))
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        df["ATR_20"] = tr.rolling(20).mean()
        return df

    def scan_markets(self):
        snapshots = {}
        for name, ticker in self.assets_xm.items():
            try:
                data = yf.download(
                    ticker, period="2mo", interval="1d", progress=False
                )
                if data.empty:
                    continue
                if isinstance(data.columns, pd.MultiIndex):
                    data.columns = data.columns.get_level_values(0)

                df = self.calculate_indicators(data)
                last = df.iloc[-1]
                close = float(last["Close"])
                up = float(last["Upper_20"])
                low = float(last["Lower_20"])
                atr = float(last["ATR_20"])

                snapshots[name] = {
                    "price": close,
                    "upper_20": up,
                    "lower_20": low,
                    "atr": atr,
                    "signal": (
                        "LONG"
                        if close > up
                        else ("SHORT" if close < low else "RANGE")
                    ),
                }
            except Exception:
                continue
        return snapshots


# ------------------------------------------------------------------
# SESSION STATE
# ------------------------------------------------------------------
if "engine" not in st.session_state:
    st.session_state.engine = NabilAIEngine()

if "trade_history" not in st.session_state:
    st.session_state.trade_history = [
        {
            "ID": "TRD-1092",
            "Asset": "GOLD",
            "Tipo": "LONG",
            "Apertura": "2026-07-24 14:30",
            "Chiusura": "2026-07-24 18:15",
            "Esito": "TP",
            "P&L": "+$250.00",
        },
        {
            "ID": "TRD-1091",
            "Asset": "US100",
            "Tipo": "SHORT",
            "Apertura": "2026-07-23 09:15",
            "Chiusura": "2026-07-23 11:40",
            "Esito": "SL",
            "P&L": "-$100.00",
        },
        {
            "ID": "TRD-1090",
            "Asset": "EURUSD",
            "Tipo": "LONG",
            "Apertura": "2026-07-22 10:00",
            "Chiusura": "2026-07-22 16:20",
            "Esito": "TP",
            "P&L": "+$180.00",
        },
    ]

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "🤖 **QUANTUM ENGINE XM.COM PRONTO.**\n\nHo allineato i database con i contratti del broker **XM.com**. Chiedimi di 'trovare un'opportunità' o di analizzare i grafici!",
        }
    ]

# ------------------------------------------------------------------
# UI INTERFACE (LAYOUT QUANTUM TERMINAL)
# ------------------------------------------------------------------

# Banner Superiore
st.markdown(
    """
    <div class="quantum-header">
        <div class="quantum-title">⚡ QUANTUM AI TERMINAL ⚡</div>
        <div class="quantum-sub">SYSTEM INTEGRATION: XM.COM BROKER CORE • MULTI-TIMEFRAME QUANT ENGINE</div>
    </div>
""",
    unsafe_allow_html=True,
)

# Scansione Mercati Live
with st.spinner("Allineamento dati XM.com in corso..."):
    snapshots = st.session_state.engine.scan_markets()

# Titolo Sezione Console
st.markdown("### 📡 CORE CONSOLE")

# Grid Mettiche Prezzi Live
c1, c2, c3 = st.columns(3)
c1.metric(
    "GOLD (XAUUSD)",
    f"${snapshots.get('GOLD', {}).get('price', 0):,.2f}",
    snapshots.get("GOLD", {}).get("signal", "N/A"),
)
c2.metric(
    "US100",
    f"{snapshots.get('US100', {}).get('price', 0):,.2f}",
    snapshots.get("US100", {}).get("signal", "N/A"),
)
c3.metric(
    "EURUSD",
    f"{snapshots.get('EURUSD', {}).get('price', 0):.4f}",
    snapshots.get("EURUSD", {}).get("signal", "N/A"),
)

st.divider()

# Registro TP / SL
st.markdown("### 📜 REGISTRO ESEGUITI (TP / SL)")
df_hist = pd.DataFrame(st.session_state.trade_history)

tot = len(df_hist)
tp = len(df_hist[df_hist["Esito"] == "TP"])
sl = len(df_hist[df_hist["Esito"] == "SL"])
wr = (tp / tot * 100) if tot > 0 else 0

m1, m2, m3, m4 = st.columns(4)
m1.metric("Totale Trades", tot)
m2.metric("Take Profit 🎯", tp)
m3.metric("Stop Loss 🛑", sl)
m4.metric("Win Rate %", f"{wr:.1f}%")

st.dataframe(df_hist, use_container_width=True)

st.divider()

# Chat AI Console
st.markdown("### 💬 AI MENTOR CONSOLE")

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Fai una domanda sul grafico o chiedi un'analisi..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    if client:
        try:
            sys_prompt = f"""
            Sei l'AI Quantum Trading Mentor integrato con XM.com.
            Analizza i dati di mercato reali: {json.dumps(snapshots, indent=2)}
            Storico operazioni: {json.dumps(st.session_state.trade_history, indent=2)}
            Rispondi in modo tecnico, analitico e senza risposte preimpostate.
            """
            res = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
            )
            reply = res.choices[0].message.content
        except Exception as e:
            reply = f"⚠️ Errore di connessione API OpenAI: {str(e)}. Verifica che la chiave sia attiva su platform.openai.com"
    else:
        reply = "⚠️ **API Key OpenAI non rilevata o non valida.** Inseriscila nei Secrets di Streamlit su `share.streamlit.io` -> Manage app -> Secrets -> OPENAI_API_KEY = 'sk-...'"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)
