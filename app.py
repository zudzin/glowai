import streamlit as st
import os
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from crewai import Agent, Task, Crew, LLM
from crewai.tools import tool

# --- USTAWIENIA STRONY ---
st.set_page_config(page_title="glowai", page_icon="💖", layout="wide")

# --- EDGY PINK & CREAM HIGH-END AESTHETIC (Inspirowane Rhode & Hush) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600&family=Montserrat:wght@300;400;600&display=swap');
    
    /* Tło całej aplikacji - delikatny, luksusowy krem */
    .stApp {
        background-color: #fff9f6;
    }
    
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
        color: #2b2b2b;
    }
    
    /* Olbrzymi, edgy napis w tle w stylu Twoich inspo */
    .bg-huge-text {
        font-family: 'Cinzel', serif;
        font-size: 14vw;
        color: rgba(224, 164, 164, 0.15);
        font-weight: 700;
        text-align: center;
        position: absolute;
        width: 100%;
        top: -40px;
        z-index: 0;
        pointer-events: none;
        letter-spacing: -5px;
    }
    
    /* Estetyczne menu górne */
    .nav-bar {
        text-align: center;
        padding: 15px;
        font-size: 13px;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #a38585;
        border-bottom: 1px solid rgba(163, 133, 133, 0.15);
        margin-bottom: 30px;
    }
    
    /* Główny nagłówek */
    .brand-title {
        font-family: 'Cinzel', serif;
        color: #c98a8a;
        font-size: 70px;
        text-align: center;
        font-weight: 600;
        letter-spacing: 4px;
        margin-top: 20px;
    }
    
    .brand-subtitle {
        text-align: center;
        color: #635252;
        font-size: 16px;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 50px;
    }
    
    /* Pudrowo-różowe, minimalistyczne kontenery */
    .skincare-card {
        background-color: #ffffff;
        padding: 40px;
        border-radius: 40px 0px 40px 0px; /* Charakterystyczne, ścięte rogi jak w HUSH */
        border: 1px solid #f7dede;
        box-shadow: 15px 15px 0px #f0cfcf;
        margin-bottom: 40px;
        position: relative;
        z-index: 1;
    }
    
    /* Zdjęcia i transformacje przed/po */
    .gallery-img {
        border-radius: 20px;
        object-fit: cover;
        box-shadow: 0px 10px 25px rgba(201, 138, 138, 0.15);
        transition: transform 0.3s ease;
    }
    .gallery-img:hover {
        transform: scale(1.02);
    }
    
    /* Produkty kosmetyczne w stylu Rhode */
    .product-pill {
        background-color: #f7dede;
        color: #635252;
        padding: 20px;
        border-radius: 20px;
        margin-bottom: 15px;
        border: 1px solid #ebc5c5;
        font-weight: 400;
    }
    
    /* Przepiękny, matowy przycisk */
    div.stButton > button:first-child {
        background-color: #c98a8a !important;
        color: white !important;
        border-radius: 30px !important;
        border: none !important;
        padding: 15px 40px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        letter-spacing: 2px !important;
        width: 100%;
        box-shadow: 0px 8px 20px rgba(201, 138, 138, 0.3) !important;
    }
    div.stButton > button:first-child:hover {
        background-color: #b87676 !important;
        transform: translateY(-2px);
    }
    </style>
