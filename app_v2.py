import streamlit as st
import json
from planner_data import PLANNER_DATA

# Configuração da página para ser mobile-friendly
st.set_page_config(
    page_title="30-Day Prayer Planner",
    page_icon="🕊️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilos CSS para um visual limpo e profissional
st.markdown("""
    <style>
    .main { padding: 1rem; }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 12px;
        font-weight: bold;
    }
    .verse-box {
        background-color: #f0f7f4;
        border-left: 5px solid #4CAF50;
        padding: 20px;
        margin: 20px 0;
        border-radius: 5px;
    }
    .reflection-box {
        background-color: #fffdf0;
        border-left: 5px solid #ffd700;
        padding: 20px;
        margin: 20px 0;
        border-radius: 5px;
    }
    .prayer-box {
        background-color: #f0f4f8;
        border-left: 5px solid #4169e1;
        padding: 20px;
        margin: 20px 0;
        border-radius: 5px;
    }
    .day-header {
        text-align: center;
        color: #2c3e50;
        margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# Inicialização do estado do aplicativo
if 'current_day' not in st.session_state:
    st.session_state.current_day = 1

# Carregar notas do Local Storage (simulado via session_state para esta versão)
if 'user_notes' not in st.session_state:
    st.session_state.user_notes = {}

# Título Principal
st.markdown('<h1 class="day-header">🕊️ 30-Day Prayer & Meditation</h1>', unsafe_allow_html=True)

# Navegação entre os dias
col_prev, col_day, col_next = st.columns([1, 2, 1])

with col_prev:
    if st.button("←", key="prev"):
        if st.session_state.current_day > 1:
            st.session_state.current_day -= 1
            st.rerun()

with col_day:
    st.markdown(f"<h3 style='text-align: center;'>Day {st.session_state.current_day}</h3>", unsafe_allow_html=True)

with col_next:
    if st.button("→", key="next"):
        if st.session_state.current_day < 30:
            st.session_state.current_day += 1
            st.rerun()

# Progresso
st.progress(st.session_state.current_day / 30)

# Dados do dia atual
day_data = PLANNER_DATA[st.session_state.current_day - 1]

st.markdown(f"## {day_data['title']}")

# Seção do Versículo
st.markdown(f"""
<div class="verse-box">
    <p style="font-weight: bold; color: #4CAF50; margin-bottom: 5px;">📖 {day_data['verse']}</p>
    <p style="font-style: italic; font-size: 1.1em;">"{day_data['verse_text']}"</p>
</div>
""", unsafe_allow_html=True)

# Seção de Reflexão
st.markdown(f"""
<div class="reflection-box">
    <p style="font-weight: bold; color: #b8860b; margin-bottom: 5px;">💭 Reflection</p>
    <p>{day_data['reflection']}</p>
</div>
""", unsafe_allow_html=True)

# Perguntas e Journaling
st.markdown("### 📝 Your Journal")
for i, q in enumerate(day_data['questions'], 1):
    st.markdown(f"**{i}. {q}**")

# Campo de texto para notas
note_key = f"note_{st.session_state.current_day}"
user_note = st.text_area(
    "Write your thoughts here...",
    value=st.session_state.user_notes.get(str(st.session_state.current_day), ""),
    height=200,
    key=note_key
)

# Botão de Salvar
if st.button("💾 Save My Reflection"):
    st.session_state.user_notes[str(st.session_state.current_day)] = user_note
    st.success("Reflection saved! 🙏")

# Seção de Oração
st.markdown(f"""
<div class="prayer-box">
    <p style="font-weight: bold; color: #4169e1; margin-bottom: 5px;">🙏 Closing Prayer</p>
    <p style="font-style: italic;">{day_data['prayer']}</p>
</div>
""", unsafe_allow_html=True)

# Rodapé
st.markdown("---")
st.markdown("<p style='text-align: center; color: #7f8c8d; font-size: 0.8em;'>Created for Lofi Biblical Music Community</p>", unsafe_allow_html=True)
