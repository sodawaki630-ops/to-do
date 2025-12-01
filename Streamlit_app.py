import streamlit as st
import random

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(page_title="⚡ เกมคิดเลขเร็ว", page_icon="🧮", layout="centered")

# ----------------------------
# Custom CSS UI
# ----------------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #f6d365, #fda085);
}

.title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    color: #ffffff;
    margin-bottom: 10px;
}

.quiz-box {
    background: #ffffff;
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0px 5px 18px rgba(0,0,0,0.2);
    text-align: center;
}

.question-text {
    font-size: 28px;
    font-weight: bold;
    margin-bottom: 20px;
    color: #333333;
}

.big-emoji {
    font-size: 90px;
    text-align: center;
}

.answer-box input {
    font-size: 22px !important;
    text-align: center;
}

.button {
    width: 100%;
    font-size: 22px;
    padding: 10px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)


# ----------------------------
# Session State Setup
# ----------------------------
if "score" not in st.session_state:
    st.session_state.score = 0

if "round" not in st.session_state:
    st.session_state.round = 1

if "num1" not in st.session_state:
    st.session_state.num1 = random.randint(1, 20)

if "num2" not in st.session_state:
    st.session_state.num2 = random.randint(1, 20)

if "operator" not in st.session_state:
    st.session_state.operator = random.choice(["+", "-", "×"])

if "show_result" not in st.session_state:
    st.session_state.show_result = None  # True = ถูก, False = ผิด


# ----------------------------
# Function to Generate New Question
# ----------------------------
def new_question():
    st.session_state.num1 = random.randint(1, 20)
    st.session_state.num2 = random.randint(1, 20)
    st.session_state.operator = random.choice(["+", "-", "×"])
    st.session_state.round += 1
    st.session_state.show_result = None


# ----------------------------
# Title
# ----------------------------
st.markdown("<div class='title'>⚡ เกมคิดเลขเร็ว 🧮</div>", unsafe_allow_html=True)

# Score + Round
st.markdown(f"### ⭐ คะแนน: **{st.session_state.score}** | 🔁 รอบที่: **{st.session_state.round}**")


# ----------------------------
# Question Box
# ----------------------------
with st.container():
    st.markdown("<div class='quiz-box'>", unsafe_allow_html=True)

    q = f"{st.session_state.num1} {st.session_state.operator} {st.session_state.num2}"
    st.markdown(f"<div class='question-text'>{q}</div>", unsafe_allow_html=True)

    answer = st.text_input("คำตอบของคุณ:", key="answer_input")

    if st.button("ส่งคำตอบ", use_container_width=True):
        try:
            user_ans = int(answer)

            # คำนวณคำตอบจริง
            if st.session_state.operator == "+":
                correct = st.session_state.num1 + st.session_state.num2
            elif st.session_state.operator == "-":
                correct = st.session_state.num1 - st.session_state.num2
            else:
                correct = st.session_state.num1 * st.session_state.num2

            # ตรวจคำตอบ
            if user_ans == correct:
                st.session_state.score += 1
                st.session_state.show_result = True
            else:
                st.session_state.show_result = False

        except:
            st.warning("❗ กรุณากรอกตัวเลข")
    
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# ----------------------------
# Result Popup
# ----------------------------
if st.session_state.show_result is True:
    st.markdown("<p class='big-emoji'>🎉</p>", unsafe_allow_html=True)
    st.success("ถูกต้อง! เยี่ยมมาก 🎉")

    if st.button("ข้อต่อไป ▶",
