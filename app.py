import streamlit as st
import google.generativeai as genai
from streamlit_option_menu import option_menu
from PIL import Image

# 1. Configuración de la IA
genai.configure(api_key="AIzaSyBOW2-p-OwcPKCbq54sByBQgyQw49QL2L4")
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

st.set_page_config(page_title="카이로스 (Kairos)", layout="centered")

# 2. Cargar Estilos
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 3. Encabezado
col1, col2 = st.columns([1, 4])
with col1:
    try: st.image("logo.png", width=80)
    except: st.write("🕊️")
with col2:
    st.markdown("<h1 style='color: #4A403A;'>카이로스</h1>", unsafe_allow_html=True)
    st.write("Tu diccionario y tutor personal")

# 4. Menú de Navegación
selected = option_menu(None, ["Diccionario Pro", "Chat con Kai"], 
    icons=['search', 'robot'], orientation="horizontal")

# --- LÓGICA DICCIONARIO ---
if selected == "Diccionario Pro":
    st.subheader("Búsqueda Avanzada")
    query = st.text_input("Escribe una palabra u oración:")
    
    if query:
        with st.spinner("Kai está analizando..."):
            prompt = f"Analiza '{query}'. Dame: 1. Traducción ES/EN. 2. Hanjas si es coreano (significado individual y conjunto). 3. Gramática desglosada. 4. Contextos de uso. Todo en español."
            res = model.generate_content(prompt)
            st.markdown(res.text)

# --- LÓGICA CHAT ---
elif selected == "Chat con Kai":
    st.subheader("Práctica con Kai (카이)")
    idioma = st.selectbox("Idioma", ["Coreano", "Español", "Inglés"])
    nivel = st.selectbox("Nivel", ["Principiante", "Intermedio", "Avanzado"])

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": f"¡Hola! Soy Kai. Vamos a practicar {idioma} en nivel {nivel}."}]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(f"**{'Kai (카이)' if msg['role'] == 'assistant' else 'Tú'}**")
            st.markdown(msg["content"])

    if p := st.chat_input("Escribe a Kai..."):
        st.session_state.messages.append({"role": "user", "content": p})
        with st.chat_message("user"): st.markdown(p)
        
        with st.chat_message("assistant"):
            with st.spinner("Kai está pensando..."):
                prompt_kai = f"Eres Kai, un tutor de {idioma} nivel {nivel}. Responde y corrige errores."
                res = model.generate_content(f"{prompt_kai}\nChat: {p}")
                st.markdown(res.text)
                st.session_state.messages.append({"role": "assistant", "content": res.text})
