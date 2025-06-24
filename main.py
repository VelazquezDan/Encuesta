import streamlit as st
import json
import time
from collections import defaultdict
import plotly.express as px
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="TechQuiz - ¿Quién Sabe Más?",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personalizado para el estilo tecnológico
st.markdown("""
<style>
:root {
    --electric-blue: #00a8ff;
    --dark-blue: #005a8c;
    --light-blue: #e6f4ff;
    --pcb-green: #0a4b1e;
    --gold: #ffd700;
    --silver: #c0c0c0;
    --dark-bg: #0a0a0a;
}

.stApp {
    background-color: var(--dark-bg);
    background-image: 
        linear-gradient(rgba(0, 168, 255, 0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 168, 255, 0.05) 1px, transparent 1px);
    background-size: 30px 30px;
    color: white;
}

.header {
    background: linear-gradient(135deg, var(--dark-blue), #000);
    color: white;
    padding: 2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    border-bottom: 3px solid var(--gold);
    box-shadow: 0 0 20px rgba(0, 168, 255, 0.5);
    margin-bottom: 2rem;
}

h1 {
    margin: 0;
    font-size: 2.8rem;
    position: relative;
    text-shadow: 0 0 10px var(--electric-blue);
    letter-spacing: 1px;
}

h1::after {
    content: "";
    display: block;
    width: 100px;
    height: 3px;
    background: var(--gold);
    margin: 10px auto;
}

.question-card {
    background: rgba(10, 20, 30, 0.8);
    border-radius: 8px;
    padding: 1.8rem;
    box-shadow: 0 0 15px rgba(0, 168, 255, 0.2);
    border: 1px solid rgba(0, 168, 255, 0.3);
    position: relative;
    overflow: hidden;
    margin-bottom: 2rem;
}

.question-card::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--electric-blue), var(--gold));
}

h2 {
    color: var(--electric-blue);
    margin-top: 0;
    font-size: 1.5rem;
    position: relative;
    padding-left: 20px;
}

h2::before {
    content: "❯";
    position: absolute;
    left: 0;
    color: var(--gold);
}

.option-btn {
    background: rgba(0, 40, 80, 0.5) !important;
    color: white !important;
    border: 1px solid var(--electric-blue) !important;
    border-radius: 6px !important;
    padding: 1rem !important;
    transition: all 0.3s ease !important;
    font-weight: 500 !important;
    width: 100%;
    margin-bottom: 1rem;
}

.option-btn:hover {
    background: var(--electric-blue) !important;
    transform: scale(1.02);
    box-shadow: 0 0 15px var(--electric-blue);
}

.stButton>button {
    background: rgba(0, 40, 80, 0.5);
    color: white;
    border: 1px solid var(--electric-blue);
    border-radius: 6px;
    padding: 0.5rem 1rem;
    transition: all 0.3s ease;
}

.stButton>button:hover {
    background: var(--electric-blue);
    transform: scale(1.02);
    box-shadow: 0 0 15px var(--electric-blue);
}
</style>
""", unsafe_allow_html=True)

# Cargar preguntas desde JSON
@st.cache_resource
def cargar_preguntas():
    try:
        with open('preguntas.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error al cargar preguntas: {e}")
        return []

preguntas_data = cargar_preguntas()

# Inicializar votos en session_state
if 'votos' not in st.session_state:
    st.session_state.votos = {}
    for pregunta in preguntas_data:
        st.session_state.votos[pregunta['id'] = defaultdict(int)
        for i in range(len(pregunta['opciones'])):
            st.session_state.votos[pregunta['id']][f'opcion{i}'] = 0

# Función para manejar votos
def registrar_voto(pregunta_id, opcion_index):
    opcion_key = f'opcion{opcion_index}'
    if pregunta_id in st.session_state.votos and opcion_key in st.session_state.votos[pregunta_id]:
        st.session_state.votos[pregunta_id][opcion_key] += 1
        st.success("¡Voto registrado!")
    else:
        st.error("Opción no válida")

# Header personalizado
st.markdown("""
<div class="header">
    <h1>TECH QUIZ - ¿Quién Sabe Más?</h1>
</div>
""", unsafe_allow_html=True)

# Mostrar preguntas y opciones
for pregunta in preguntas_data:
    with st.container():
        col1, col2 = st.columns([1, 1], gap="large")
        
        with col1:
            st.markdown(f"""
            <div class="question-card">
                <h2>{pregunta['texto']}</h2>
            """, unsafe_allow_html=True)
            
            for i, opcion in enumerate(pregunta['opciones']):
                if st.button(opcion, key=f"btn_{pregunta['id']}_{i}", 
                           help=f"Votar por {opcion}"):
                    registrar_voto(pregunta['id'], i)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="question-card">
                <h2>Resultados en tiempo real</h2>
            """, unsafe_allow_html=True)
            
            # Preparar datos para la gráfica
            datos_votos = {
                "Opciones": pregunta['opciones'],
                "Votos": [st.session_state.votos[pregunta['id']][f'opcion{i}'] 
                         for i in range(len(pregunta['opciones']))]
            }
            
            # Crear gráfica con Plotly
            fig = px.bar(
                datos_votos,
                x="Opciones",
                y="Votos",
                color="Opciones",
                color_discrete_sequence=[
                    '#00a8ff', '#ffd700', '#c0c0c0', '#2ecc71', '#9b59b6', '#e74c3c'
                ],
                template="plotly_dark"
            )
            
            fig.update_layout(
                showlegend=False,
                margin=dict(l=20, r=20, t=30, b=20),
                xaxis_title=None,
                yaxis_title=None,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                hoverlabel=dict(
                    bgcolor="rgba(10, 10, 10, 0.8)",
                    font_size=12,
                    font_color="white"
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

# Nota: Para una implementación multi-usuario en tiempo real, necesitarías:
# 1. Una base de datos externa (Firebase, SQL, etc.)
# 2. Implementar WebSockets (no soportado nativamente en Streamlit)
# 3. O usar una solución como Streamlit Sharing con almacenamiento compartido
