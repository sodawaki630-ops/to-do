# app.py
import streamlit as st
import random
import time
import pandas as pd
import os

# -------------------------
# Page config & Neon CSS
# -------------------------
st.set_page_config(page_title="Neon Math Rush", layout="centered", page_icon="🧮")

NEON_CSS = """
<style>
body { background: #020204; color: #e6f7ff; }
.title { font-size:36px; text-align:center; color:#00eaff; text-shadow: 0 0 10px #00eaff; margin-bottom: 8px; }
.subtitle { text-align:center; color:#8be9ff; margin-bottom: 18px; }
.card {
  background: linear-gradient(90deg, rgba(255,255,255,0.03), rgba(0,255,255,0.02));
  border: 1px solid rgba(0,255,255,0.12);
  padding: 18px;
  border-radius: 14px;
  box-shadow: 0 8px 30px rgba(0,255,255,0.03);
}
.big-emoji { font-size: 96px; text-align:center; margin:10px 0; }
.side-note { color:#a9f0ff; font-size:14px; text-align:center; margin-top:8px; }
.btn-neon {
  background: transparent;
  color: #00f0ff;
  border: 2px solid #00f0ff;
  padding: 10px 14px;
  border-radius: 12px;
  font-size: 16px;
  width:100%;
}
.btn-neon:hover { background: rgba(0,255,255,0.06); box-shadow:0 0 10px #00eaff; }
.leader-row { padding:8px 6px; border-bottom:1px solid rgba(255,255,255,0.04); }
</style>
"""
st.markdown(NEON_CSS, unsafe_allow_html=True)

# -------------------------
# Helper: generate question
# -------------------------
def generate_question(mode):
    if mode == "Easy":
        a = random.randint(1, 10); b = random.randint(1, 10); op = random.choice(["+", "-"])
    elif mode == "Medium":
        a = random.randint(5, 20); b = random.randint(1, 15); op = random.choice(["+", "-", "×"])
    elif mode == "Hard":
        a = random.randint(10, 80); b = random.randint(5, 30); op = random.choice(["+", "-", "×", "÷"])
    else:  # Speed
        a = random.randint(1, 15); b = random.randint(1, 15); op = random.choice(["+", "-", "×"])
    # ensure integer division for ÷
    if op == "÷":
        # make result integer
        b = random.randint(1, 12)
        a = b * random.randint(1, 10)
    # compute correct int answer
    if op == "+":
        correct = a + b
    elif op == "-":
        correct = a - b
    elif op == "×":
        correct = a * b
    else:
        correct = a // b
    return {"a": a, "b": b, "op": op, "correct": correct}

# -------------------------
# Initialize session state
# -------------------------
if "page" not in st.session_state:
    st.session_state.page = "Home"

if "game_mode" not in st.session_state:
    st.session_state.game_mode = "Easy"

if "score" not in st.session_state:
    st.session_state.score = 0

if "round" not in st.session_state:
    st.session_state.round = 0

# For current question storage to avoid regen on every rerun:
if "current_q" not in st.session_state:
    st.session_state.current_q = generate_question(st.session_state.game_mode)

# For speed mode timer:
if "speed_start" not in st.session_state:
    st.session_state.speed_start = None

# For result feedback
if "last_result" not in st.session_state:
    st.session_state.last_result = None  # "correct" / "wrong" / None

# -------------------------
# Sidebar / Navigation
# -------------------------
st.sidebar.title("📱 Menu")
page = st.sidebar.radio("", ["Home", "Play", "Speed Mode", "Leaderboard", "Settings"])
st.session_state.page = page

# -------------------------
# Home Page
# -------------------------
st.markdown("<div class='title'>NEON MATH RUSH</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>คิดเร็ว ตอบไว สะสมคะแนน — Dark Neon Theme</div>", unsafe_allow_html=True)

