import json
from datetime import datetime
import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf
from openai import OpenAI

# ------------------------------------------------------------------
# CONFIGURAZIONE PAGINA
# ------------------------------------------------------------------
st.set_page_config(
    page_title="Nabil AI - Trading Terminal",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Inizializzazione Client OpenAI dai Secrets di Streamlit
api_key = st.secrets.get("OPENAI_API_KEY", "")
client = OpenAI(api_key=api_key) if api_key else None


# ------------------------------------------------------------------
# ENGINE QUANTITATIVO (ANALISI XM)
# ------------------------------------------------------------------
class NabilAIEngine:

    def __init__(self, capital=10000.0, max_risk_pct=0.01):
        self.capital = capital
        self.max_risk_pct = max_risk_pct
        self.assets_xm = {
            "GOLD": "GC=F",
            "OIL": "CL=F",
            "US100": "^NDX",
            "GER40": "^GDAXI",
            "GBPJPY": "GBPJPY=X",
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
                        "LONG BREAKOUT"
                        if close > up
                        else ("SHORT BREAKOUT" if close < low else "RANGING")
                    ),
                }
            except Exception:
                continue
        return snapshots


# ------------------------------------------------------------------
# SESSION STATE (PER STORICO TP/SL E CHAT)
# ------------------------------------------------------------------
if "engine" not in st.session_state:
    st.session_state.engine = NabilAIEngine()

# Storico iniziale con operazioni di esempio
if "trade_history" not in st.session_state:
    st.session_state.trade_history = [
        {
            "ID": "TRD-1092",
            "Asset": "GOLD",
            "Tipo": "LONG",
            "Data Apertura": "2026-07-24 14:30",
            "Data Chiusura": "2026-07-24 18:15",
            "Ingresso": 2380.00,
            "Uscita": 2405.00,
            "Esito": "TP",
            "P&L": "+$250.00 (+2.1%)",
        },
        {
            "ID": "TRD-1091",
            "Asset": "US100",
            "Tipo": "SHORT",
            "Data Apertura": "2026-07-23 09:15",
            "Data Chiusura": "2026-07-23 11:40",
            "Ingresso": 19850.00,
            "Uscita": 19890.00,
            "Esito": "SL",
            "P&L": "-$100.00 (-1.0%)",
        },
        {
            "ID": "TRD-1090",
            "Asset": "EURUSD",
            "Tipo": "LONG",
            "Data Apertura": "2026-07-22 10:00",
            "Data Chiusura": "2026-07-22 16:20",
            "Ingresso": 1.0850,
            "Uscita": 1.0895,
            "Esito": "TP",
            "P&L": "+$180.00 (+1.8%)",
        },
    ]

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Ciao! Sono il tuo AI Mentor. Ho caricato i dati dei grafici live e il tuo storico operazioni. Come posso aiutarti oggi?",
        }
    ]

# ------------------------------------------------------------------
# INTERFACCIA UTENTE DASHBOARD
# ------------------------------------------------------------------
st.title("⚡ NABIL AI INFINITY TERMINAL")
st.caption("Piattaforma di Analisi Quantitativa & AI Mentor 24/7")

# Scansione Mercati Live
with st.spinner("Scansione grafici XM in tempo reale..."):
    snapshots = st.session_state.engine.scan_markets()

# Visualizzazione Prezzi e Segnali principali
col1, col2, col3 = st.columns(3)
col1.metric(
    "GOLD (XAUUSD)",
    f"${snapshots.get('GOLD', {}).get('price', 0):,.2f}",
    snapshots.get("GOLD", {}).get("signal", "N/A"),
)
col2.metric(
    "US100",
    f"{snapshots.get('US100', {}).get('price', 0):,.2f}",
    snapshots.get("US100", {}).get("signal", "N/A"),
)
col3.metric(
    "EURUSD",
    f"{snapshots.get('EURUSD', {}).get('price', 0):.4f}",
    snapshots.get("EURUSD", {}).get("signal", "N/A"),
)

st.divider()

# ------------------------------------------------------------------
# SEZIONE REGISTRO STORICO (TP / SL & WIN RATE)
# ------------------------------------------------------------------
st.subheader("📜 Registro Storico Eseguiti (Take Profit & Stop Loss)")

df_history = pd.DataFrame(st.session_state.trade_history)

# Calcolo Metriche
total_trades = len(df_history)
tp_count = len(df_history[df_history["Esito"] == "TP"])
sl_count = len(df_history[df_history["Esito"] == "SL"])
win_rate = (tp_count / total_trades * 100) if total_trades > 0 else 0.0

# Metric Badges
m1, m2, m3, m4 = st.columns(4)
m1.metric("Totale Operazioni", total_trades)
m2.metric("Take Profit 🎯", tp_count)
m3.metric("Stop Loss 🛑", sl_count)
m4.metric("Win Rate %", f"{win_rate:.1f}%")

# Tabella Eseguiti
st.dataframe(df_history, use_container_width=True)

st.divider()

# ------------------------------------------------------------------
# CHAT AI MENTOR DINAMICO
# ------------------------------------------------------------------
st.subheader("💬 AI Mentor Chat (Analisi Grafici Dinamica)")

# Mostra i messaggi passati
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Input dell'utente
if prompt := st.chat_input(
    "Chiedimi un'analisi sul grafico dell'Oro o sui tuoi trade..."
):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    if client:
        # Prompt di contesto per non avere risposte prefabbricate
        system_context = f"""
        Sei un AI Mentor Professionista di Trading Quantitativo.
        Il tuo compito è analizzare i grafici e rispondere all'utente in modo dinamico, analitico e senza mai usare risposte preimpostate.

        DATI DI MERCATO LIVE DAI GRAFICI:
        {json.dumps(snapshots, indent=2)}

        REGISTRO STORICO TP / SL DELL'UTENTE:
        {json.dumps(st.session_state.trade_history, indent=2)}

        Rispondi alla domanda dell'utente basandoti unicamente su questi dati reali.
        """

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_context},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
        )
        reply = response.choices[0].message.content
    else:
        reply = "⚠️ Nota: Inserisci la tua OPENAI_API_KEY nelle impostazioni Secrets di Streamlit per attivare l'AI Mentor."

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)
