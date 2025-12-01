import streamlit as st

st.set_page_config(layout="centered")

st.title("⚡ เลือกโหมดการเล่น")

mode = st.radio(
    "เลือกความยาก:",
    ["Easy", "Medium", "Hard", "Speed Mode"]
)

if st.button("เริ่มเกม ▶"):
    st.session_state.game_mode = mode
    st.switch_page("1_start_game.py")