if page == "Home":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 🎮 วิธีเล่นโดยย่อ")
    st.markdown("- เลือกเมนู `Play` หรือ `Speed Mode` จากแถบซ้าย")
    st.markdown("- ตอบคำถามให้ถูกเพื่อเพิ่มคะแนน")
    st.markdown("- ใน Speed Mode จะมีตัวจับเวลา ให้ตอบให้ได้มากที่สุดก่อนหมดเวลา")
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# Play Page (normal modes)
# -------------------------
elif page == "Play":
    st.session_state.speed_start = None  # reset speed timer if coming from speed
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.markdown("### เลือกระดับความยาก")
    mode = st.selectbox("", ["Easy", "Medium", "Hard"], index=["Easy","Medium","Hard"].index(st.session_state.game_mode) if st.session_state.game_mode in ["Easy","Medium","Hard"] else 0)
    st.session_state.game_mode = mode

    # Generate new question only when user requests next or first round
    if st.button("เริ่มคำถามใหม่ ▶", key="new_q"):
        st.session_state.current_q = generate_question(st.session_state.game_mode)
        st.session_state.last_result = None
        st.session_state.round += 1
        st.experimental_rerun()

    q = st.session_state.current_q
    st.markdown(f"<div style='text-align:center; margin: 10px 0;'><h2 style='color:#bffeff'>{q['a']} {q['op']} {q['b']} = ?</h2></div>", unsafe_allow_html=True)

    # text_input has fixed key so it persists user entry until submit
    user = st.text_input("คำตอบของคุณ:", key="normal_answer")

    if st.button("ส่งคำตอบ", key="submit_normal"):
        if user.strip().lstrip("-").isdigit():
            user_ans = int(user)
            if user_ans == q["correct"]:
                st.session_state.score += 1
                st.session_state.last_result = "correct"
            else:
                st.session_state.last_result = "wrong"
            # keep question until user presses new question; but you can regenerate:
            # regenerate automatically:
            st.session_state.current_q = generate_question(st.session_state.game_mode)
            st.session_state.round += 1
            st.experimental_rerun()
        else:
            st.warning("กรุณากรอกตัวเลข เช่น 12 หรือ -5")

    # Feedback
    if st.session_state.last_result == "correct":
        st.markdown("<div class='big-emoji'>🎉</div>", unsafe_allow_html=True)
        st.success("ถูกต้อง! คะแนน +1")
    elif st.session_state.last_result == "wrong":
        st.markdown("<div class='big-emoji'>❌</div>", unsafe_allow_html=True)
        st.error(f"ผิดแล้ว คำตอบที่ถูกคือ {q['correct']}")

    st.markdown(f"<div class='side-note'>รอบ: {st.session_state.round} | คะแนน: {st.session_state.score}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# Speed Mode Page
# -------------------------
elif page == "Speed Mode":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#bffeff'>🔥 โหมดเร็ว — ตอบให้ได้มากที่สุดในเวลาที่กำหนด</h3>", unsafe_allow_html=True)

    time_limit = st.slider("เลือกเวลาทดสอบ (วินาที)", 10, 60, 20, 5)

    if st.session_state.speed_start is None:
        if st.button("เริ่มโหมดเร็ว ▶"):
            st.session_state.speed_start = time.time()
            st.session_state.score = 0
            st.session_state.round = 0
            st.session_state.current_q = generate_question("Speed")
            # prepare input key
            st.session_state["speed_answer_value"] = ""
            st.experimental_rerun()
        else:
            st.info("กด 'เริ่มโหมดเร็ว' เพื่อเริ่มจับเวลา")
            st.markdown("</div>", unsafe_allow_html=True)
            st.stop()

    # remaining time
    elapsed = time.time() - st.session_state.speed_start
    remain = max(0, int(time_limit - elapsed))
    st.markdown(f"### ⏳ เวลาที่เหลือ: **{remain} วินาที**")

    if remain <= 0:
        st.warning(f"หมดเวลา! คะแนนรวม: {st.session_state.score}")
        # offer save
        name = st.text_input("ชื่อที่ต้องการบันทึก:", key="save_name")
        if st.button("บันทึกคะแนน"):
            if name.strip():
                row = {"name": name.strip(), "score": st.session_state.score, "mode": "Speed"}
                # append to CSV
                if os.path.exists("leaderboard.csv"):
                    df = pd.read_csv("leaderboard.csv")
                    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
                else:
                    df = pd.DataFrame([row])
                df.to_csv("leaderboard.csv", index=False)
                st.success("บันทึกคะแนนเรียบร้อย 🎉")
                # reset
                st.session_state.speed_start = None
            else:
                st.warning("กรุณากรอกชื่อก่อนบันทึก")
        st.markdown("</div>", unsafe_allow_html=True)
        st.stop()

    # show question
    q = st.session_state.current_q
    st.markdown(f"<div style='text-align:center; margin: 8px 0;'><h2 style='color:#bffeff'>{q['a']} {q['op']} {q['b']} = ?</h2></div>", unsafe_allow_html=True)

    # one persistent key
    ans = st.text_input("ตอบที่นี่แล้วกด 'ส่ง'", key="speed_answer")
    if st.button("ส่งคำตอบ (เร็ว)", key="submit_speed"):
        if ans.strip().lstrip("-").isdigit():
            user_ans = int(ans)
            if user_ans == q["correct"]:
                st.session_state.score += 1
                st.session_state.last_result = "correct"
            else:
                st.session_state.last_result = "wrong"
            # new question immediately
            st.session_state.current_q = generate_question("Speed")
            # clear the input box by setting to empty string in session_state
            st.session_state["speed_answer"] = ""
            st.session_state.round += 1
            st.experimental_rerun()
        else:
            st.warning("กรุณากรอกตัวเลข")

    # instant feedback
    if st.session_state.last_result == "correct":
        st.markdown("<div class='big-emoji'>🎉</div>", unsafe_allow_html=True)
    elif st.session_state.last_result == "wrong":
        st.markdown("<div class='big-emoji'>❌</div>", unsafe_allow_html=True)

    st.markdown(f"<div class='side-note'>ตอบถูก: {st.session_state.score} | รอบ: {st.session_state.round}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# Leaderboard Page
# -------------------------
elif page == "Leaderboard":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#bffeff'>🏆 Leaderboard</h3>", unsafe_allow_html=True)

    if os.path.exists("leaderboard.csv"):
        df = pd.read_csv("leaderboard.csv")
        df = df.sort_values(by="score", ascending=False).reset_index(drop=True)
        # show top 20
        for i, row in df.head(20).iterrows():
            st.markdown(f"<div class='leader-row'><b>#{i+1}</b> {row['name']} — {int(row['score'])} pts ({row.get('mode','')})</div>", unsafe_allow_html=True)
    else:
        st.info("ยังไม่มีคะแนนในระบบ — เล่นแล้วบันทึกคะแนนเพื่อขึ้นหน้า Leaderboard")

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# Settings (optional)
# -------------------------
if page == "Settings":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("Settings coming soon...")
    st.markdown("</div>", unsafe_allow_html=True)
