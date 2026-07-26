import base64
import json
import io
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from openai import OpenAI

# 1. Inizializzazione del client API (assicurati di inserire la tua API Key nei Secrets di Streamlit o come variabile d'ambiente)
client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY", "IL_TUO_API_KEY_HERE"))

st.set_page_config(page_title="Trading Chart AI Analyzer", layout="wide")
st.title("📈 AI Chart Analyzer & Annotator")
st.write("Carica lo screenshot del tuo grafico per ricevere l'analisi visiva, i livelli di trading e le annotazioni sulle zone chiave.")

# 2. Funzione per convertire l'immagine in Base64 per l'API Vision
def encode_image(image_bytes):
    return base64.b64encode(image_bytes).decode('utf-8')

# 3. Funzione per disegnare le annotazioni sul grafico
def annotate_chart(original_image, annotations):
    img = original_image.convert("RGBA")
    draw = ImageDraw.Draw(img)
    width, height = img.size

    # Disegno delle Bounding Box/Zone (es. Order Blocks, FVG, Liquidity)
    for box in annotations.get("boxes", []):
        # Convertiamo le coordinate percentuali (0-100) in pixel reali
        ymin, xmin, ymax, xmax = box["box_2d"]
        left = (xmin / 100.0) * width
        top = (ymin / 100.0) * height
        right = (xmax / 100.0) * width
        bottom = (ymax / 100.0) * height
        
        label = box.get("label", "")
        color = box.get("color", "yellow") # e.g. green per demand, red per supply

        # Disegno del rettangolo della zona
        draw.rectangle([left, top, right, bottom], outline=color, width=3)
        # Etichetta di testo
        draw.text((left + 5, top + 5), label, fill=color)

    # Disegno dei livelli di prezzo (Entry, SL, TP)
    for line in annotations.get("price_lines", []):
        y_percent = line["y_position_percent"]
        y_pixel = (y_percent / 100.0) * height
        label = line.get("label", "")
        color = line.get("color", "white")

        # Linea orizzontale
        draw.line([(0, y_pixel), (width, y_pixel)], fill=color, width=2)
        # Testo accanto alla linea
        draw.text((10, y_pixel - 15), label, fill=color)

    return img.convert("RGB")

# 4. Uploader Immagine
uploaded_file = st.file_uploader("Carica lo screenshot del grafico (PNG, JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    col1, col2 = st.columns(2)
    
    # MOSTRA GRAFICO ORIGINALE
    image = Image.open(uploaded_file)
    with col1:
        st.subheader("Grafico Originale")
        st.image(image, use_column_width=True)

    analyze_button = st.button("🔍 Analizza e Annotato Grafico", type="primary")

    if analyze_button:
        with st.spinner("L'IA sta analizzando la struttura di mercato e calcolando i livelli..."):
            # Preparazione immagine per API
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format=image.format or 'PNG')
            base64_image = encode_image(img_byte_arr.getvalue())

            # Prompt di sistema per forzare l'output in JSON con coordinate visive
            system_prompt = """
            Sei un analista tecnico esperto di trading (Smart Money Concepts / Price Action).
            Analizza l'immagine del grafico fornita ed estrai le informazioni in formato JSON strutturato.
            
            Devi restituire un oggetto JSON con questa struttura esatta:
            {
                "trade_setup": {
                    "asset": "String (es. XAUUSD, EURUSD)",
                    "direction": "BUY" o "SELL",
                    "entry_price": "float o stringa",
                    "stop_loss": "float o stringa",
                    "take_profit": "float o stringa",
                    "risk_reward": "stringa (es. 1:2.5)"
                },
                "analysis_text": "Spiegazione dettagliata dell'analisi (BOS, CHoCH, Zone di Domanda/Offerta, Liquida, Volume Profile).",
                "boxes": [
                    {
                        "label": "Nome Zona (es. Demand Zone M15 / Order Block / FVG)",
                        "box_2d": [ymin, xmin, ymax, xmax],  # coordinate percentuali da 0 a 100
                        "color": "green" (per zone buyer/demand) o "red" (per offerta/supply) o "yellow"
                    }
                ],
                "price_lines": [
                    {
                        "label": "ENTRY @ ...",
                        "y_position_percent": float (da 0 a 100 indicante l'altezza della linea),
                        "color": "blue"
                    },
                    {
                        "label": "STOP LOSS @ ...",
                        "y_position_percent": float,
                        "color": "red"
                    },
                    {
                        "label": "TAKE PROFIT @ ...",
                        "y_position_percent": float,
                        "color": "green"
                    }
                ]
            }
            Rispondi ESCLUSIVAMENTE in formato JSON privo di testo extra o blocchi di codice markdown.
            """

            try:
                # Chiamata all'API Vision
                response = client.chat.completions.create(
                    model="gpt-4o",  # Modello multimodale con vision
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": "Analizza questo grafico e fornisci il JSON per l'annotazione."},
                                {
                                    "type": "image_url",
                                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                                }
                            ]
                        }
                    ],
                    response_format={"type": "json_object"},
                    max_tokens=1500
                )

                # Parsing del JSON restituito dall'IA
                analysis_data = json.loads(response.choices[0].message.content)

                # Generazione Immagine Annotata
                annotated_img = annotate_chart(image, analysis_data)

                # MOSTRA RISULTATI
                with col2:
                    st.subheader("Grafico Annotato dall'IA")
                    st.image(annotated_img, use_column_width=True)

                st.markdown("---")
                st.subheader("📊 Scheda Operativa e Analisi Tecnica")
                
                # Tabella o Metriche per i livelli
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
                st.error(f"Errore durante l'elaborazione dell'analisi: {e}")
