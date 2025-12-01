import streamlit as st

st.set_page_config(
    page_title="⚡ Math Quiz Dark Mode",
    page_icon="🧮",
    layout="centered"
)

# ---------- Dark Mode CSS ----------
st.markdown("""
<style>
body {
    background-color: #121212;
    color: #ffffff;
}
.title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    margin-top: 20px;
    color: #00eaff;
}
.menu-btn {
    background: #1f1f1f;
    border: 2px solid #00eaff;
    padding: 12px;
    border-radius: 12px;
    text-align: center;
    font-size: 22px;
    margin: 10px 0;
}
.menu-btn:hover {
    background: #00eaff;
    color: #000;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>⚡ Math Quiz - Dark Mode</div>", unsafe_allow_html=True)

st.page_link("pages/1_🎮_เริ่มเกม.py", label="🎮 เริ่มเล่นเกม", icon="🔥")
st.page_link("pages/2_⚡_เลือกโหมด.py", label="⚡ เลือกโหมด", icon="⚙️")
st.page_link("pages/3_🏆_อันดับผู้เล่น.py", label="🏆 อันดับผู้เล่น", icon="📊")
