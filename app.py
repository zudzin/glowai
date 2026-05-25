import streamlit as st
import os
import time

# --- USTAWIENIA STRONY ---
st.set_page_config(page_title="GlowAI | Skincare Secrets", page_icon="🎀", layout="wide")

# --- EDGY & CLEAN GIRL UI (ZAAWANSOWANY CSS) ---
css_style = """
<style>
/* Luksusowy font - wyłącznie Montserrat */
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap');

/* Tło strony - najjaśniejszy odcień palety (#F5ECEE) */
.stApp {
    background-color: #F5ECEE;
}

/* Wymuszenie fontu Montserrat i najciemniejszego koloru tekstu dla czytelności (#38242C) */
html, body, [class*='css'], p, div {
    font-family: 'Montserrat', sans-serif !important;
    color: #38242C !important;
}

/* Ukrycie domyślnego, pustego marginesu na górze Streamlita */
div[data-testid="stAppViewBlockContainer"] {
    padding-top: 2rem !important;
}

/* GŁÓWNE LOGO (#A24D72) */
.edgy-logo {
    font-family: 'Montserrat', sans-serif;
    font-size: 60px;
    text-align: center;
    font-weight: 700;
    letter-spacing: 10px;
    color: #A24D72;
    text-transform: uppercase;
    margin-top: 0px;
    margin-bottom: -10px;
}

.subtitle {
    text-align: center;
    font-family: 'Montserrat', sans-serif;
    font-size: 11px;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: #C27F97;
    margin-bottom: 50px;
    font-weight: 600;
}

/* ZDJĘCIA PO BOKACH - ramki w kolorze #D8AAB7 */
[data-testid='stImage'] img {
    border-radius: 12px !important;
    object-fit: cover;
    box-shadow: 0px 8px 25px rgba(107, 47, 74, 0.1) !important; /* Poświata w kolorze #6B2F4A */
    border: 1px solid #D8AAB7;
    transition: all 0.5s ease;
}
[data-testid='stImage'] img:hover {
    transform: translateY(-4px);
    box-shadow: 0px 15px 35px rgba(107, 47, 74, 0.2) !important;
}

/* POLA TEKSTOWE */
div[data-baseweb="input"] > div {
    background-color: #FFFFFF !important;
    border: 1px solid #D8AAB7 !important;
    border-radius: 8px !important;
    padding: 2px 5px !important;
}
div[data-baseweb="input"] > div:focus-within {
    border: 1px solid #A24D72 !important;
    box-shadow: none !important;
}
input::placeholder {
    color: #C27F97 !important;
    letter-spacing: 1px;
    font-size: 12px;
    text-transform: uppercase;
    font-weight: 500;
}

/* WYGLĄD DYMKÓW CZATU */
[data-testid="stChatMessage"] {
    background-color: #FFFFFF !important;
    border-radius: 16px;
    border: 1px solid #D8AAB7 !important;
    padding: 18px 22px !important;
    box-shadow: 0px 4px 15px rgba(107, 47, 74, 0.05) !important;
    margin-bottom: 15px !important;
    font-size: 14px !important;
    line-height: 1.6 !important;
}
/* Dymek bota - piękny, brudny róż z palety (#D8AAB7) */
[data-testid="stChatMessage"]:nth-child(even) {
    background-color: #D8AAB7 !important;
    border: 1px solid #C27F97 !important;
}

/* PASEK CZATU NA DOLE */
div[data-testid="stChatInput"] {
    background-color: #FFFFFF !important;
    border: 1px solid #D8AAB7 !important;
    border-radius: 30px !important;
    padding: 2px 10px !important;
    box-shadow: 0px -5px 20px rgba(107, 47, 74, 0.08) !important;
}

/* PRZYCISK MAILOWY - intensywny róż (#A24D72) */
div.stButton > button:first-child {
    background-color: #A24D72 !important;
    color: #FFFFFF !important;
    border-radius: 8px !important;
    border: none !important;
    padding: 15px 24px !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    width: 100%;
    margin-top: 10px;
    transition: all 0.3s ease;
}
div.stButton > button:first-child:hover {
    background-color: #6B2F4A !important; /* Ciemniejszy róż na hover */
    color: #F5ECEE !important;
    transform: translateY(-2px);
}

/* STOPKA */
.footer {
    text-align: center;
    font-size: 10px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #C27F97;
    margin-top: 80px;
    padding-bottom: 20px;
    border-top: 1px solid #D8AAB7;
    padding-top: 30px;
}
</style>
"""
st.markdown(css_style, unsafe_allow_html=True)

