import streamlit as st
import os
import time

# --- USTAWIENIA STRONY ---
st.set_page_config(page_title="GlowAI | Skincare Secrets", page_icon="🎀", layout="wide")

# --- EDGY & CLEAN GIRL UI (ZAAWANSOWANY CSS) ---
css_style = """
<style>
/* Luksusowe fonty */
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700&family=Jost:wght@300;400;500&display=swap');

/* Tło strony - czysty, ciepły krem */
.stApp {
    background-color: #fdfbf9;
}

/* Wymuszenie fontu globalnie */
html, body, [class*='css'], p, div {
    font-family: 'Jost', sans-serif !important;
    color: #2b2b2b !important;
}

/* Ukrycie domyślnego, pustego marginesu na górze Streamlita */
div[data-testid="stAppViewBlockContainer"] {
    padding-top: 2rem !important;
}

/* GŁÓWNE LOGO */
.edgy-logo {
    font-family: 'Cinzel', serif;
    font-size: 65px;
    text-align: center;
    font-weight: 700;
    letter-spacing: 12px;
    color: #1a1a1a;
    text-transform: uppercase;
    margin-top: 0px;
    margin-bottom: -10px;
}

.subtitle {
    text-align: center;
    font-family: 'Jost', sans-serif;
    font-size: 11px;
    letter-spacing: 5px;
    text-transform: uppercase;
    color: #a39191;
    margin-bottom: 50px;
}

/* ZDJĘCIA PO BOKACH - aesthetic filter */
[data-testid='stImage'] img {
    border-radius: 12px !important;
    object-fit: cover;
    box-shadow: 0px 8px 25px rgba(0, 0, 0, 0.04) !important;
    border: 1px solid #f2ecec;
    transition: all 0.5s ease;
    filter: contrast(105%) brightness(102%) saturate(90%);
}
[data-testid='stImage'] img:hover {
    transform: translateY(-4px);
    box-shadow: 0px 15px 35px rgba(0, 0, 0, 0.08) !important;
    filter: contrast(110%) brightness(105%) saturate(100%);
}

/* POLA TEKSTOWE - czysty minimalizm */
div[data-baseweb="input"] > div {
    background-color: #ffffff !important;
    border: 1px solid #e8dcdc !important;
    border-radius: 6px !important;
    padding: 2px 5px !important;
}
div[data-baseweb="input"] > div:focus-within {
    border: 1px solid #c98a8a !important;
    box-shadow: none !important;
}
input::placeholder {
    color: #b5a6a6 !important;
    letter-spacing: 1px;
    font-size: 13px;
    text-transform: uppercase;
}

/* WYGLĄD DYMKÓW CZATU */
[data-testid="stChatMessage"] {
    background-color: #ffffff !important;
    border-radius: 16px;
    border: 1px solid #f2ecec !important;
    padding: 18px 22px !important;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.01) !important;
    margin-bottom: 15px !important;
    font-size: 15px !important;
    line-height: 1.6 !important;
}
[data-testid="stChatMessage"]:nth-child(even) {
    background-color: #faf5f5 !important;
    border: 1px solid #f5e6e6 !important;
}

/* PASEK CZATU NA DOLE */
div[data-testid="stChatInput"] {
    background-color: #ffffff !important;
    border: 1px solid #e8dcdc !important;
    border-radius: 30px !important;
    padding: 2px 10px !important;
    box-shadow: 0px -5px 20px rgba(0, 0, 0, 0.02) !important;
}

/* PRZYCISK MAILOWY - Haute Couture */
div.stButton > button:first-child {
    background-color: #1a1a1a !important;
    color: #ffffff !important;
    border-radius: 6px !important;
    border: none !important;
    padding: 15px 24px !important;
    font-family: 'Jost', sans-serif !important;
    font-size: 11px !important;
    font-weight: 500 !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    width: 100%;
    margin-top: 10px;
    transition: all 0.3s ease;
}
div.stButton > button:first-child:hover {
    background-color: #c98a8a !important;
    color: #ffffff !important;
}

/* STOPKA */
.footer {
    text-align: center;
    font-size: 10px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #b5a6a6;
    margin-top: 80px;
    padding-bottom: 20px;
    border-top: 1px solid #f2ecec;
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
        user_name = st.text_input("Name", placeholder="YOUR NAME", label_visibility="collapsed")
    with c2:
        user_email = st.text_input("Email", placeholder="YOUR EMAIL", label_visibility="collapsed")
    
    st.markdown("<div style='margin-bottom: 40px;'></div>", unsafe_allow_html=True)

    # Inicjalizacja czatu
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi gorgeous! 🤍 Ready to romanticize your skincare routine? Tell me what your skin is craving today."}
        ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Wprowadzanie tekstu
    if prompt := st.chat_input("Tell me your skin secrets..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("assistant"):
            with st.spinner("Analyzing your glow profile... ✨"):
                time.sleep(1.5) 
                mock_response = (
                    "I see exactly what's going on! ✨ Your skin barrier needs a little extra love right now.\n\n"
                    "**The Diagnosis:** Dehydration mixed with slight irritation. We need to focus on barrier repair.\n\n"
                    "**The Protocol:** Drop the harsh actives. Switch to a milky cleanser, drown your skin in Ceramides (our database suggests the *Rhode Glazing Fluid*), and seal it with a rich peptide cream.\n\n"
                    "You've got this. Keep glowing! 🧴🤍"
                )
                st.markdown(mock_response)
        st.session_state.messages.append({"role": "assistant", "content": mock_response})

    # Przycisk mailowy
    if len(st.session_state.messages) > 1:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("SEND ROUTINE TO MY EMAIL"):
            if not user_email or "@" not in user_email:
                st.error("Please enter a valid email above gorgeous! ✨")
            else:
                with st.spinner("Sending aesthetic vibes to your inbox..."):
                    time.sleep(1)
                    st.success("Sent! Check your inbox. 🕊️")

st.markdown('<p class="footer">New philosophy of selfcare: healthy skin first</p>', unsafe_allow_html=True)
