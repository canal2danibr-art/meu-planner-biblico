import streamlit as st
import json
import os
from datetime import datetime
from pathlib import Path
from planner_data import PLANNER_DATA

# Configuração da página
st.set_page_config(
    page_title="30-Day Prayer & Meditation Planner",
    page_icon="🕊️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para melhor aparência e responsividade mobile
st.markdown("""
    <style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .main {
        padding: 1rem;
    }
    
    @media (max-width: 768px) {
        .main {
            padding: 0.5rem;
        }
    }
    
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 12px;
        font-size: 16px;
        font-weight: 600;
        transition: background-color 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #45a049;
    }
    
    .verse-box {
        background-color: #f0f8ff;
        border-left: 4px solid #4CAF50;
        padding: 15px;
        margin: 15px 0;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .reflection-box {
        background-color: #fffacd;
        border-left: 4px solid #FFD700;
        padding: 15px;
        margin: 15px 0;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .prayer-box {
        background-color: #e6f3ff;
        border-left: 4px solid #4169E1;
        padding: 15px;
        margin: 15px 0;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .header-title {
        text-align: center;
        color: #2c3e50;
        font-size: 2.5em;
        margin-bottom: 10px;
        word-wrap: break-word;
    }
    
    @media (max-width: 768px) {
        .header-title {
            font-size: 1.8em;
        }
    }
    
    .header-subtitle {
        text-align: center;
        color: #7f8c8d;
        font-size: 1.2em;
        margin-bottom: 30px;
        word-wrap: break-word;
    }
    
    @media (max-width: 768px) {
        .header-subtitle {
            font-size: 1em;
        }
    }
    
    .day-title {
        color: #2c3e50;
        font-size: 2em;
        margin: 20px 0 10px 0;
    }
    
    @media (max-width: 768px) {
        .day-title {
            font-size: 1.5em;
        }
    }
    
    .verse-reference {
        font-weight: 600;
        color: #4CAF50;
        font-size: 1.1em;
    }
    
    .verse-text {
        font-style: italic;
        color: #333;
        margin-top: 10px;
        line-height: 1.6;
    }
    
    .question-text {
        background-color: #f9f9f9;
        padding: 10px;
        margin: 8px 0;
        border-radius: 3px;
        border-left: 3px solid #4CAF50;
    }
    
    .progress-container {
        margin: 20px 0;
    }
    
    .footer {
        text-align: center;
        color: #7f8c8d;
        font-size: 0.9em;
        margin-top: 40px;
        padding: 20px;
        border-top: 1px solid #ddd;
    }
    
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 12px;
        border-radius: 5px;
        margin: 10px 0;
    }
    
    .note-saved-indicator {
        display: inline-block;
        background-color: #4CAF50;
        color: white;
        padding: 5px 10px;
        border-radius: 3px;
        font-size: 0.9em;
        margin-left: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Diretório para armazenar notas
NOTES_DIR = Path("user_notes")
NOTES_DIR.mkdir(exist_ok=True)

# Função para obter o arquivo de notas do usuário
def get_user_notes_file():
    # Usar um ID de sessão simples (pode ser melhorado com autenticação real)
    user_id = st.session_state.get('user_id', 'default_user')
    return NOTES_DIR / f"{user_id}_notes.json"

# Função para carregar todas as notas do usuário
def load_all_notes():
    notes_file = get_user_notes_file()
    if notes_file.exists():
        try:
            with open(notes_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

# Função para salvar notas
def save_all_notes(notes_dict):
    notes_file = get_user_notes_file()
    try:
        with open(notes_file, 'w', encoding='utf-8') as f:
            json.dump(notes_dict, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.error(f"Erro ao salvar notas: {e}")
        return False

# Inicializar session state
if 'current_day' not in st.session_state:
    st.session_state.current_day = 1

if 'user_id' not in st.session_state:
    st.session_state.user_id = 'default_user'

if 'notes' not in st.session_state:
    st.session_state.notes = load_all_notes()

if 'last_saved_day' not in st.session_state:
    st.session_state.last_saved_day = None

# Header
st.markdown('<div class="header-title">🕊️ 30-Day Prayer & Meditation Planner</div>', unsafe_allow_html=True)
st.markdown('<div class="header-subtitle">A Journey to Peace, Identity, and Purpose in Christ</div>', unsafe_allow_html=True)

# Layout com sidebar
col_sidebar, col_main = st.columns([1, 3], gap="medium")

with col_sidebar:
    st.markdown("### 📅 Navigation")
    st.markdown("---")
    
    # Seletor de dia
    selected_day = st.slider(
        "Select Day",
        min_value=1,
        max_value=30,
        value=st.session_state.current_day,
        step=1
    )
    
    st.session_state.current_day = selected_day
    
    # Botões de navegação
    st.markdown("### Quick Navigation")
    nav_col1, nav_col2 = st.columns(2)
    
    with nav_col1:
        if st.button("← Previous", key="prev_btn", use_container_width=True):
            if st.session_state.current_day > 1:
                st.session_state.current_day -= 1
                st.rerun()
    
    with nav_col2:
        if st.button("Next →", key="next_btn", use_container_width=True):
            if st.session_state.current_day < 30:
                st.session_state.current_day += 1
                st.rerun()
    
    # Mostrar progresso
    st.markdown("### Your Progress")
    progress = st.session_state.current_day / 30
    st.progress(progress)
    st.write(f"**Day {st.session_state.current_day} of 30**")
    
    # Estatísticas
    st.markdown("### Statistics")
    notes_saved = len([n for n in st.session_state.notes.values() if n.strip()])
    st.metric("Notes Saved", notes_saved)
    
    # Informações
    st.markdown("---")
    st.markdown("### About This Planner")
    st.markdown("""
    This 30-day journey is designed to guide you through:
    
    - **Days 1-10**: Foundations of Peace
    - **Days 11-20**: Identity & Purpose
    - **Days 21-30**: Faith & Impact
    
    Take time to reflect, journal, and pray each day.
    """)

with col_main:
    # Obter dados do dia atual
    current_data = PLANNER_DATA[st.session_state.current_day - 1]
    
    # Exibir conteúdo do dia
    st.markdown(f'<div class="day-title">Day {current_data["day"]}: {current_data["title"]}</div>', unsafe_allow_html=True)
    
    # Versículo
    st.markdown('<div class="verse-box">', unsafe_allow_html=True)
    st.markdown(f'<div class="verse-reference">📖 {current_data["verse"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="verse-text">"{current_data["verse_text"]}"</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Reflexão
    st.markdown('<div class="reflection-box">', unsafe_allow_html=True)
    st.markdown("### 💭 Reflection")
    st.markdown(current_data['reflection'])
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Perguntas para Meditação
    st.markdown("### 🤔 Questions for Meditation & Journaling")
    for i, question in enumerate(current_data['questions'], 1):
        st.markdown(f'<div class="question-text"><strong>{i}. {question}</strong></div>', unsafe_allow_html=True)
    
    # Espaço para notas
    st.markdown("### 📝 Your Notes")
    current_note = st.session_state.notes.get(str(st.session_state.current_day), "")
    
    note_text = st.text_area(
        "Write your thoughts, reflections, and answers to the questions above:",
        value=current_note,
        height=200,
        key=f"note_{st.session_state.current_day}",
        placeholder="Share your reflections here..."
    )
    
    # Salvar nota com feedback visual
    col_save, col_status = st.columns([3, 1])
    
    with col_save:
        if st.button("💾 Save Note", key=f"save_{st.session_state.current_day}", use_container_width=True):
            st.session_state.notes[str(st.session_state.current_day)] = note_text
            if save_all_notes(st.session_state.notes):
                st.session_state.last_saved_day = st.session_state.current_day
                st.success("✅ Note saved successfully!")
            else:
                st.error("❌ Error saving note. Please try again.")
    
    # Oração
    st.markdown('<div class="prayer-box">', unsafe_allow_html=True)
    st.markdown("### 🙏 Closing Prayer")
    st.markdown(f"*{current_data['prayer']}*")
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
    <div class="footer">
    <p>Created with ❤️ for Lofi Biblical Music Community</p>
    <p>May this journey bring you closer to God's peace and purpose.</p>
    <p style="margin-top: 15px; font-size: 0.8em; color: #999;">
    Your notes are saved locally on your device. They are private and secure.
    </p>
    </div>
""", unsafe_allow_html=True)