# --- FUNKCJE POMOCNICZE WIZUALNE ---
def safe_image(img_name, fallback_url):
    if os.path.exists(img_name):
        st.image(img_name, use_container_width=True)
    else:
        st.image(fallback_url, use_container_width=True)

# --- UKŁAD KOLUMN ---
col_left, col_center, col_right = st.columns([1, 2.2, 1], gap="large")

with col_left:
    st.write("")
    safe_image("1fa08f5d77417f45981c55e8b887f909.jpg", "https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?q=80&w=400")
    st.markdown("<br>", unsafe_allow_html=True)
    safe_image("102e80d2a00f1417283bfd743d021a76.jpg", "https://images.unsplash.com/photo-1556229174-5e42a09e45af?q=80&w=400")
    st.markdown("<br>", unsafe_allow_html=True)
    safe_image("9438d31b27d424e2feb4e744c7578aa3.jpg", "https://images.unsplash.com/photo-1616394584738-fc6e612e71b9?q=80&w=400")

with col_right:
    st.write("")
    safe_image("700129929a2803b16ab124197ec8ba69.jpg", "https://images.unsplash.com/photo-1608248597481-496100c8c836?q=80&w=400")
    st.markdown("<br>", unsafe_allow_html=True)
    safe_image("daa4eaf344eebaaa5d8e72625ca7f976.jpg", "https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?q=80&w=400")
    st.markdown("<br>", unsafe_allow_html=True)
    safe_image("edf73f24d9d6a298f7d0626c20569a7c.jpg", "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?q=80&w=400")

with col_center:
    # Logo
    st.markdown('<p class="edgy-logo">GLOW.AI</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Your digital skincare confidant</p>', unsafe_allow_html=True)
    
    # Ultra-minimalistyczny setup profilu (ukryte etykiety)
    c1, c2 = st.columns(2)
    with c1:
        user_name = st.text_input("Name", placeholder="TWOJE IMIĘ", label_visibility="collapsed")
    with c2:
        user_email = st.text_input("Email", placeholder="TWÓJ EMAIL", label_visibility="collapsed")
    
    st.markdown("<div style='margin-bottom: 40px;'></div>", unsafe_allow_html=True)

    # Inicjalizacja czatu
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Cześć piękna! 🤍 Gotowa zromantyzować swoją rutynę pielęgnacyjną? Zdradź mi, czego dzisiaj pragnie Twoja skóra."}
        ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Wprowadzanie tekstu
    if prompt := st.chat_input("Zdradź mi sekrety swojej skóry..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("assistant"):
            with st.spinner("Analizuję Twój profil glow... ✨"):
                time.sleep(1.5) 
                mock_response = (
                    "Wiem dokładnie, co tu się dzieje! ✨ Twoja bariera hydrolipidowa potrzebuje teraz odrobiny miłości.\n\n"
                    "**Diagnoza:** Odwodnienie połączone z lekkim podrażnieniem. Musimy w 100% skupić się na odbudowie bariery.\n\n"
                    "**Protokół:** Odstaw mocne składniki aktywne. Przejdź na mleczną emulsję do mycia, zalej skórę Ceramidami (nasza baza podpowiada *Rhode Glazing Fluid*) i domknij to wszystko bogatym kremem peptydowym.\n\n"
                    "Dasz radę. Keep glowing! 🧴🤍"
                )
                st.markdown(mock_response)
        st.session_state.messages.append({"role": "assistant", "content": mock_response})

    # Przycisk mailowy
    if len(st.session_state.messages) > 1:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("WYŚLIJ RUTYNĘ NA MÓJ EMAIL"):
            if not user_email or "@" not in user_email:
                st.error("Wpisz wyżej poprawny e-mail, piękna! ✨")
            else:
                with st.spinner("Wysyłam aesthetic vibes na Twoją skrzynkę..."):
                    time.sleep(1)
                    st.success("Wysłane! Sprawdź swoją skrzynkę. 🕊️")

st.markdown('<p class="footer">New philosophy of selfcare: healthy skin first</p>', unsafe_allow_html=True)
