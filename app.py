import streamlit as st
import os
import time

# --- USTAWIENIA STRONY ---
st.set_page_config(page_title="GlowAI", page_icon="🎀", layout="wide")

# --- EDGY & CLEAN GIRL UI (BEZWZGLĘDNA PALETA KOLORÓW) ---
css_style = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;800&display=swap');

/* Tło całej aplikacji - jasny róż #F5ECEE */
.stApp, .main, [data-testid="stAppViewContainer"] {
    background-color: #D895B1 !important;
}

/* Wymuszenie fontu Montserrat dla całego tekstu oraz głównego koloru #38242C */
html, body, p, div, span, h1, h2, h3, input, textarea {
    font-family: 'Montserrat', sans-serif !important;
    color: #38242C !important;
}

/* Ukrycie marginesów górnych */
div[data-testid="stAppViewBlockContainer"] {
    padding-top: 2rem !important;
}

/* OGROMNE LOGO GLOW.AI (#6B2F4A) */
.huge-logo {
    font-size: 90px !important;
    font-weight: 800 !important;
    text-align: center !important;
    letter-spacing: 15px !important;
    color: #6B2F4A !important;
    margin-top: 10px !important;
    margin-bottom: -20px !important;
    line-height: 1 !important;
}

/* Subtitle (#A24D72) */
.subtitle {
    font-size: 13px !important;
    text-align: center !important;
    letter-spacing: 6px !important;
    text-transform: uppercase !important;
    color: #A24D72 !important;
    margin-bottom: 60px !important;
    font-weight: 600 !important;
}

/* Zdjęcia po bokach z ramką #C27F97 */
[data-testid='stImage'] img {
    border-radius: 12px !important;
    object-fit: cover;
    border: 2px solid #C27F97 !important;
    box-shadow: 0px 10px 25px rgba(56, 36, 44, 0.1) !important;
}

/* Pola tekstowe - tło #F5ECEE, ramka #C27F97 */
div[data-baseweb="input"] > div {
    background-color: #F5ECEE !important;
    border: 2px solid #C27F97 !important;
    border-radius: 8px !important;
}
div[data-baseweb="input"] > div:focus-within {
    border: 2px solid #A24D72 !important;
}
input::placeholder {
    color: #C27F97 !important;
    letter-spacing: 2px;
    font-size: 12px;
    font-weight: 600;
}

/* WYGLĄD DYMKÓW CZATU - Tło #F5ECEE, ramka #D8AAB7 */
[data-testid="stChatMessage"] {
    background-color: #F5ECEE !important;
    border-radius: 16px !important;
    border: 2px solid #D8AAB7 !important;
    padding: 15px !important;
    margin-bottom: 15px !important;
    font-size: 15px !important;
    box-shadow: none !important;
}
/* Dymek bota - ciemniejszy róż #D8AAB7 */
[data-testid="stChatMessage"]:nth-child(even) {
    background-color: #D8AAB7 !important;
    border: 2px solid #C27F97 !important;
}

/* Pasek wpisywania na dole */
div[data-testid="stChatInput"] {
    background-color: #dfb8cc !important;
    border: 2px solid #C27F97 !important;
    border-radius: 30px !important;
}

/* PRZYCISK MAILOWY - Tło #A24D72 */
div.stButton > button:first-child {
    background-color: #A24D72 !important;
    color: #F5ECEE !important;
    border-radius: 8px !important;
    border: none !important;
    padding: 15px !important;
    font-size: 13px !important;
    font-weight: 700 !important;
    letter-spacing: 3px !important;
    width: 100% !important;
    margin-top: 20px !important;
}
div.stButton > button:first-child:hover {
    background-color: #6B2F4A !important;
    color: #F5ECEE !important;
}

/* Stopka */
.footer {
    text-align: center;
    font-size: 11px;
    letter-spacing: 3px;
    color: #C27F97;
    margin-top: 80px;
    border-top: 1px solid #D8AAB7;
    padding-top: 30px;
}
</style>
"""
st.markdown(css_style, unsafe_allow_html=True)

# --- FUNKCJA BEZPIECZNYCH ZDJĘĆ (BEZ PSA) ---
def safe_image(img_name):
    # Wyświetla zdjęcie TYLKO jeśli istnieje w plikach
    if os.path.exists(img_name):
        st.image(img_name, use_container_width=True)

# --- UKŁAD KOLUMN ---
col_left, col_center, col_right = st.columns([1, 2.2, 1], gap="large")

with col_left:
    st.write("")
    safe_image("1fa08f5d77417f45981c55e8b887f909.jpg")
    st.markdown("<br>", unsafe_allow_html=True)
    safe_image("102e80d2a00f1417283bfd743d021a76.jpg")
    st.markdown("<br>", unsafe_allow_html=True)
    safe_image("9438d31b27d424e2feb4e744c7578aa3.jpg")

with col_right:
    st.write("")
    safe_image("700129929a2803b16ab124197ec8ba69.jpg")
    st.markdown("<br>", unsafe_allow_html=True)
    safe_image("daa4eaf344eebaaa5d8e72625ca7f976.jpg")
    st.markdown("<br>", unsafe_allow_html=True)
    safe_image("edf73f24d9d6a298f7d0626c20569a7c.jpg")

with col_center:
    # GIGANTYCZNE LOGO
    st.markdown('<div class="huge-logo">GLOW.AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Your digital skincare confidant</div>', unsafe_allow_html=True)
    
    # Inputy profilu
    c1, c2 = st.columns(2)
    with c1:
        user_name = st.text_input("Name", placeholder="TWOJE IMIĘ", label_visibility="collapsed")
    with c2:
        user_email = st.text_input("Email", placeholder="TWÓJ EMAIL", label_visibility="collapsed")
    
    st.markdown("<div style='margin-bottom: 40px;'></div>", unsafe_allow_html=True)

    # Inicjalizacja wiadomości w czacie
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Cześć piękna! 🤍 Gotowa zromantyzować swoją rutynę pielęgnacyjną? Zdradź mi, czego dzisiaj pragnie Twoja skóra."}
        ]

    # Wyświetlanie czatu (z własnymi avatarami!)
    for message in st.session_state.messages:
        avatar_icon = "🤍" if message["role"] == "user" else "✨"
        with st.chat_message(message["role"], avatar=avatar_icon):
            st.markdown(message["content"])

    # Wprowadzanie tekstu
    if prompt := st.chat_input("Zdradź mi sekrety swojej skóry..."):
        with st.chat_message("user", avatar="🤍"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("assistant", avatar="✨"):
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

st.markdown('<div class="footer">New philosophy of selfcare: healthy skin first</div>', unsafe_allow_html=True)
