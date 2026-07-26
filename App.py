import json
import io
import streamlit as st
from PIL import Image, ImageDraw
from google import genai
from google.genai import types

# 1. Inizializzazione Client Google AI Studio (Gratuito)
api_key = st.secrets.get("GEMINI_API_KEY", "")

st.set_page_config(page_title="Free Trading Chart Analyzer", layout="wide")
st.title("📈 AI Chart Analyzer (Versione Gratuita Gemini)")
st.write("Carica lo screenshot del tuo grafico per ricevere l'analisi visiva, i livelli di trading e le annotazioni sulle zone chiave senza costi.")

# 2. Funzione per disegnare le annotazioni sul grafico
def annotate_chart(original_image, annotations):
    img = original_image.convert("RGBA")
    draw = ImageDraw.Draw(img)
    width, height = img.size

    # Disegno delle Bounding Box (Order Blocks, FVG, Liquidity)
    for box in annotations.get("boxes", []):
        ymin, xmin, ymax, xmax = box.get("box_2d", [0, 0, 0, 0])
        left = (xmin / 100.0) * width
        top = (ymin / 100.0) * height
        right = (xmax / 100.0) * width
        bottom = (ymax / 100.0) * height
        
        label = box.get("label", "")
        color = box.get("color", "yellow")

        draw.rectangle([left, top, right, bottom], outline=color, width=3)
        draw.text((left + 5, top + 5), label, fill=color)

    # Disegno dei livelli di prezzo (Entry, SL, TP)
    for line in annotations.get("price_lines", []):
        y_percent = line.get("y_position_percent", 50)
        y_pixel = (y_percent / 100.0) * height
        label = line.get("label", "")
        color = line.get("color", "white")

        draw.line([(0, y_pixel), (width, y_pixel)], fill=color, width=2)
        draw.text((10, y_pixel - 15), label, fill=color)

    return img.convert("RGB")

# 3. Caricamento Immagine
uploaded_file = st.file_uploader("Carica lo screenshot del grafico (PNG, JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    col1, col2 = st.columns(2)
    image = Image.open(uploaded_file)
    
    with col1:
        st.subheader("Grafico Originale")
        st.image(image, use_column_width=True)

    if st.button("🔍 Analizza Gratis con Gemini AI", type="primary"):
        if not api_key:
            st.error("Inserisci la GEMINI_API_KEY nei Secrets di Streamlit!")
        else:
            with st.spinner("Gemini sta analizzando la struttura del grafico..."):
                try:
                    client = genai.Client(api_key=api_key)

                    prompt = """
                    Sei un analista tecnico esperto di trading (Smart Money Concepts / Price Action).
                    Analizza questo grafico ed estrai le informazioni in formato JSON strutturato.
                    
                    Restituisci questo oggetto JSON:
                    {
                        "trade_setup": {
                            "direction": "BUY" o "SELL",
                            "entry_price": "valore",
                            "stop_loss": "valore",
                            "take_profit": "valore",
                            "risk_reward": "es. 1:2.5"
                        },
                        "analysis_text": "Spiegazione dettagliata dell'analisi (BOS, CHoCH, Zone di Domanda/Offerta, Liquida, Volume Profile).",
                        "boxes": [
                            {
                                "label": "Nome Zona (es. Demand Zone / Order Block)",
                                "box_2d": [ymin, xmin, ymax, xmax],  # percentuali da 0 a 100
                                "color": "green" o "red" o "yellow"
                            }
                        ],
                        "price_lines": [
                            {"label": "ENTRY @ ...", "y_position_percent": 50.0, "color": "blue"},
                            {"label": "STOP LOSS @ ...", "y_position_percent": 70.0, "color": "red"},
                            {"label": "TAKE PROFIT @ ...", "y_position_percent": 20.0, "color": "green"}
                        ]
                    }
                    """

                    # Chiamata API Gratuita al modello visivo di Gemini
                    response = client.models.generate_content(
                        model='gemini-1.5-flash',
                        contents=[image, prompt],
                        config=types.GenerateContentConfig(
                            response_mime_type="application/json"
                        )
                    )

                    analysis_data = json.loads(response.text)
                    annotated_img = annotate_chart(image, analysis_data)

                    with col2:
                        st.subheader("Grafico Annotato dall'IA")
                        st.image(annotated_img, use_column_width=True)

                    st.markdown("---")
                    st.subheader("📊 Scheda Operativa e Analisi Tecnica")
                    
                    setup = analysis_data.get("trade_setup", {})
                    m1, m2, m3, m4, m5 = st.columns(5)
                    m1.metric("Direzione", setup.get("direction", "N/A"))
                    m2.metric("Entry", setup.get("entry_price", "N/A"))
                    m3.metric("Stop Loss", setup.get("stop_loss", "N/A"))
                    m4.metric("Take Profit", setup.get("take_profit", "N/A"))
                    m5.metric("Rischio/Rendimento", setup.get("risk_reward", "N/A"))

                    st.write("**Spiegazione del Setup:**")
                    st.info(analysis_data.get("analysis_text", "Nessuna spiegazione fornita."))

                except Exception as e:
                    st.error(f"Errore durante l'elaborazione: {e}")
