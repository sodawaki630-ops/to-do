import streamlit as st
import random
import time
import requests

# -------------------- CONFIG --------------------
st.set_page_config(page_title="Neon Math Rush", layout="centered")

API_URL = "https://api.npoint.io/4c5b3f571f3f6bf1573c"  # Mock Leaderboard JSON

# -------------------- CUSTOM NEON CSS --------------------
NEON_STYLE = """
<style>
body {
    background: #020204;
}
.title {
    font-family: 'Trebuchet MS';
    font-size: 42px;
    color: #00eaff;
    text-shadow: 0 0 20px #00eaff;
    text-align: center;
    margin-top: 10px;
}
.mode-btn {
    width: 100%;
    padding: 18px;
    border-radius: 14px;
    border: 2px solid #0ff;
    background: rgba(0, 255, 255, 0.07);
    color: #0ff;
    font-size: 22px;
    margin-top: 12px;
    cursor: pointer;
    transition: 0.2s;
}
.mode-btn:hover {
    background: rgba(0, 255, 255, 0.2);
    box-shadow: 0 0 15px #0ff;
}
.card {
    background: rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 20px;
    width: 100%;
    box-shadow: 0 0 15px #0ff;
}
</style>
"""

st.markdown(NEON_STYLE, unsafe_allow_html=True)

# -------------------- MULTI-PAGE NAV --------------------
page = st.sidebar.radio("📱 เมนู", ["🏠 หน้าแรก", "🧠 โหมดปกติ", "🔥 โหมดเร็ว", "🏆 Leaderboard"])

# -------------------- HOME --------------------
if page == "🏠 หน้าแรก":
    st.markdown("<div class='title'>NEON MATH RUSH</div>", unsafe_allow_html=True)
    st.write("")
    st.markdown("### 🎮 แอปคำนวณเร็วสไตล์เกมมือถือ\nเลือกโหมดด้านซ้ายเพื่อเริ่มเล่นได้เลย!")

# -------------------- MODE 1: NORMAL MODE --------------------
elif page == "🧠 โหมดปกติ":
    st.markdown("<div class='title'>🧠 โหมดปกติ</div>", unsafe_allow_html=True)

    num1 = random.randint(1, 20)
    num2 = random.randint(1, 20)
    op = random.choice(["+", "-"])
    correct = eval(f"{num1}{op}{num2}")

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"## {num1} {op} {num2} = ?")

    answer = st.text_input("ใส่คำตอบ:", "")
    if st.button("ตรวจคำตอบ"):
        if answer.strip().isdigit() and int(answer) == correct:
            st.success("✔ ถูกต้อง!")
        else:
            st.error("❌ ผิด ลองใหม่นะ")

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------- MODE 2: SPEED MODE --------------------
elif page == "🔥 โหมดเร็ว":
    st.markdown("<div class='title'>🔥 โหมดเร็ว (Timer)</div>", unsafe_allow_html=True)

    if "score" not in st.session_state:
        st.session_state.score = 0
        st.session_state.start_time = time.time()

    time_limit = 15  # วินาที

    remain = time_limit - int(time.time() - st.session_state.start_time)
    st.markdown(f"## ⏳ เวลาที่เหลือ: **{remain} วินาที**")

    if remain <= 0:
        st.warning(f"หมดเวลา! คะแนนของคุณคือ: {st.session_state.score}")
        name = st.text_input("ใส่ชื่อเพื่อบันทึกคะแนน:")
        if st.button("บันทึกคะแนน"):
            try:
                requests.post(API_URL, json={"name": name, "score": st.session_state.score})
            except:
                pass
        st.stop()

    # สุ่มโจทย์
    num1 = random.randint(1, 15)
    num2 = random.randint(1, 15)
    op = random.choice(["+", "-"])
    correct = eval(f"{num1}{op}{num2}")

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"## {num1} {op} {num2} = ?")

    ans = st.text_input("ตอบเร็ว!", key=new := random.random())

    if st.button("ยืนยัน"):
        if ans.strip().isdigit() and int(ans) == correct:
            st.success("✔ ถูกต้อง!")
            st.session_state.score += 1
        else:
            st.error("❌ ผิด แต้มไม่เพิ่ม")

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------- LEADERBOARD --------------------
elif page == "🏆 Leaderboard":
    st.markdown("<div class='title'>🏆 Leaderboard</div>", unsafe_allow_html=True)

    try:
        data = requests.get(API_URL).json()
    except:
        data = []

    st.markdown("### 👑 อันดับผู้ทำคะแนนสูงสุด")

    if len(data) == 0:
        st.info("ยังไม่มีคะแนน")
    else:
        sorted_data = sorted(data, key=lambda x: x["score"], reverse=True)
        for i, d in enumerate(sorted_data[:10]):
            st.markdown(
                f"**#{i+1}. {d['name']} — {d['score']} คะแนน**"
            )
