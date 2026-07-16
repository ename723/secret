import streamlit as st

# --- MENU LATERALE ---
st.sidebar.title("🍔 Quantum Menu")
pagina = st.sidebar.radio("Naviga in:", ["💻 Terminale Operativo", "📚 Academy"])

if pagina == "📚 Academy":
    st.title("📚 Academy: Corso Strategie")
    st.write("Area in fase di sviluppo.")
    st.stop()

import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as dict_plot
from plotly.subplots import make_subplots
import time

# Configurazione della pagina Streamlit
st.set_page_config(
    page_title="QUANTUM AI - XM.COM TERMINAL", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS ULTRA FUTURISTICO CON LOGHI E SCRITTE IN BIANCO FORZATO ---
st.markdown("""
    <style>
        .stApp {
            background: radial-gradient(circle at 50% 50%, #0d1117 0%, #07090e 100%);
            color: #ffffff !important;
            font-family: 'Courier New', Courier, monospace, sans-serif;
        }
        
        .stMarkdown, .stMarkdown p, .stChatMessage, p, li, span, div {
            color: #ffffff !important;
        }
        
        .laser-bar {
            height: 3px;
            background: linear-gradient(90deg, #00f2fe 0%, #4facfe 30%, #a855f7 70%, #ef4444 100%);
            width: 100%;
            position: absolute;
            top: 0;
            left: 0;
            box-shadow: 0px 0px 15px #00f2fe, 0px 0px 30px #a855f7;
            animation: pulse 2s infinite;
        }
        
        .terminal-header {
            text-align: center;
            padding: 25px 0 15px 0;
            background: rgba(13, 17, 23, 0.6);
            border-bottom: 1px solid rgba(0, 242, 254, 0.15);
            margin-bottom: 25px;
            border-radius: 0 0 20px 20px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), inset 0 0 15px rgba(0, 242, 254, 0.05);
        }
        
        .terminal-title {
            font-family: 'Courier New', monospace;
            font-size: 2.5rem !important;
            font-weight: 900 !important;
            letter-spacing: 4px;
            background: linear-gradient(90deg, #00f2fe, #a855f7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 20px rgba(0, 242, 254, 0.3);
            margin: 0;
        }

        .terminal-subtitle {
            color: #00f2fe !important;
            font-size: 0.9rem;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-top: 5px;
            text-shadow: 0 0 8px rgba(0, 242, 254, 0.4);
        }

        .neon-card {
            background: rgba(18, 22, 33, 0.8) !important;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-left: 4px solid #3b82f6; 
            border-radius: 8px;
            padding: 15px;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
            transition: all 0.3s ease;
        }
        .neon-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(59, 130, 246, 0.2);
            border-color: rgba(59, 130, 246, 0.5);
        }
        
        .card-green { border-left: 4px solid #10b981; }
        .card-green:hover { box-shadow: 0 8px 25px rgba(16, 185, 129, 0.25); }
        
        .card-red { border-left: 4px solid #ef4444; }
        .card-red:hover { box-shadow: 0 8px 25px rgba(239, 68, 68, 0.25); }
        
        .card-purple { border-left: 4px solid #a855f7; }
        .card-purple:hover { box-shadow: 0 8px 25px rgba(168, 85, 247, 0.25); }
        
        .stChatMessage {
            background-color: rgba(18, 22, 33, 0.85) !important;
            border-radius: 12px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            padding: 15px !important;
            box-shadow: 0 5px 15px rgba(0,0,0,0.4);
            backdrop-filter: blur(5px);
        }
        
        input {
            color: #ffffff !important;
        }
        
        .signal-glow-buy {
            background-color: rgba(16, 185, 129, 0.15);
            color: #10b981 !important;
            padding: 6px 14px;
            border-radius: 4px;
            border: 1px solid #10b981;
            font-weight: bold;
            text-shadow: 0 0 10px rgba(16, 185, 129, 0.6);
            box-shadow: 0 0 15px rgba(16, 185, 129, 0.25);
            display: inline-block;
        }
        .signal-glow-buy * { color: #10b981 !important; }
        
        .signal-glow-sell {
            background-color: rgba(239, 68, 68, 0.15);
            color: #ef4444 !important;
            padding: 6px 14px;
            border-radius: 4px;
            border: 1px solid #ef4444;
            font-weight: bold;
            text-shadow: 0 0 10px rgba(239, 68, 68, 0.6);
            box-shadow: 0 0 15px rgba(239, 68, 68, 0.25);
            display: inline-block;
        }
        .signal-glow-sell * { color: #ef4444 !important; }
        
        .signal-glow-neutral {
            background-color: rgba(156, 163, 175, 0.15);
            color: #ffffff !important;
            padding: 6px 14px;
            border-radius: 4px;
            border: 1px solid #4b5563;
            font-weight: bold;
            display: inline-block;
        }
        .signal-glow-neutral * { color: #ffffff !important; }
        
        @keyframes pulse {
            0% { opacity: 0.7; }
            50% { opacity: 1; }
            100% { opacity: 0.7; }
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="laser-bar"></div>', unsafe_allow_html=True)

st.markdown("""
    <div class="terminal-header">
        <h1 class="terminal-title">⚡ QUANTUM AI TERMINAL ⚡</h1>
        <div class="terminal-subtitle">SYSTEM INTEGRATION: XM.COM BROKER CORE • MULTI-TIMEFRAME QUANT ENGINE</div>
    </div>
""", unsafe_allow_html=True)

# --- MAPPATURA SPECIFICA PER XM.COM (CON SUPPORTO AL SUFFISSO '#' E INDICI CASH) ---
MAPPATURA_ASSET = {
    # Forex Majors (XM Ultra Low / Standard)
    "EURUSD#": "EURUSD=X", "EURUSD": "EURUSD=X",
    "GBPUSD#": "GBPUSD=X", "GBPUSD": "GBPUSD=X",
    "USDJPY#": "USDJPY=X", "USDJPY": "USDJPY=X",
    "USDCHF#": "USDCHF=X", "USDCHF": "USDCHF=X",
    "AUDUSD#": "AUDUSD=X", "AUDUSD": "AUDUSD=X",
    "USDCAD#": "USDCAD=X", "USDCAD": "USDCAD=X",
    "NZDUSD#": "NZDUSD=X", "NZDUSD": "NZDUSD=X",
    
    # Forex Crosses
    "GBPJPY#": "GBPJPY=X", "GBPJPY": "GBPJPY=X",
    "EURJPY#": "EURJPY=X", "EURJPY": "EURJPY=X",
    "EURAUD#": "EURAUD=X", "EURAUD": "EURAUD=X",
    "EURGBP#": "EURGBP=X", "EURGBP": "EURGBP=X",
    "EURCAD#": "EURCAD=X", "EURCAD": "EURCAD=X",
    "GBPCHF#": "GBPCHF=X", "GBPCHF": "GBPCHF=X",
    "GBPAUD#": "GBPAUD=X", "GBPAUD": "GBPAUD=X",
    "AUDJPY#": "AUDJPY=X", "AUDJPY": "AUDJPY=X",
    "CHFJPY#": "CHFJPY=X", "CHFJPY": "CHFJPY=X",
    
    # Metalli & Energie XM.com
    "GOLD#": "GC=F", "GOLD": "GC=F", "XAUUSD": "GC=F",
    "SILVER#": "SI=F", "SILVER": "SI=F", "XAGUSD": "SI=F",
    "OILCASH#": "CL=F", "OILCASH": "CL=F", "OIL#": "CL=F", "OIL": "CL=F",
    
    # Indici Cash XM.com (Mappati su Yahoo Finance)
    "GER40CASH#": "^GDAXI", "GER40CASH": "^GDAXI", "GER40": "^GDAXI",
    "US100CASH#": "^IXIC", "US100CASH": "^IXIC", "US100": "^IXIC",
    "US30CASH#": "^DJI", "US30CASH": "^DJI", "US30": "^DJI",
    "US500CASH#": "^GSPC", "US500CASH": "^GSPC", "US500": "^GSPC",
    
    # Criptovalute XM.com
    "BTCUSD#": "BTC-USD", "BTCUSD": "BTC-USD",
    "ETHUSD#": "ETH-USD", "ETHUSD": "ETH-USD"
}

# --- LISTA DI SCANSIONE COMPLETA SPECIFICA XM.COM ---
ASSET_SCAN_LIST = [
    # Forex Majors
    "EURUSD#", "GBPUSD#", "USDJPY#", "AUDUSD#", "USDCAD#",
    # Forex Crosses
    "GBPJPY#", "EURJPY#", "EURAUD#", "EURGBP#", "GBPAUD#",
    # Metalli & Energie
    "GOLD#", "SILVER#", "OILCash#",
    # Indici Cash principali XM
    "GER40Cash#", "US100Cash#", "US30Cash#", "US500Cash#",
    # Crypto
    "BTCUSD#", "ETHUSD#"
]

def ripulisci_nome_ticker(ticker_raw):
    nome = ticker_raw.strip().upper()
    for chiave_xm, valore_yf in MAPPATURA_ASSET.items():
        if valore_yf == nome or chiave_xm == nome:
            return chiave_xm
    if nome.endswith("=X"): return nome.replace("=X", "#")
    if nome.endswith("-USD"): return nome.replace("-USD", "USD#")
    return nome

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "🤖 **QUANTUM ENGINE XM.COM PRONTO.**\n\nHo allineato i database con i contratti del broker **XM.com** (compresi indici cash ed asset con suffisso `#`).\n\n👉 Chiedimi di **'trovare un'opportunità'** per scansionare il mercato di XM!"}
    ]

if "last_fig" not in st.session_state:
    st.session_state.last_fig = None
if "last_metriche" not in st.session_state:
    st.session_state.last_metriche = None
if "last_asset" not in st.session_state:
    st.session_state.last_asset = ""

col_chat, col_grafico = st.columns([1, 2])

with col_chat:
    st.markdown("### 📡 CORE CONSOLE")
    chat_container = st.container(height=520)
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

def esegui_analisi_mtf(ticker_utente):
    ticker_pulito = ticker_utente.strip().upper().replace(" ", "").replace("/", "").replace("-", "")
    ticker_yf = MAPPATURA_ASSET.get(ticker_pulito, ticker_pulito)
    
    if len(ticker_pulito) == 6 and ticker_pulito.isalpha() and ticker_pulito not in MAPPATURA_ASSET:
        ticker_yf = ticker_pulito + "=X"

    ticker_bello = ripulisci_nome_ticker(ticker_yf)

    try:
        df_15m = yf.download(ticker_yf, period="5d", interval="15m", progress=False)
        df_1h = yf.download(ticker_yf, period="30d", interval="1h", progress=False)
        df_4h = yf.download(ticker_yf, period="60d", interval="4h", progress=False)

        if df_15m.empty or df_1h.empty or df_4h.empty:
            return None, f"❌ ERRORE: Asset XM.com '{ticker_bello}' non trovato.", None

        for df in [df_15m, df_1h, df_4h]:
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.droplevel(1)

        # 4H TREND
        df_4h['EMA_50'] = df_4h['Close'].ewm(span=50, adjust=False).mean()
        last_close_4h = float(df_4h['Close'].iloc[-1])
        last_ema_4h = float(df_4h['EMA_50'].iloc[-1])
        trend_macro = "RIALZISTA" if last_close_4h > last_ema_4h else "RIBASSISTA"

        # 1H TREND
        df_1h['EMA_50'] = df_1h['Close'].ewm(span=50, adjust=False).mean()
        last_close_1h = float(df_1h['Close'].iloc[-1])
        last_ema_1h = float(df_1h['EMA_50'].iloc[-1])
        trend_medio = "RIALZISTA" if last_close_1h > last_ema_1h else "RIBASSISTA"

        # 15M TRIGGER
        df_15m['SMA_20'] = df_15m['Close'].rolling(window=20).mean()
        std_dev_15m = df_15m['Close'].rolling(window=20).std()
        df_15m['Bollinger_High'] = df_15m['SMA_20'] + (std_dev_15m * 2)
        df_15m['Bollinger_Low'] = df_15m['SMA_20'] - (std_dev_15m * 2)
        df_15m['EMA_50'] = df_15m['Close'].ewm(span=50, adjust=False).mean()

        # RSI
        delta_15m = df_15m['Close'].diff()
        gain_15m = (delta_15m.where(delta_15m > 0, 0)).rolling(window=14).mean()
        loss_15m = (-delta_15m.where(delta_15m < 0, 0)).rolling(window=14).mean()
        rs_15m = gain_15m / loss_15m
        df_15m['RSI'] = 100 - (100 / (1 + rs_15m))
        
        # ATR
        high_low = df_15m['High'] - df_15m['Low']
        high_close = (df_15m['High'] - df_15m['Close'].shift()).abs()
        low_close = (df_15m['Low'] - df_15m['Close'].shift()).abs()
        df_15m['TR'] = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        df_15m['ATR'] = df_15m['TR'].rolling(window=14).mean()

        last_price_15m = float(df_15m['Close'].iloc[-1])
        last_rsi_15m = float(df_15m['RSI'].iloc[-1]) if not pd.isna(df_15m['RSI'].iloc[-1]) else 50.0
        last_atr_15m = float(df_15m['ATR'].iloc[-1]) if not pd.isna(df_15m['ATR'].iloc[-1]) else 0.0
        last_b_high = float(df_15m['Bollinger_High'].iloc[-1])
        last_b_low = float(df_15m['Bollinger_Low'].iloc[-1])

        # Fibonacci
        massimo_swing = float(df_15m['High'].max())
        minimo_swing = float(df_15m['Low'].min())
        diff_fib = massimo_swing - minimo_swing
        fib_50 = massimo_swing - (diff_fib * 0.50)
        fib_618 = massimo_swing - (diff_fib * 0.618)

        # SMC Order Block
        ob_tipo = "Nessuno"
        ob_prezzo = 0.0
        for i in range(len(df_15m) - 2, len(df_15m) - 40, -1):
            open_c, close_c = df_15m['Open'].iloc[i], df_15m['Close'].iloc[i]
            open_p, close_p = df_15m['Open'].iloc[i-1], df_15m['Close'].iloc[i-1]
            if close_p < open_p and close_c > open_c and close_c > open_p:
                ob_tipo = "Bullish OB"
                ob_prezzo = float(df_15m['Low'].iloc[i-1])
                break
            elif close_p > open_p and close_c < open_c and close_c < open_p:
                ob_tipo = "Bearish OB"
                ob_prezzo = float(df_15m['High'].iloc[i-1])
                break

        # Volume Profile POC
        p_min, p_max = float(df_15m['Close'].min()), float(df_15m['Close'].max())
        step = (p_max - p_min) / 15
        fasce, volumi = [], []
        for i in range(15):
            f_inf = p_min + (i * step)
            f_sup = f_inf + step
            vol_sum = df_15m[(df_15m['Close'] >= f_inf) & (df_15m['Close'] < f_sup)]['Volume'].sum()
            fasce.append((f_inf, f_sup))
            volumi.append(float(vol_sum))
        poc_prezzo = (fasce[np.argmax(volumi)][0] + fasce[np.argmax(volumi)][1]) / 2

        # LOGICA OPERATIVA
        allineato = (trend_macro == trend_medio)
        direzione = "NEUTRALE"
        win_rate = 50.0
        setup_desc = "Timeframe disallineati o nessuna zona di reazione rilevata."

        if allineato:
            vicino_fib = (last_price_15m >= fib_618) and (last_price_15m <= fib_50)
            vicino_ob = abs(last_price_15m - ob_prezzo) < (last_atr_15m * 0.4) if ob_prezzo > 0 else False

            if trend_macro == "RIALZISTA":
                if vicino_fib:
                    direzione = "BUY"
                    win_rate = 87.0
                    setup_desc = "Confluenza: Fibonacci Golden Zone + Allineamento Bullish MTF"
                elif ob_tipo == "Bullish OB" and vicino_ob:
                    direzione = "BUY"
                    win_rate = 89.5
                    setup_desc = "SMC Confluenza: Reazione su Order Block Istituzionale H15"
                elif last_price_15m < last_b_low:
                    direzione = "BUY"
                    win_rate = 78.0
                    setup_desc = "Eccesso: Prezzo sotto la Banda Inferiore di Bollinger"
            else:
                if vicino_fib:
                    direzione = "SELL"
                    win_rate = 87.0
                    setup_desc = "Confluenza: Fibonacci Golden Zone + Allineamento Bearish MTF"
                elif ob_tipo == "Bearish OB" and vicino_ob:
                    direzione = "SELL"
                    win_rate = 89.5
                    setup_desc = "SMC Confluenza: Reazione su Order Block Istituzionale H15"
                elif last_price_15m > last_b_high:
                    direzione = "SELL"
                    win_rate = 78.0
                    setup_desc = "Eccesso: Prezzo sopra la Banda Superiore di Bollinger"

        metriche = {
            "price": last_price_15m,
            "trend_4h": trend_macro,
            "trend_1h": trend_medio,
            "rsi_15m": last_rsi_15m,
            "atr_15m": last_atr_15m,
            "direzione": direzione,
            "win_rate": win_rate,
            "condizione": setup_desc,
            "poc": poc_prezzo,
            "ob_prezzo": ob_prezzo,
            "ob_tipo": ob_tipo
        }

        if direzione != "NEUTRALE":
            # Determinazione del valore del pip in base all'asset
            if "GOLD" in ticker_bello or "XAU" in ticker_bello:
                pip_distanza = 10.0 # Per l'oro, 100 pips sono 10.0 punti
            elif "CASH" in ticker_bello or "US" in ticker_bello or "GER" in ticker_bello:
                pip_distanza = 80.0 # Per gli indici, puntiamo a 80 punti
            else:
                pip_distanza = 0.0090 # Per il forex standard, 90 pips (0.0090)

            tp = last_price_15m + pip_distanza if direzione == "BUY" else last_price_15m - pip_distanza
            sl = last_price_15m - (pip_distanza * 0.5) if direzione == "BUY" else last_price_15m + (pip_distanza * 0.5)
            
            # (Il resto del codice rimane invariato...)
            output_testo = (
                f"📡 **ANALISI CONCLUSA SU {ticker_bello}**\n\n"
                f"🚨 **STATO TRIGGER:** {badge}\n"
                f"🛡️ **SETUP:** *{setup_desc}*\n\n"
                f"🎯 **PARAMETRI OPERATIVI XM.COM:**\n"
                f"- **PREZZO D'INGRESSO:** `{last_price_15m:.5f}`\n"
                f"- **🎯 TARGET (TP):** `{tp:.5f}`\n"
                f"- **🛑 PROTEZIONE (SL):** `{sl:.5f}`\n\n"
                f"📐 **CONFLUENZE TECNICHE (15M):**\n"
                f"- **Volume Profile (POC):** `{poc_prezzo:.5f}`\n"
                f"- **Area Fibo:** `{fib_618:.5f}` - `{fib_50:.5f}`\n"
                f"- **Order Block:** *{ob_tipo}* a `{ob_prezzo:.5f}`"
            )
        else:
            badge = "<span class='signal-glow-neutral'>SISTEMA IN STANDBY (FLAT)</span>"
            output_testo = (
                f"📡 **ANALISI CONCLUSA SU {ticker_bello}**\n\n"
                f"🚨 **STATO TRIGGER:** {badge}\n"
                f"🛡️ **SETUP:** *{setup_desc}*\n\n"
                f"📊 Struttura non sbilanciata. Non ci sono confluenze ottimali in questo momento."
            )

        # PLOT
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05, row_width=[0.22, 0.78])

        fig.add_trace(dict_plot.Candlestick(
            x=df_15m.index, open=df_15m['Open'], high=df_15m['High'], low=df_15m['Low'], close=df_15m['Close'],
            name=f"{ticker_bello} 15M",
            increasing_line_color='#00ff87', decreasing_line_color='#ff0055',
            increasing_fillcolor='rgba(0, 255, 135, 0.4)', decreasing_fillcolor='rgba(255, 0, 85, 0.4)'
        ), row=1, col=1)

        fig.add_trace(dict_plot.Scatter(
            x=df_15m.index, y=df_15m['EMA_50'], line=dict(color='#00f2fe', width=2), name="EMA 50 (15M)"
        ), row=1, col=1)

        fig.add_trace(dict_plot.Scatter(
            x=df_15m.index, y=df_15m['Bollinger_High'], line=dict(color='rgba(168, 85, 247, 0.25)', width=1, dash='dash'), name="BB High"
        ), row=1, col=1)
        fig.add_trace(dict_plot.Scatter(
            x=df_15m.index, y=df_15m['Bollinger_Low'], line=dict(color='rgba(168, 85, 247, 0.25)', width=1, dash='dash'), name="BB Low"
        ), row=1, col=1)

        fig.add_hline(y=fib_50, line_dash="dot", line_color="rgba(0, 242, 254, 0.6)", annotation_text="Fib 0.50", row=1, col=1)
        fig.add_hline(y=fib_618, line_dash="dot", line_color="rgba(0, 242, 254, 0.6)", annotation_text="Fib 0.618", row=1, col=1)
        fig.add_hline(y=poc_prezzo, line_dash="solid", line_color="#ff0055", line_width=2, annotation_text="POC", row=1, col=1)

        if ob_prezzo > 0:
            color_ob = "#00ff87" if "Bullish" in ob_tipo else "#ff0055"
            fig.add_hline(y=ob_prezzo, line_dash="dash", line_color=color_ob, line_width=2, annotation_text=f"SMC {ob_tipo}", row=1, col=1)

        fig.add_trace(dict_plot.Scatter(
            x=df_15m.index, y=df_15m['RSI'], line=dict(color='#a855f7', width=2), name="RSI (15M)"
        ), row=2, col=1)
        fig.add_hline(y=70, line_dash="dash", line_color="#ff0055", line_width=1, row=2, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="#00ff87", line_width=1, row=2, col=1)

        fig.update_layout(
            xaxis_rangeslider_visible=False,
            height=600,
            template="plotly_dark",
            paper_bgcolor='rgba(7, 9, 14, 0.95)',
            plot_bgcolor='rgba(7, 9, 14, 0.95)',
            margin=dict(l=15, r=15, t=15, b=15),
            xaxis=dict(gridcolor='rgba(255, 255, 255, 0.03)'),
            yaxis=dict(gridcolor='rgba(255, 255, 255, 0.03)'),
            xaxis2=dict(gridcolor='rgba(255, 255, 255, 0.03)'),
            yaxis2=dict(gridcolor='rgba(255, 255, 255, 0.03)')
        )

        return fig, output_testo, metriche

    except Exception as e:
        return None, f"❌ ERRORE CRITICO: {str(e)}", None

# --- NUOVO LAYOUT CON PULSANTE RAPIDO ---
col_input, col_cerca, col_rapido = st.columns([3, 1, 1])

with col_input:
    user_query = st.text_input("Inserisci asset:", placeholder="Es: EURUSD#")

with col_cerca:
    st.write("") # Spazio per allineamento
    st.write("")
    cerca_premut = st.button("🚀 CERCA")

with col_rapido:
    st.write("") # Spazio per allineamento
    st.write("")
    # Questo è il pulsante magico che scrive per te
    if st.button("🔍 SCAN"):
        user_query = "trovami un'opportunità"


# --- LOGICA DI ATTIVAZIONE (UNICA, NON DUPLICARE) ---
if user_query or cerca_premut:
    with col_chat:
        with st.chat_message("user"):
            st.markdown(user_query)
        st.session_state.messages.append({"role": "user", "content": user_query})

# ... (il resto del codice originale che segue, come la pulizia della query)


    
    # Pulizia avanzata anti-bug per rimuovere punteggiatura e apostrofi
    query_clean = user_query.strip().lower()
    for char in ["'", "’", ",", ".", "!", "?", "-"]:
        query_clean = query_clean.replace(char, " ")
    
    parole_chiave_scan = ["opportunita", "opportunità", "oppurtunita", "oppurtunità", "trova", "cerca", "scan", "trade", "segnala"]
    
    # --- LOGICA DI SCANSIONE AUTOMATICA XM.COM ---
    if any(keyword in query_clean for keyword in parole_chiave_scan):
        with col_chat:
            # Creazione barra di progresso dinamica nell'interfaccia
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            opportunita_trovata = False
            totale_asset = len(ASSET_SCAN_LIST)
            
            for index, asset in enumerate(ASSET_SCAN_LIST):
                percentuale = int(((index + 1) / totale_asset) * 100)
                progress_bar.progress(percentuale)
                status_text.markdown(f"🔬 Scansione quantica XM in corso: **{asset}** ({percentuale}%)")
                
                fig, risposta, metriche = esegui_analisi_mtf(asset)
                
                # Se troviamo un setup valido attivo (BUY o SELL) con WR alto, lo blocchiamo subito
                if metriche and metriche["direzione"] != "NEUTRALE" and metriche["win_rate"] >= 75.0:
                    st.session_state.last_fig = fig
                    st.session_state.last_metriche = metriche
                    st.session_state.last_asset = asset
                    opportunita_trovata = True
                    
                    risposta_finale = f"🎯 **OPPORTUNITÀ RILEVATA CON SUCCESSO!**\n\nHo scansionato i mercati XM.com e individuato questo sbilanciamento volumetrico su **{asset}**:\n\n" + risposta
                    break
                
                # Piccola pausa per stabilizzare le API yfinance durante il ciclo veloce
                time.sleep(0.1)
                
            # Pulizia indicatori di caricamento
            progress_bar.empty()
            status_text.empty()
                
            if not opportunita_trovata:
                risposta_finale = "🔍 **SCANSIONE GLOBALE XM.COM COMPLETATA.**\n\nNessuno dei mercati scansionati presenta un'anomalia strutturale o un allineamento ottimale in questo esatto momento. **Strategia consigliata: FLAT (Attendi la prossima sessione)**."
                st.session_state.last_fig = None
                st.session_state.last_metriche = None
                st.session_state.last_asset = ""

        with col_chat:
            with st.chat_message("assistant"):
                st.markdown(risposta_finale)
        # BUG RISOLTO: Ora richiama correttamente 'risposta_finale' con la 'i'
        st.session_state.messages.append({"role": "assistant", "content": risposta_finale})
        
    else:
        # Analisi su singolo asset
        fig, risposta, metriche = esegui_analisi_mtf(user_query)
        
        if metriche is not None:
            st.session_state.last_fig = fig
            st.session_state.last_metriche = metriche
            st.session_state.last_asset = ripulisci_nome_ticker(MAPPATURA_ASSET.get(user_query.strip().upper(), user_query))
        
        with col_chat:
            with st.chat_message("assistant"):
                st.markdown(risposta)
        st.session_state.messages.append({"role": "assistant", "content": risposta})

# --- RENDER PANNELLO GRAFICO (Sulla Destra) ---
if st.session_state.last_fig is not None and st.session_state.last_metriche is not None:
    metriche = st.session_state.last_metriche
    fig = st.session_state.last_fig
    asset_corrente = st.session_state.last_asset
    
    with col_grafico:
        st.markdown(f"### 🚀 XM.COM LIVE PANEL • {asset_corrente}")
        
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        
        # 1. Macro Trend (4H)
        style_4h = "card-green" if metriche['trend_4h'] == "RIALZISTA" else "card-red"
        color_txt_4h = "#10b981" if metriche['trend_4h'] == "RIALZISTA" else "#ef4444"
        with col_m1:
            st.markdown(f"""
                <div class="neon-card {style_4h}">
                    <span style="color: #ffffff; font-size: 0.8rem; font-weight:bold;">MACRO TREND (4H)</span>
                    <h3 style="margin: 8px 0px 0px 0px; color: {color_txt_4h} !important; text-shadow: 0 0 10px {color_txt_4h}80;">{metriche['trend_4h']}</h3>
                </div>
            """, unsafe_allow_html=True)
            
        # 2. Medium Trend (1H)
        style_1h = "card-green" if metriche['trend_1h'] == "RIALZISTA" else "card-red"
        color_txt_1h = "#10b981" if metriche['trend_1h'] == "RIALZISTA" else "#ef4444"
        with col_m2:
            st.markdown(f"""
                <div class="neon-card {style_1h}">
                    <span style="color: #ffffff; font-size: 0.8rem; font-weight:bold;">MEDIUM TREND (1H)</span>
                    <h3 style="margin: 8px 0px 0px 0px; color: {color_txt_1h} !important; text-shadow: 0 0 10px {color_txt_1h}80;">{metriche['trend_1h']}</h3>
                </div>
            """, unsafe_allow_html=True)
            
        # 3. RSI 15M (Glow Viola)
        with col_m3:
            st.markdown(f"""
                <div class="neon-card card-purple">
                    <span style="color: #ffffff; font-size: 0.8rem; font-weight:bold;">MOMENTUM RSI (15M)</span>
                    <h3 style="margin: 8px 0px 0px 0px; color: #a855f7 !important; text-shadow: 0 0 10px rgba(168, 85, 247, 0.6);">{metriche['rsi_15m']:.1f}</h3>
                </div>
            """, unsafe_allow_html=True)
            
        # 4. Volatilità ATR (Glow Azzurro)
        with col_m4:
            st.markdown(f"""
                <div class="neon-card" style="border-left: 4px solid #00f2fe; box-shadow: 0 4px 20px rgba(0, 242, 254, 0.05);">
                    <span style="color: #ffffff; font-size: 0.8rem; font-weight:bold;">VOLATILITY ATR</span>
                    <h3 style="margin: 8px 0px 0px 0px; color: #00f2fe !important; text-shadow: 0 0 10px rgba(0, 242, 254, 0.6);">{metriche['atr_15m']:.5f}</h3>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)