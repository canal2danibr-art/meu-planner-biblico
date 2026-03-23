import streamlit as st
import json
from planner_data_en import PLANNER_DATA_LOFI

# Page Configuration
st.set_page_config(
    page_title="30-Day Prayer Planner",
    page_icon="🕊️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============= LOFI COLOR PALETTE =============
# Soft pastel colors: Beige, Olive Green, Ash Blue
COLORS = {
    "beige": "#E8DCC8",
    "olive_green": "#7A9B6F",
    "ash_blue": "#8B9BA8",
    "white": "#FEFDFB",
    "dark_text": "#4A4A4A",
    "light_text": "#8B8B8B",
    "accent_gold": "#C9A961"
}

# ============= MINIMALIST CSS STYLES =============
st.markdown(f"""
    <style>
    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}
    
    body {{
        background-color: {COLORS["white"]};
        font-family: 'Georgia', 'Garamond', serif;
        color: {COLORS["dark_text"]};
    }}
    
    .main {{
        padding: 2rem 1rem;
        background-color: {COLORS["white"]};
    }}
    
    /* Main Header */
    .header-container {{
        text-align: center;
        margin-bottom: 2rem;
        padding: 2rem 0;
        border-bottom: 2px solid {COLORS["beige"]};
    }}
    
    .header-title {{
        font-size: 2.5em;
        color: {COLORS["olive_green"]};
        font-weight: 300;
        letter-spacing: 2px;
        margin-bottom: 0.5rem;
    }}
    
    .header-subtitle {{
        font-size: 1em;
        color: {COLORS["light_text"]};
        font-weight: 300;
        font-style: italic;
    }}
    
    .day-indicator {{
        font-size: 0.9em;
        color: {COLORS["ash_blue"]};
        margin-top: 1rem;
        letter-spacing: 1px;
    }}
    
    /* Content Sections */
    .section-box {{
        background-color: {COLORS["white"]};
        border-left: 4px solid {COLORS["olive_green"]};
        padding: 1.5rem;
        margin: 1.5rem 0;
        border-radius: 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }}
    
    .section-title {{
        font-size: 0.85em;
        color: {COLORS["olive_green"]};
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 1rem;
        font-weight: 600;
    }}
    
    .verse-box {{
        background-color: {COLORS["beige"]};
        border-left: 4px solid {COLORS["olive_green"]};
        padding: 1.5rem;
        margin: 1.5rem 0;
        border-radius: 0;
    }}
    
    .verse-reference {{
        font-size: 0.9em;
        color: {COLORS["olive_green"]};
        font-weight: 600;
        margin-bottom: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    
    .verse-text {{
        font-size: 1.1em;
        color: {COLORS["dark_text"]};
        font-style: italic;
        line-height: 1.8;
        margin: 1rem 0;
    }}
    
    .reflection-box {{
        background-color: {COLORS["white"]};
        border-left: 4px solid {COLORS["ash_blue"]};
        padding: 1.5rem;
        margin: 1.5rem 0;
    }}
    
    .reflection-question {{
        font-size: 1em;
        color: {COLORS["dark_text"]};
        font-style: italic;
        line-height: 1.6;
        margin: 1rem 0;
    }}
    
    .stTextArea textarea {{
        background-color: {COLORS["white"]};
        border: 1px solid {COLORS["beige"]};
        color: {COLORS["dark_text"]};
        font-family: 'Georgia', serif;
        border-radius: 0;
        padding: 1rem;
    }}
    
    .stCheckbox {{
        margin: 0.5rem 0;
    }}
    
    .stCheckbox label {{
        color: {COLORS["dark_text"]};
        font-size: 1em;
    }}
    
    /* Buttons */
    .stButton>button {{
        background-color: {COLORS["olive_green"]};
        color: white;
        border: none;
        border-radius: 0;
        padding: 0.8rem 2rem;
        font-size: 0.95em;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
        width: 100%;
        transition: background-color 0.3s ease;
    }}
    
    .stButton>button:hover {{
        background-color: {COLORS["ash_blue"]};
    }}
    
    /* Navigation */
    .nav-container {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 2rem 0;
        gap: 1rem;
    }}
    
    .nav-button {{
        flex: 1;
    }}
    
    .day-counter {{
        text-align: center;
        font-size: 0.9em;
        color: {COLORS["light_text"]};
        flex: 2;
    }}
    
    /* Progress Bar */
    .stProgress {{
        margin: 2rem 0;
    }}
    
    /* Intentional White Space */
    .spacer {{
        margin: 2rem 0;
    }}
    
    /* Footer */
    .footer {{
        text-align: center;
        color: {COLORS["light_text"]};
        font-size: 0.85em;
        margin-top: 3rem;
        padding-top: 2rem;
        border-top: 1px solid {COLORS["beige"]};
        font-style: italic;
    }}
    
    /* Week Theme */
    .week-theme {{
        text-align: center;
        font-size: 0.9em;
        color: {COLORS["accent_gold"]};
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 1rem;
    }}
    
    /* Checklist */
    .checklist-item {{
        padding: 0.8rem 0;
        border-bottom: 1px solid {COLORS["beige"]};
    }}
    
    .checklist-item:last-child {{
        border-bottom: none;
    }}
    </style>
""", unsafe_allow_html=True)

# ============= STATE INITIALIZATION =============
if 'current_day' not in st.session_state:
    st.session_state.current_day = 1

if 'user_data' not in st.session_state:
    st.session_state.user_data = {}

# ============= HELPER FUNCTIONS =============
def get_day_data(day):
    return PLANNER_DATA_LOFI[day - 1]

def save_user_data(day, data_type, value):
    """Saves user data for a specific day"""
    if str(day) not in st.session_state.user_data:
        st.session_state.user_data[str(day)] = {}
    st.session_state.user_data[str(day)][data_type] = value

def get_user_data(day, data_type):
    """Retrieves user data for a specific day"""
    if str(day) in st.session_state.user_data:
        return st.session_state.user_data[str(day)].get(data_type, "")
    return ""

# ============= MAIN INTERFACE =============

# Header
st.markdown(f"""
<div class="header-container">
    <div class="header-title">🕊️ 30-Day Prayer Planner</div>
    <div class="header-subtitle">A Journey to Peace, Identity & Purpose in Christ</div>
    <div class="day-indicator">Day {st.session_state.current_day} of 30</div>
</div>
""", unsafe_allow_html=True)

# Get day data
day_data = get_day_data(st.session_state.current_day)

# Week Theme
st.markdown(f'<div class="week-theme">Week {day_data["week"]}: {day_data["week_theme"]}</div>', unsafe_allow_html=True)

# Day Title
st.markdown(f"## {day_data['title']}")

# Progress
progress_value = st.session_state.current_day / 30
st.progress(progress_value)

# ============= SECTION 1: VERSE OF THE DAY =============
st.markdown(f"""
<div class="verse-box">
    <div class="verse-reference">📖 {day_data['verse']}</div>
    <div class="verse-text">"{day_data['verse_text']}"</div>
</div>
""", unsafe_allow_html=True)

# Intentional white space
st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

# ============= SECTION 2: GUIDED REFLECTION =============
st.markdown(f"""
<div class="reflection-box">
    <div class="section-title">💭 Reflection</div>
    <div class="reflection-question">{day_data['reflection_question']}</div>
</div>
""", unsafe_allow_html=True)

# Input field for reflection
reflection_text = st.text_area(
    "Your thoughts:",
    value=get_user_data(st.session_state.current_day, "reflection"),
    height=100,
    key=f"reflection_{st.session_state.current_day}",
    label_visibility="collapsed"
)

# ============= SECTION 3: GRATITUDE SPACE =============
st.markdown("""
<div class="section-box">
    <div class="section-title">🙏 Gratitude</div>
    <p style="color: #8B8B8B; font-size: 0.9em; margin-bottom: 1rem;">List 3 blessings you're grateful for today:</p>
</div>
""", unsafe_allow_html=True)

gratitude_1 = st.text_input(
    "Blessing 1:",
    value=get_user_data(st.session_state.current_day, "gratitude_1"),
    key=f"gratitude_1_{st.session_state.current_day}",
    label_visibility="collapsed"
)

gratitude_2 = st.text_input(
    "Blessing 2:",
    value=get_user_data(st.session_state.current_day, "gratitude_2"),
    key=f"gratitude_2_{st.session_state.current_day}",
    label_visibility="collapsed"
)

gratitude_3 = st.text_input(
    "Blessing 3:",
    value=get_user_data(st.session_state.current_day, "gratitude_3"),
    key=f"gratitude_3_{st.session_state.current_day}",
    label_visibility="collapsed"
)

# White space
st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

# ============= SECTION 4: MY PRAYERS =============
st.markdown("""
<div class="section-box">
    <div class="section-title">🕊️ My Prayers</div>
</div>
""", unsafe_allow_html=True)

prayer_text = st.text_area(
    "Write your prayers and intercessions:",
    value=get_user_data(st.session_state.current_day, "prayer"),
    height=120,
    key=f"prayer_{st.session_state.current_day}",
    label_visibility="collapsed"
)

# White space
st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

# ============= SECTION 5: SPIRITUAL SELF-CARE CHECKLIST =============
st.markdown("""
<div class="section-box">
    <div class="section-title">✓ Spiritual Self-Care Checklist</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    prayed = st.checkbox(
        "Prayed",
        value=get_user_data(st.session_state.current_day, "prayed") == True,
        key=f"prayed_{st.session_state.current_day}"
    )

with col2:
    read_word = st.checkbox(
        "Read God's Word",
        value=get_user_data(st.session_state.current_day, "read_word") == True,
        key=f"read_word_{st.session_state.current_day}"
    )

with col3:
    worship_music = st.checkbox(
        "Worship Music",
        value=get_user_data(st.session_state.current_day, "worship_music") == True,
        key=f"worship_music_{st.session_state.current_day}"
    )

# White space
st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

# ============= SAVE BUTTON =============
if st.button("💾 Save My Reflection"):
    save_user_data(st.session_state.current_day, "reflection", reflection_text)
    save_user_data(st.session_state.current_day, "gratitude_1", gratitude_1)
    save_user_data(st.session_state.current_day, "gratitude_2", gratitude_2)
    save_user_data(st.session_state.current_day, "gratitude_3", gratitude_3)
    save_user_data(st.session_state.current_day, "prayer", prayer_text)
    save_user_data(st.session_state.current_day, "prayed", prayed)
    save_user_data(st.session_state.current_day, "read_word", read_word)
    save_user_data(st.session_state.current_day, "worship_music", worship_music)
    
    st.success("✨ Your reflection has been saved.")

# White space
st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

# ============= NAVIGATION =============
st.markdown("---")

nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])

with nav_col1:
    if st.button("← Previous", use_container_width=True):
        if st.session_state.current_day > 1:
            st.session_state.current_day -= 1
            st.rerun()

with nav_col2:
    st.markdown(f"<div class=\'day-counter\'>Day {st.session_state.current_day} / 30</div>", unsafe_allow_html=True)

with nav_col3:
    if st.button("Next →", use_container_width=True):
        if st.session_state.current_day < 30:
            st.session_state.current_day += 1
            st.rerun()

# ============= FOOTER =============
st.markdown(f"""
<div class="footer">
    <p>Created with love for the Lofi Biblical Music community</p>
    <p>May this journey bring you closer to God's peace and purpose</p>
</div>
""", unsafe_allow_html=True)
