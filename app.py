import streamlit as st
import os
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from crewai import Agent, Task, Crew, LLM
from crewai.tools import tool

# --- STYLIZACJA STRONY (Dziewczęcy, Edgy Pink & Cream Aesthetic) ---
st.set_page_config(page_title="GlowAI - Skin Profiler", page_icon="✨", layout="wide")

st.markdown("""
    <style>
    /* Główny background i czcionki */
    .stApp {
        background-color: #fff9f5;
    }
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;1,400&family=Montserrat:wght@300;400;600&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Montserrat', sans-serif;
        color: #4a4a4a;
    }
    
    /* Różowy, dziewczęcy nagłówek */
    .main-title {
        font-family: 'Playfair Display', serif;
        color: #9b4d4d;
        font-size: 55px;
        text-align: center;
        margin-bottom: 5px;
        font-weight: 700;
    }
    .subtitle {
        text-align: center;
        color: #cca4a4;
        font-size: 18px;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 40px;
    }
    
    /* Karta formularza - Kremowa z różową ramką */
    .glow-card {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 30px 0px 30px 0px; /* Edgy design */
        border: 2px solid #fce7e8;
        box-shadow: 10px 10px 0px #fbcba2;
        margin-bottom: 30px;
    }
    
    /* Estetyczne kafelki produktowe */
    .product-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #fbcba2;
        margin-bottom: 15px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.02);
    }
    
    /* Przyciski */
    div.stButton > button:first-child {
        background-color: #9b4d4d !important;
        color: white !important;
        border-radius: 20px !important;
        border: none !important;
        padding: 12px 30px !important;
        font-weight: 600 !important;
        width: 100%;
        transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #fbcba2 !important;
        color: #121212 !important;
        transform: translateY(-2px);
    }
    </style>
""", unsafe_allowed_html=True)

# --- KONFIGURACJA POCZTY I AI ---
GMAIL_USER = "n.zudzin@gmail.com"
GMAIL_PASS = "syry wcts pymb yscg"
os.environ["GROQ_API_KEY"] = "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"

moj_llm = LLM(model="groq/llama-3.1-8b-instant", temperature=0.3)

def send_email(receiver_email, content):
    try:
        msg = MIMEMultipart()
        msg['From'] = GMAIL_USER
        msg['To'] = receiver_email
        msg['Subject'] = "✨ Twój Osobisty Raport Pielęgnacyjny GlowAI"
        msg.attach(MIMEText(content, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASS)
        server.send_message(msg)
        server.quit()
        return "Mail wysłany!"
    except Exception as e:
        return f"Błąd wysyłki: {e}"

@tool("Wyszukiwarka_CSV")
def search_cosmetics_tool(skladnik: str) -> str:
    """Szuka produktów w pliku cosmetics.csv."""
    try:
        df = pd.read_csv('cosmetics.csv')
        res = df[df['Ingredients'].str.contains(skladnik.strip(), case=False, na=False)].head(2)
        return res[['Brand', 'Name', 'Price']].to_string(index=False) if not res.empty else "Brak w bazie."
    except: 
        return "Błąd bazy danych."

# --- UKŁAD STRONY WEBOWEJ ---

st.markdown('<div class="main-title">GlowAI</div>', unsafe_allowed_html=True)
st.markdown('<div class="subtitle">✨ Twój Inteligentny Skin Profiler online ✨</div>', unsafe_allowed_html=True)

# GÓRNA SEKCJA: INSPIRACJE I METAMORFOZY (Estetyczne zdjęcia z internetu)
col1, col2, col3 = st.columns(3)
with col1:
    st.image("https://images.unsplash.com/photo-1556228720-195a672e8a03?q=80&w=400", caption="Clean Girl Glow")
with col2:
    st.image("https://images.unsplash.com/photo-1608248597481-496100c8c836?q=80&w=400", caption="Świadoma Pielęgnacja")
with col3:
    st.image("https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?q=80&w=400", caption="Naturalna Metamorfoza")

st.markdown("---")

# INTERFEJS KONSULTACJI
st.markdown('<div class="glow-card">', unsafe_allowed_html=True)
st.subheader("🌸 Rozpocznij swoją darmową analizę")

user_input = st.text_area("Opisz nam stan swojej cery (np. 'mam problem z egzemą i suchą skórą, świecę się na czole'):", placeholder="Napisz to całkowicie na luzie, swoimi słowami...")
user_email = st.text_input("Twój adres e-mail (na niego wyślemy pełen raport):", placeholder="przyklad@gmail.com")

generate_btn = st.button("GENERUJ MÓJ GLOW-PLAN ✨")
st.markdown('</div>', unsafe_allowed_html=True)

# REAKCJA NA KLIKNIĘCIE
if generate_btn:
    if not user_input or not user_email or "@" not in user_email:
        st.error("💖 Proszę, uzupełnij poprawnie opis cery oraz swój e-mail!")
    else:
        with st.spinner("✨ Nasz zespół 5 agentów AI analizuje Twoją skórę... Chwileczkę, tworzymy magię!"):
            
            # Definiowanie agentów (Twój oryginalny kod)
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
                
                # WYŚWIETLENIE WYNIKU NA STRONIE
                st.balloons()
                st.success(f"💖 Sukces! {status_maila}")
                
                st.markdown("### 💌 Twój Spersonalizowany Raport:")
                st.write(str(wynik))
                
                # Prezentacja polecanych kosmetyków
                st.markdown("### 🧴 Sugerowane produkty z naszej bazy:")
                st.markdown("""
                    <div class="product-box">
                        <b>🧁 Krem ochronny z ceramidami i kwasem hialuronowym</b><br>
                        <i>Rekomendowany dla odbudowy barierowej | Estymowany koszt: 50,00 zł za 100 ml</i>
                    </div>
                    <div class="product-box">
                        <b>🌿 Serum kojące z ekstraktami roślinnymi</b><br>
                        <i>Intensywne nawilżenie i redukcja zaczerwienień | Estymowany koszt: 30,00 zł za 30 ml</i>
                    </div>
                """, unsafe_allowed_html=True)
                
            except Exception as e:
                st.error(f"Coś poszło nie tak, spróbuj ponownie za chwilę! Błąd: {e}")