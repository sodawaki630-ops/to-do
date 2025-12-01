import streamlit as st
import random

# ตั้งค่าเว็บ
st.set_page_config(page_title="🧠 Fast Math Game", page_icon="➕", layout="centered")

# CSS ความสวยงาม
st.markdown("""
<style>
.app-title {
    text-align:center; 
    color:#FF5733; 
    font-weight:bold; 
    font-size:40px;
}
.question-box {
    background-color:#F0F8FF;
    padding:20px;
    border-radius:15px;
    margin-bottom:20px;
    box-shadow:2px 2px 10px #aaa;
}
.option-button button {
    background-color:#1E90FF !important;
    color:white !important;
    font-size:20px !important;
    padding:12px 20px;
    border-radius:12px !important;
    margin-top:10px;
}
.big-emoji {
    font-size:120px;
    text-align:center;
}
.info-box {
    text-align:center;
    font-size:20px;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 class='app-title'>🧠 Fast Math Game ➕</h1>", unsafe_allow_html=True)
st.write("ตอบโจทย์ให้เร็ว สะสมคะแนนให้ได้มากที่สุด!")

# ฟังก์ชันสร้างโจทย์คณิตแบบง่าย
def generate_question():
    a = random.randint(1, 20)
    b = random.randint(1, 20)
    ops = ["+", "-", "×"]
    op = random.choice(ops)

    if op == "+":
        ans = a + b
    elif op == "-":
        ans = a - b
    else:
        ans = a * b

    # ตัวเลือกสุ่ม
    options = [ans,
               ans + random.randint(1, 5),
               ans - random.randint(1, 5),
               ans + random.randint(-3, 3)]
    options = list(set(options))  # กันซ้ำ
    random.shuffle(options)

    return f"{a} {op} {b} = ?", ans, options

# session state
if "question" not in st.session_state:
    q, ans, opts = generate_question()
    st.session_state.question = q
    st.session_state.answer = ans
    st.session_state.options = opts
    st.session_state.score = 0
    st.session_state.round = 1
    st.session_state.answered = False

# แสดงคำถาม
st.markdown(f"<div class='question-box'><h2>{st.session_state.question}</h2></div>", unsafe_allow_html=True)

# ปุ่มตัวเลือก
for opt in st.session_state.options:
    if st.button(str(opt)) and not st.session_state.answered:
        st.session_state.answered = True
        if opt == st.session_state.answer:
            st.markdown("<div class='big-emoji'>🎉</div>", unsafe_allow_html=True)
            st.success("ตอบถูก! เก่งมาก 👏")
            st.session_state.score += 1
        else:
            st.markdown("<div class='big-emoji'>❌</div>", unsafe_allow_html=True)
            st.error(f"ผิด! คำตอบที่ถูกคือ {st.session_state.answer}")

# ปุ่มไปคำถามต่อไป
if st.session_state.answered:
    if st.button("➡️ คำถามต่อไป"):
        q, ans, opts = generate_question()
        st.session_state.question = q
        st.session_state.answer = ans
        st.session_state.options = opts
        st.session_state.round += 1
        st.session_state.answered = False
        st.experimental_rerun()

# แสดงคะแนน
st.markdown(
    f"<p class='info-box'>รอบที่ {st.session_state.round} | คะแนน: {st.session_state.score}</p>",
    unsafe_allow_html=True
)
