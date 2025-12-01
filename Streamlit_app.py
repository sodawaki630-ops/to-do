import streamlit as st
import random
import time
import pandas as pd
import os

st.set_page_config(page_title="Play Quiz", layout="centered")

# ------------------------
# Setup
# ------------------------
if "score" not in st.session_state:
    st.session_state.score = 0

if "round" not in st.session_state:
    st.session_state.round = 1

if "result" not in st.session_state:
    st.session_state.result = None

if "game_mode" not in st.session_state:
    st.session_state.game_mode = "Easy"


def generate_question():
    mode = st.session_state.game_mode

    if mode == "Easy":
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        op = random.choice(["+", "-"])

    elif mode == "Medium":
        a = random.randint(5, 15)
        b = random.randint(1, 10)
        op = random.choice(["+", "-", "×"])

    elif mode == "Hard":
        a = random.randint(10, 40)
        b = random.randint(5, 25)
        op = random.choice(["+", "-", "×", "÷"])

    else:  # Speed Mode
        a = random.randint(1, 20)
        b = random.randint(1, 20)
        op = random.choice(["+", "-", "×"])

    if op == "÷":
        b = random.randint(1, 10)

    st.session_state.a = a
    st.session_state.b = b
    st.session_state.op = op


generate_question()

# ------------------------
# UI / CSS
# ------------------------
st.markdown("""
<style>
body {
    background-color: #121212;
    color: #ffffff;
}

.box {
    background: #1e1e1e;
    padding: 25px;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}

.question {
    font-size: 35px;
    font-weight: bold;
}

.big-emoji {
    font-size: 90px;
}
</style>
""", unsafe_allow_html=True)

# ------------------------
# Question Box
# ------------------------
st.markdown(f"<h2>🎮 Mode: {st.session_state.game_mode}</h2>", unsafe_allow_html=True)

st.markdown(f"⭐ คะแนน: **{st.session_state.score}** | 🔁 รอบ: **{st.session_state.round}**")

st.markdown("<div class='box'>", unsafe_allow_html=True)
st.markdown(f"<div class='question'>{st.session_state.a} {st.session_state.op} {st.session_state.b}</div>",
            unsafe_allow_html=True)

user_answer = st.text_input("คำตอบ:", key="ans")

if st.button("ส่งคำตอบ ✓"):
    try:
        ans = int(user_answer)

        if st.session_state.op == "+":
            correct = st.session_state.a + st.session_state.b
        elif st.session_state.op == "-":
            correct = st.session_state.a - st.session_state.b
        elif st.session_state.op == "×":
            correct = st.session_state.a * st.session_state.b
        else:
            correct = st.session_state.a // st.session_state.b

        if ans == correct:
            st.session_state.score += 1
            st.session_state.result = "correct"
        else:
            st.session_state.result = "wrong"

        st.session_state.round += 1
        generate_question()
        st.rerun()

    except:
        st.warning("กรุณากรอกตัวเลข")

st.markdown("</div>", unsafe_allow_html=True)

# ------------------------
# Result Emoji
# ------------------------
if st.session_state.result == "correct":
    st.markdown("<p class='big-emoji'>🎉</p>", unsafe_allow_html=True)

elif st.session_state.result == "wrong":
    st.markdown("<p class='big-emoji'>❌</p>", unsafe_allow_html=True)


# ------------------------
# Save Score
# ------------------------
if st.button("บันทึกคะแนน 🏆"):
    name = st.text_input("ชื่อผู้เล่น", key="namebox")

    if name and st.button("ยืนยันบันทึก"):
        row = {"name": name, "score": st.session_state.score, "mode": st.session_state.game_mode}

        if os.path.exists("leaderboard.csv"):
            df = pd.read_csv("leaderboard.csv")
        else:
            df = pd.DataFrame(columns=["name", "score", "mode"])

        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
        df.to_csv("leaderboard.csv", index=False)

        st.success("บันทึกสำเร็จ!")
