import streamlit as st

import sys
from pathlib import Path

# Agregar la raíz del proyecto al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from Agents.Orquestador.graph import graph

from langchain_core.messages import (
    HumanMessage,
    AIMessage
)


# 1. Configuración de la página
st.set_page_config(
    page_title="ROMA - Product Owner Assistant",
    page_icon="🟣",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. CSS personalizado
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@200;300;400;500;600;700;800&display=swap');
            
    .main-title {
        font-family: 'Manrope', sans-serif !important;
        color:  #7c4dff !important;
        text-align: left;
        padding: 1rem;
        border-bottom: 2px solid  #7c4dff ;
        margin-bottom: 2rem;
    }
    
    .main-title span {
        color: #161338;
        border-bottom: 2px solid #ffffff !important;
    }
            
    .main-body {
        color: white !important;
    }       

    /* 1. Estilo base para AMBAS burbujas */
    [data-testid="stChatMessage"] {
        border-radius: 20px !important;
        margin-bottom: 15px;
        padding: 15px;
        border: 2px solid #7c4dff !important;
        background-color: #f9f7ff;
    
    }

    /* Personalización del Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #1e0b4b 0%,
            #24115c 40%,
            #13072e 100%
        ) !important;

        border-right: 1px solid rgba(255,255,255,0.08);
    }

    /* Texto del sidebar */
    [data-testid="stSidebar"] * {
        color: white !important;
    }

    
    /* Estilo para los botones (opcional) */
    .stButton >button {
        border-radius: 20px;
        border: 1px solid #FF6B35;
        background-color: transparent;
        color: white !important;
        font-weight: 600;
        transition: 0.3s ease;
    }

    .stButton > button:hover {
        background-color: #7c4dff;
        border: 1px solid #7c4dff;
        color: white !important;
    }
    </style>

    <h5>¡Hola, Product Owner! 👋</h5>        
    <h1 class="main-title">Soy <span class="main-title span">ROMA</span>, tu asistente virtual</h1>
    <h6> Cuéntame qué necesitas hoy y trabajemos juntos para construir productos increíbles.</h6>
""", unsafe_allow_html=True)

# 3. Sidebar
with st.sidebar:
   
    st.image(
        "Recursos\ROMA.png",
        width=250
    )

    st.markdown("### 🚀 Te puedo ayudar a:")

    st.markdown("""
    - Crear historias de usuario  
    - Filtrar Issues del sprint actual segun una etiqueta
    - Generar reportes para los Stakeholders
    - Consultas sobre la metodologia Scrum
    """)


    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("➕ Nueva conversación"):
        st.session_state.messages = []
        st.rerun()

# 4. Session state 
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Mostrar historial
for msg in st.session_state.messages:
    avatar = "👩🏻‍🍳" if msg["role"] == "assistant" else "👤"

    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

        # Mostrar imagen si existe
        if "image" in msg and msg["image"] is not None:
            st.image(msg["image"], caption="Imagen enviada", width="stretch")


# 7. Input del usuario
if query := st.chat_input("¿En qué te puedo ayudar?"):

    # Guardar mensaje usuario
    st.session_state.messages.append({
        "role": "user",
        "content": query,
    })

    # Mostrar mensaje usuario
    with st.chat_message("user", avatar="👨‍💻"):
        st.markdown(query)

    # Respuesta del agente
    with st.chat_message("assistant", avatar="🟣"):

        with st.spinner("ROMA está pensando..."):

            try:

                # ==================================
                # Convertir historial a LangChain
                # ==================================

                langchain_messages = []

                for msg in st.session_state.messages:

                    if msg["role"] == "user":

                        langchain_messages.append(
                            HumanMessage(
                                content=msg["content"]
                            )
                        )

                    elif msg["role"] == "assistant":

                        langchain_messages.append(
                            AIMessage(
                                content=msg["content"]
                            )
                        )

                # ==================================
                # Invocar graph con historial
                # ==================================

                response = graph.invoke(
                    {
                        "messages": langchain_messages
                    }
                )

                final_response = response[
                    "final_response"
                ]

                st.markdown(final_response)

                # Guardar respuesta
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": final_response
                })

            except Exception as e:

                st.error(
                    f"¡Ups! Algo salió mal: {e}"
                )