import streamlit as st

st.set_page_config(
    page_title="Math Quiz",
    page_icon="🧮",
    layout="centered"
)

st.markdown("""
<style>
body {
    background-color: #121212;
    color: white;
}

.menu-title {
    font-size: 42px;
    text-align: center;
    color: #00eaff;
    font-weight: bold;
    margin-bottom: 30px;
}

.menu-button {
    background: #1f1f1f;
    border: 2px solid #00eaff;
    padding: 15px;
    border-radius: 15px;
    font-size: 22px;
    text-align: center;
    margin: 10px 0;
}

.menu-button:hover {
    background: #00eaff;
    color: black;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='menu-title'>⚡ Math Quiz</div>", unsafe_allow_html=True)

st.page_link("pages/1_start_game.py", label="🎮 เริ่มเล่นเกม", icon="🔥")
st.page_link("pages/2_select_mode.py", label="⚡ เลือกโหมด", icon="⚙️")
st.page_link("pages/3_leaderboard.py", label="🏆 อันดับผู้เล่น", icon="📊")
