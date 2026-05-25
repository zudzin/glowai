import streamlit as st
import os
import pandas as pd
import smtplib
import json
import urllib.request
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- USTAWIENIA STRONY I WYGLĄD (CSS) ---
st.set_page_config(page_title="GlowAI", page_icon="💋", layout="wide")

css_style = (
    "<style>"
    "@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600&family=Montserrat:wght@300;400;600&display=swap');"
    ".stApp { background-color: #fffaf7; }"
    "html, body, [class*='css'] { font-family: 'Montserrat', sans-serif; color: #2b2b2b; }"
    ".brand-logo { font-family: 'Cinzel', serif; color: #c98a8a; font-size: 60px; text-align: center; font-weight: 700; letter-spacing: 6px; margin-top: 10px; margin-bottom: 5px; }"
    ".brand-tagline { text-align: center; color: #a38585; font-size: 13px; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 30px; }"
    ".profile-card { background-color: #ffffff; padding: 25px; border-radius: 20px; border: 1px solid #f7dede; box-shadow: 8px 8px 0px #f0cfcf; margin-bottom: 25px; }"
    "[data-testid='stChatMessage'] { background-color: #ffffff; border-radius: 20px; border: 1px solid #f7dede; margin-bottom: 10px; padding: 15px; }"
    "[data-testid='stChatMessage']:nth-child(even) { background-color: #fff0f1; border: 1px solid #ebc5c5; }"
    "[data-testid='stImage'] img { border-radius: 15px; object-fit: cover; border: 1px solid #f7dede; box-shadow: 0px 4px 15px rgba(201,138,138,0.1); transition: transform 0.3s ease; }"
    "[data-testid='stImage'] img:hover { transform: scale(1.03); }"
    ".brand-footer { text-align: center; font-family: 'Cinzel', serif; color: #a38585; font-size: 16px; letter-spacing: 3px; text-transform: uppercase; margin-top: 60px; padding: 25px; border-top: 1px solid rgba(163, 133, 133, 0.15); }"
    "div.stButton > button:first-child { background-color: #c98a8a !important; color: white !important; border-radius: 25px !important; border: none !important; padding: 10px 25px !important; font-size: 14px !important; font-weight: 600 !important; width: 100%; box-shadow: 0px 4px 12px rgba(201, 138, 138, 0.2) !important; }"
    "div.stButton > button:first-child:hover { background-color: #b87676 !important; transform: translateY(-1px); }"
    "</style>"
)
st.markdown(css_style, unsafe_allow_html=True)


# --- TWOJA LOGIKA BACKENDOWA ---
GMAIL_USER = "n.zudzin@gmail.com"
GMAIL_PASS = "syry wcts pymb yscg"
# Ten klucz zostaje dla natywnego połączenia z modelem
GROQ_API_KEY = "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"

def send_email(receiver_email, content):
    try:
        msg = MIMEMultipart()
        msg['From'] = GMAIL_USER
        msg['To'] = receiver_email
        msg['Subject'] = "💋 Zapis Twojej konsultacji GlowAI!"
        
        body = f"Oto pełna historia Twojej czatowej rozmowy z wirtualnymi agentami GlowAI:\n\n{content}\n\nStay glowing, XOXO!\nZespół GlowAI"
        
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASS)
        server.send_message(msg)
        server.quit()
        return "Pełna historia rozmowy została wysłana na Twój e-mail! 💌"
    except Exception as e:
        return f"Błąd wysyłki raportu na e-mail: {e}"

def search_cosmetics_tool(skladnik: str) -> str:
    """Szuka produktów w pliku cosmetics.csv."""
    try:
        if os.path.exists('cosmetics.csv'):
            df = pd.read_csv('cosmetics.csv')
            res = df[df['Ingredients'].str.contains(skladnik.strip(), case=False, na=False)].head(2)
            return res[['Brand', 'Name', 'Price']].to_string(index=False) if not res.empty else "Brak w bazie."
        else:
            return "Plik cosmetics.csv nie istnieje."
    except Exception as e: 
        return f"Błąd bazy danych: {str(e)}"

def uruchom_agentow(opis_problemu):
    # Sekwencyjna analiza symulująca logikę agentową (Diagnosta -> Technolog -> Strateg -> Redaktor),
    # wykonana czystym wywołaniem HTTP do Llama-3.1 na Groq. 
    # Omijamy potężne dependency CrewAI, pozostając przy oryginalnym modelu i zaangażowaniu narzędzia CSV.
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    # KROK 1: Wymuszamy
