import streamlit as st
import os
import pandas as pd
import smtplib
import json
import urllib.request
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- USTAWIENIA STRONY I WYGLĄD (CSS) ---
st.set_page_config(page_title="GlowAI x Gossip Girl", page_icon="💋", layout="wide")

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
    
    # KROK 1: Wymuszamy na modelu podanie kluczowego składnika na podstawie opisu użytkownika.
    step1_messages = [
        {"role": "system", "content": "Jesteś Diagnostą skóry. Na podstawie opisu wskaż *jeden* główny składnik aktywny (po angielsku), którego potrzebuje ta skóra. Odpowiedz WYŁĄCZNIE nazwą składnika (np. Ceramides, Hyaluronic Acid, Salicylic Acid, Glycerin)."},
        {"role": "user", "content": opis_problemu}
    ]
    
    data1 = {"model": "llama-3.1-8b-instant", "messages": step1_messages, "temperature": 0.1}
    skladnik = "Hyaluronic Acid" # Domyślny fallback
    try:
        req = urllib.request.Request(url, data=json.dumps(data1).encode('utf-8'))
        req.add_header('Content-Type', 'application/json')
        req.add_header('Authorization', f'Bearer {GROQ_API_KEY}')
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode('utf-8'))
            skladnik = res['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Krok 1 error: {e}")
        pass
    
    # KROK 2: Użycie narzędzia narzędzia (Technolog)
    wynik_bazy = search_cosmetics_tool(skladnik)
    
    # KROK 3: Ostateczna synteza i ocena (Redaktor + Strateg) w stylu Gossip Girl
    final_prompt = (
        f"Użytkownik ma problem: {opis_problemu}. "
        f"Jako zespół ekspertów zalecasz główny składnik: {skladnik}. "
        f"Oto co znalazł Twój Technolog w bazie (Marka, Nazwa, Cena): {wynik_bazy}. "
        f"Teraz wciel się w rolę głównego redaktora (w stylu luksusowej 'Gossip Girl', używając 💋 i ✨). "
        f"Zdiagnozuj problem, wspomnij o opłacalności produktów z bazy i napisz zwięzłą, ciepłą poradę pielęgnacyjną."
    )
    
    final_messages = [{"role": "user", "content": final_prompt}]
    data2 = {"model": "llama-3.1-8b-instant", "messages": final_messages, "temperature": 0.4}
    try:
        req = urllib.request.Request(url, data=json.dumps(data2).encode('utf-8'))
        req.add_header('Content-Type', 'application/json')
        req.add_header('Authorization', f'Bearer {GROQ_API_KEY}')
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode('utf-8'))
            return res['choices'][0]['message']['content']
    except Exception as e:
         return (
            "💋 Ojej, Moi agenci chyba poszli na kawkę, bo serwery Groqa rzucają błędem uwierzytelniania! "
            "Twój klucz API najprawdopodobniej został ograniczony przez systemy zabezpieczające platformy. Sprawdź go, kochana! ✨"
        )


# --- INTERFEJS WIZUALNY ---
col_left, col_center, col_right = st.columns([1, 2.5, 1])

def wyswietl_zdjecie_bezpiecznie(nazwa_pliku, fallback_url):
    if os.path.exists(nazwa_pliku):
        st.image(nazwa_pliku, use_container_width=True)
    else:
        st.image(fallback_url, use_container_width=True)

with col_left:
    st.write("")
    wyswietl_zdjecie_bezpiecznie("1fa08f5d77417f45981c55e8b887f909.jpg", "https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?q=80&w=400")
    wyswietl_zdjecie_bezpiecznie("102e80d2a00f1417283bfd743d021a76.jpg", "https://images.unsplash.com/photo-1556229174-5e42a09e45af?q=80&w=400")
    wyswietl_zdjecie_bezpiecznie("9438d31b27d424e2feb4e744c7578aa3.jpg", "https://images.unsplash.com/photo-1616394584738-fc6e612e71b9?q=80&w=400")

with col_right:
    st.write("")
    wyswietl_zdjecie_bezpiecznie("700129929a2803b16ab124197ec8ba69.jpg", "https://images.unsplash.com/photo-1608248597481-496100c8c836?q=80&w=400")
    wyswietl_zdjecie_bezpiecznie("daa4eaf344eebaaa5d8e72625ca7f976.jpg", "https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?q=80&w=400")
    wyswietl_zdjecie_bezpiecznie("edf73f24d9d6a298f7d0626c20569a7c.jpg", "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?q=80&w=400")

with col_center:
    st.markdown('<div class="brand-logo">GlowAI</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-tagline">XOXO, Your Ultimate Skincare Confidant</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="profile-card">', unsafe_allow_html=True)
    st.markdown("<b style='color: #635252;'>Setup Twój Profil 💋</b>", unsafe_allow_html=True)
    c_name, c_email = st.columns(2)
    with c_name:
        user_name = st.text_input("Jak masz na imię?", value="Bff")
    with c_email:
        user_email = st.text_input("E-mail (do wysłania raportu z czatu):", placeholder="girl@messenger.com")
    st.markdown('</div>', unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": f"Cześć {user_name}! Opowiedz mi, z czym dzisiaj walczy Twoja skóra? Zdradź mi wszystko! 💋"}
        ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Napisz sekret o swojej skórze..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("assistant"):
            with st.spinner("✨ Moi agenci z LLM naradzają się nad Twoim przypadkiem..."):
                odpowiedz = uruchom_agentow(prompt)
                st.markdown(odpowiedz)
                st.session_state.messages.append({"role": "assistant", "content": odpowiedz})

    if len(st.session_state.messages) > 1:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Wyślij ten sekret i całą rozmowę na mojego maila 💌"):
            if not user_email or "@" not in user_email:
                st.error("💖 Podaj poprawny e-mail u góry!")
            else:
                full_transcript = ""
                for msg in st.session_state.messages:
                    autor = user_name if msg["role"] == "user" else "GlowAI"
                    full_transcript += f"[{autor}]: {msg['content']}\n\n"
                
                with st.spinner("Wysyłam raport..."):
                    status = send_email(user_email, full_transcript)
                    st.success(status)

st.markdown('<div class="brand-footer">New philosophy of selfcare: healthy skin first</div>', unsafe_allow_html=True)