""", unsafe_allowed_html=True)

# --- WYSTAWKA FRONTENDU ---
st.markdown('<div class="nav-bar">About us &nbsp; • &nbsp; Catalog &nbsp; • &nbsp; Skincare &nbsp; • &nbsp; AI Consultant</div>', unsafe_allowed_html=True)

# Duży napis w tle i główny brand
st.markdown('<div class="bg-huge-text">GLOW</div>', unsafe_allowed_html=True)
st.markdown('<div class="brand-title">rhode x glowai</div>', unsafe_allowed_html=True)
st.markdown('<div class="brand-subtitle">New philosophy of selfcare: healthy skin first</div>', unsafe_allowed_html=True)

# --- NAJPIĘKNIEJSZA SEKCJA WIZUALNA (MODELKI + PRZEMIANY) ---
col_img1, col_img2, col_img3 = st.columns(3)
with col_img1:
    st.markdown('<img class="gallery-img" src="https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?q=80&w=500" width="100%">', unsafe_allowed_html=True)
    st.caption("✨ Dewy, glazed skin finish.")
with col_img2:
    st.markdown('<img class="gallery-img" src="https://images.unsplash.com/photo-1556229174-5e42a09e45af?q=80&w=500" width="100%">', unsafe_allowed_html=True)
    st.caption("🌿 Pure care by nature.")
with col_img3:
    st.markdown('<img class="gallery-img" src="https://images.unsplash.com/photo-1616394584738-fc6e612e71b9?q=80&w=500" width="100%">', unsafe_allowed_html=True)
    st.caption("🌸 Barrier support transformation.")

st.markdown("<br><br>", unsafe_allowed_html=True)

# --- INTERFEJS KONSULTACJI DLA PROFESORA ---
st.markdown('<div class="skincare-card">', unsafe_allowed_html=True)
st.markdown("<h2 style='font-family: Cinzel, serif; color: #635252; text-align:center;'>🌸 Spersonalizowany Konsultant AI</h2>", unsafe_allowed_html=True)
st.markdown("<p style='text-align:center; color: #a38585; font-style: italic; margin-bottom:30px;'>Opisz swoje problemy skórne w wolnym tekście. Nasz zespół 5 agentów dobierze idealną kurację.</p>", unsafe_allowed_html=True)

user_input = st.text_area("Opisz swoją skórę (np. 'mam problem z egzemą i suchą skórą, ale świecę się w strefie T'):", placeholder="Napisz to w 100% naturalnie, tak jak czujesz...")
user_email = st.text_input("Twój e-mail, na który wyślemy oficjalny raport medyczny:", placeholder="your.email@gmail.com")

generate_btn = st.button("ANALIZUJ PROFIL SKÓRY ✨")
st.markdown('</div>', unsafe_allowed_html=True)

# --- BACKEND (Agentowy silnik z Twojego projektu) ---
GMAIL_USER = "n.zudzin@gmail.com"
GMAIL_PASS = "syry wcts pymb yscg"
os.environ["GROQ_API_KEY"] = "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"

moj_llm = LLM(model="groq/llama-3.1-8b-instant", temperature=0.3)

def send_email(receiver_email, content):
    try:
        msg = MIMEMultipart()
        msg['From'] = GMAIL_USER
        msg['To'] = receiver_email
        msg['Subject'] = "🌸 Twój Osobisty Plan Pielęgnacyjny od GlowAI"
        msg.attach(MIMEText(content, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASS)
        server.send_message(msg)
        server.quit()
        return "Raport wysłany na Twojego maila!"
    except Exception as e:
        return f"Błąd poczty: {e}"

@tool("Wyszukiwarka_CSV")
def search_cosmetics_tool(skladnik: str) -> str:
    """Szuka produktów w pliku cosmetics.csv."""
    try:
        df = pd.read_csv('cosmetics.csv')
        res = df[df['Ingredients'].str.contains(skladnik.strip(), case=False, na=False)].head(2)
        return res[['Brand', 'Name', 'Price']].to_string(index=False) if not res.empty else "Brak w bazie."
    except: 
        return "Błąd podczas odczytu bazy cosmetics.csv."

if generate_btn:
    if not user_input or not user_email or "@" not in user_email:
        st.error("💖 Słońce, podaj poprawny opis cery oraz swój adres e-mail!")
    else:
        with st.spinner("✨ Agenci AI (Diagnosta, Technolog, Strateg, Redaktor, Spedytor) miksują składniki aktywne..."):
            
            diagnosta = Agent(role='Dermatolog Kliniczny', goal='Postawić diagnozę dla: {input}', backstory='Lekarz analizujący biologię skóry.', llm=moj_llm)
            technolog = Agent(role='Technolog Składu', goal='Dobrać składnik i wyszukać w CSV.', backstory='Chemik kosmetyczny.', tools=[search_cosmetics_tool], llm=moj_llm)
            strateg = Agent(role='Strateg Kosztów', goal='Ocenić opłacalność.', backstory='Dba o budżet pacjenta.', llm=moj_llm)
            redaktor = Agent(role='Główny Konsultant', goal='Stwórz piękny raport po polsku.', backstory='Pisze uprzejmie w stylu kosmetologa.', llm=moj_llm)
            spedytor = Agent(role='Koordynator Wysyłki', goal='Przygotować treść maila.', backstory='Pakuje raport w e-mail.', llm=moj_llm)

            tasks = [
                Task(description="Zdiagnozuj krótko typ cery dla: {input}.", expected_output="Typ cery i główny problem.", agent=diagnosta),
                Task(description="Wybierz 1 składnik i znajdź produkt w CSV.", expected_output="Nazwa, marka i cena z bazy.", agent=technolog),
                Task(description="Oceń krótko opłacalność.", expected_output="Analiza kosztów w 2 zdaniach.", agent=strateg),
                Task(description="Stwórz profesjonalny raport dla pacjenta po polsku bez technicznych dopisków.", expected_output="Elegancki raport medyczny.", agent=redaktor),
                Task(description="Sformatuj jako gotowy e-mail.", expected_output="Gotowy mail.", agent=spedytor)
            ]

            crew = Crew(agents=[diagnosta, technolog, strateg, redaktor, spedytor], tasks=tasks)
            
            try:
                wynik = crew.kickoff(inputs={'input': user_input})
                status_maila = send_email(user_email, str(wynik))
                
                st.balloons()
                st.success(f"💖 {status_maila}")
                
                # WYŚWIETLENIE REKOMENDACJI
                st.markdown("### 📋 Wynik analizy kosmetologicznej:")
                st.info(str(wynik))
                
                # SAKCJA ESTETYCZNYCH PRODUKTÓW
                st.markdown("### 🧴 Wyselekcjonowane produkty dla Ciebie:")
                st.markdown("""
                    <div class="product-pill">
                        <b>🎀 Rhode Glazing Fluid</b> — Intensywne nawilżenie, bariera naskórkowa, kwas hialuronowy.
                    </div>
                    <div class="product-pill">
                        <b>🌿 Sage Pure Barrier Cream</b> — Łagodzenie stanów zapalnych, regeneracja hydrolipidowa.
                    </div>
                """, unsafe_allowed_html=True)
                
            except Exception as e:
                st.error(f"Wystąpił błąd serwera. Spróbuj ponownie za chwilę. Szczegóły: {e}")
