import streamlit as st
import os
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from crewai import Agent, Task, Crew, LLM
from crewai.tools import tool

# --- USTAWIENIA STRONY I WYGLĄD (CSS) ---
st.set_page_config(page_title="GlowAI x Gossip Girl", page_icon="💋", layout="wide")

css_style = (
    "<style>"
    "@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600&family=Montserrat:wght@300;400;600&display=swap');"
    ".stApp { background-color: #fffaf7; }"
    "html, body, [class*='css'] { font-family: 'Montserrat', sans-serif; color: #2b2b2b; }"
    
    # Nagłówki
    ".brand-logo { font-family: 'Cinzel', serif; color: #c98a8a; font-size: 60px; text-align: center; font-weight: 700; letter-spacing: 6px; margin-top: 10px; margin-bottom: 5px; }"
    ".brand-tagline { text-align: center; color: #a38585; font-size: 13px; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 30px; }"
    
    # Karty i dymki czatu
    ".profile-card { background-color: #ffffff; padding: 25px; border-radius: 20px; border: 1px solid #f7dede; box-shadow: 8px 8px 0px #f0cfcf; margin-bottom: 25px; }"
    "[data-testid='stChatMessage'] { background-color: #ffffff; border-radius: 20px; border: 1px solid #f7dede; margin-bottom: 10px; padding: 15px; }"
    "[data-testid='stChatMessage']:nth-child(even) { background-color: #fff0f1; border: 1px solid #ebc5c5; }"
    
    # Zdjęcia
    "[data-testid='stImage'] img { border-radius: 15px; object-fit: cover; border: 1px solid #f7dede; box-shadow: 0px 4px 15px rgba(201,138,138,0.1); transition: transform 0.3s ease; }"
    "[data-testid='stImage'] img:hover { transform: scale(1.03); }"
    
    # Stopka
    ".brand-footer { text-align: center; font-family: 'Cinzel', serif; color: #a38585; font-size: 16px; letter-spacing: 3px; text-transform: uppercase; margin-top: 60px; padding: 25px; border-top: 1px solid rgba(163, 133, 133, 0.15); }"
    
    # Przycisk
    "div.stButton > button:first-child { background-color: #c98a8a !important; color: white !important; border-radius: 25px !important; border: none !important; padding: 10px 25px !important; font-size: 14px !important; font-weight: 600 !important; width: 100%; box-shadow: 0px 4px 12px rgba(201, 138, 138, 0.2) !important; }"
    "div.stButton > button:first-child:hover { background-color: #b87676 !important; transform: translateY(-1px); }"
    "</style>"
)
st.markdown(css_style, unsafe_allow_html=True)


# --- TWOJA LOGIKA BACKENDOWA (Z pliku skincareconsultant.py) ---
GMAIL_USER = "n.zudzin@gmail.com"
GMAIL_PASS = "syry wcts pymb yscg"
os.environ["GROQ_API_KEY"] = "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"

# Lepsza inicjalizacja modelu tak jak w Twoim skrypcie
moj_llm = LLM(model="groq/llama-3.1-8b-instant", temperature=0.3)

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

@tool("Wyszukiwarka_CSV")
def search_cosmetics_tool(skladnik: str) -> str:
    """Szuka produktów w pliku cosmetics.csv."""
    try:
        df = pd.read_csv('cosmetics.csv')
        res = df[df['Ingredients'].str.contains(skladnik.strip(), case=False, na=False)].head(2)
        return res[['Brand', 'Name', 'Price']].to_string(index=False) if not res.empty else "Brak w bazie."
    except: 
        return "Błąd CSV."

def uruchom_agentow(opis_problemu):
    # Odtworzenie agentów z Twojego oryginalnego kodu
    diagnosta = Agent(
        role='Główny Diagnosta Skóry (Skin Profiler)',
        goal='Przeanalizować wypowiedź użytkownika po polsku i określić typ jego cery (np. Oily, Dry, Combination) oraz główne problemy (np. trądzik, przebarwienia).',
        backstory='Jesteś najlepszym dermatologiem w Polsce. Jesteś empatyczna, ale bardzo analityczna. Zawsze odpowiadasz w stylu Gossip Girl, jesteś luksusową przyjaciółką.',
        llm=moj_llm,
        allow_delegation=False
    )

    technolog = Agent(
        role='Technolog Składu', 
        goal='Dobrać składnik aktywny i wyszukać produkt w bazie CSV za pomocą narzędzia.', 
        backstory='Chemik kosmetyczny. Wypowiadasz się z klasą, lekko edgy.', 
        tools=[search_cosmetics_tool], 
        llm=moj_llm,
        allow_delegation=False
    )
    
    strateg = Agent(
        role='Strateg Kosztów', 
        goal='Ocenić opłacalność wybranych produktów rynkowych.', 
        backstory='Dba o budżet pacjenta. Komentuje w stylu przyjaciółki z Messenger.', 
        llm=moj_llm,
        allow_delegation=False
    )
    
    redaktor = Agent(
        role='Główny Konsultant', 
        goal='Zbierz wszystkie dane i stwórz z nich jedną płynną, piękną wiadomość zwrotną do klienta.', 
        backstory='Jesteś głosem marki GlowAI. Odpowiadasz użytkownikowi po polsku, używasz emoji (💋✨). Twoja wypowiedź ma wyglądać jak naturalna wiadomość na czacie z przyjaciółką.', 
        llm=moj_llm,
        allow_delegation=False
    )

    # Zadania (Tasks) z Twojego kodu
    tasks = [
        Task(description=f"Zdiagnozuj krótko typ cery dla: {opis_problemu}.", expected_output="Typ cery i główny problem.", agent=diagnosta),
        Task(description="Wybierz 1 składnik pasujący do diagnozy i użyj narzędzia Wyszukiwarka_CSV.", expected_output="Nazwa, marka i cena z bazy.", agent=technolog),
        Task(description="Oceń krótko opłacalność dobranych produktów z CSV.", expected_output="Analiza kosztów w 2 zdaniach.", agent=strateg),
        Task(description="Napisz do pacjenta ostateczną, zebraną opinię (diagnoza + produkty + koszt) jako jedną wiadomość na czacie, używajac stylu Gossip Girl.", expected_output="Ostateczna, sformatowana wiadomość zwrotna.", agent=redaktor),
    ]

    crew = Crew(agents=[diagnosta, technolog, strateg, redaktor], tasks=tasks)
    return str(crew.kickoff())


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
            with st.spinner("✨ Moi agenci z CrewAI naradzają się nad Twoim przypadkiem..."):
                try:
                    # Tutaj uruchamiamy Twój prawdziwy system CrewAI!
                    odpowiedz = uruchom_agentow(prompt)
                    st.markdown(odpowiedz)
                    st.session_state.messages.append({"role": "assistant", "content": odpowiedz})
                except Exception as e:
                    if "403" in str(e) or "authentication" in str(e).lower():
                        st.error("Błąd 403: Twój klucz do Groq został zablokowany. Wymień go w kodzie!")
                    else:
                        st.error(f"Ojej, błąd agentów: {e}")

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
