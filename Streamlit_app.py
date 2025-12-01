# app.py
import streamlit as st
import random, time, pandas as pd, os

# -------------------------
# Page config
# -------------------------
st.set_page_config(page_title="Neon Math Rush", layout="centered", page_icon="🧮")

# -------------------------
# Neon CSS
# -------------------------
NEON_CSS = """
<style>
body { background: radial-gradient(circle at top, #0f0f1c 0%, #050510 70%); color:#e7faff; font-family:'Trebuchet MS',sans-serif; }
.title { font-size:46px; text-align:center; color:#00eaff; margin:10px 0; text-shadow:0 0 8px #00eaff,0 0 16px #00eaff,0 0 32px #00eaff; animation: glowPulse 2s infinite ease-in-out; }
@keyframes glowPulse { 0% {text-shadow:0 0 8px #00eaff;} 50% {text-shadow:0 0 20px #00fff2,0 0 40px #00caff;} 100% {text-shadow:0 0 8px #00eaff;} }
.card { background: rgba(255,255,255,0.03); border:2px solid rgba(0,255,255,0.25); padding:20px; border-radius:20px; box-shadow:0 0 10px rgba(0,255,255,0.2), inset 0 0 20px rgba(0,255,255,0.06); backdrop-filter: blur(6px); margin-top:15px; }
.big-emoji { font-size:110px; text-align:center; animation: pop 0.35s ease-out; }
@keyframes pop { 0% {transform:scale(0.3); opacity:0;} 80% {transform:scale(1.1); opacity:1;} 100% {transform:scale(1);} }
input[type="text"] { background: rgba(0,255,255,0.05); border:2px solid rgba(0,255,255,0.3); border-radius:10px; padding:10px; color:#e7fff9; font-size:18px; box-shadow: inset 0 0 10px rgba(0,255,255,0.15);}
input[type="text"]:focus { outline:none !important; border:2px solid #00eaff; box-shadow:0 0 10px #00eaff,0 0 20px #00eaff; }
.question-box { font-size:42px; text-align:center; color:#affbff; margin:20px 0; text-shadow:0 0 8px #00faff,0 0 16px #00d8ff; }
.leader-row { padding:10px; border-bottom:1px solid rgba(255,255,255,0.05); font-size:18px; color:#b9faff; }
</style>
"""
st.markdown(NEON_CSS, unsafe_allow_html=True)

# -------------------------
# Session State Init
# -------------------------
keys = ["score","round","current_q","last_result","speed_start","speed_answer","game_mode","speed_name"]
for k in keys:
    if k not in st.session_state:
        st.session_state[k] = 0 if k in ["score","round"] else None if k in ["current_q","speed_start"] else "" if k in ["speed_answer","speed_name"] else "Easy"

# -------------------------
# Helper: generate question
# -------------------------
def generate_question(mode):
    if mode=="Easy": a,b,op=random.randint(1,10),random.randint(1,10),random.choice(["+","-"])
    elif mode=="Medium": a,b,op=random.randint(5,20),random.randint(1,15),random.choice(["+","-","×"])
    elif mode=="Hard": a,b,op=random.randint(10,80),random.randint(5,30),random.choice(["+","-","×","÷"])
    else: a,b,op=random.randint(1,15),random.randint(1,15),random.choice(["+","-","×"])
    if op=="÷": b=random.randint(1,12); a=b*random.randint(1,10)
    correct = a+b if op=="+" else a-b if op=="-" else a*b if op=="×" else a//b
    return {"a":a,"b":b,"op":op,"correct":correct}

# -------------------------
# Sidebar / Menu
# -------------------------
st.sidebar.title("📱 Menu")
page = st.sidebar.radio("", ["Home","Play","Speed Mode","Leaderboard"])
st.session_state.page = page

# -------------------------
# Home
# -------------------------
st.markdown("<h1 class='title'>NEON MATH RUSH</h1>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center; color:#8be9ff; margin-bottom:12px;'>คิดเร็ว ตอบไว สะสมคะแนน</div>", unsafe_allow_html=True)

if page=="Home":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 🎮 วิธีเล่นโดยย่อ")
    st.markdown("- เลือกเมนู `Play` หรือ `Speed Mode` จากแถบซ้าย")
    st.markdown("- ตอบคำถามให้ถูกเพื่อเพิ่มคะแนน")
    st.markdown("- ใน Speed Mode มีตัวจับเวลา ให้ตอบให้ได้มากที่สุด")
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# Play Mode
# -------------------------
elif page=="Play":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### เลือกระดับความยาก")
    mode = st.selectbox("", ["Easy","Medium","Hard"], index=["Easy","Medium","Hard"].index(st.session_state.game_mode))
    st.session_state.game_mode = mode

    if st.session_state.current_q is None:
        st.session_state.current_q = generate_question(mode)
    q = st.session_state.current_q

    st.markdown(f"<div class='question-box'>{q['a']} {q['op']} {q['b']} = ?</div>", unsafe_allow_html=True)
    user = st.text_input("คำตอบของคุณ:", key="play_answer")

    if st.button("ส่งคำตอบ"):
        if user.strip().lstrip("-").isdigit():
            ans = int(user)
            if ans==q["correct"]: st.session_state.score+=1; st.session_state.last_result="correct"
            else: st.session_state.last_result="wrong"
            st.session_state.current_q = generate_question(mode)
            st.session_state.round+=1
            st.session_state.play_answer=""
            st.experimental_rerun()
        else: st.warning("กรุณากรอกตัวเลข")

    if st.session_state.last_result=="correct": st.markdown("<div class='big-emoji'>🎉</div>", unsafe_allow_html=True)
    elif st.session_state.last_result=="wrong": st.markdown("<div class='big-emoji'>❌</div>", unsafe_allow_html=True)

    st.markdown(f"รอบ: {st.session_state.round} | คะแนน: {st.session_state.score}")

# -------------------------
# Speed Mode
# -------------------------
elif page=="Speed Mode":
    time_limit = st.slider("เวลา (วินาที)",10,60,20,5)
    if st.session_state.current_q is None:
        st.session_state.current_q = generate_question("Speed")

    if st.session_state.speed_start is None:
        if st.button("เริ่มโหมดเร็ว ▶"):
            st.session_state.speed_start = time.time()
            st.session_state.score = 0
            st.session_state.round = 0
            st.session_state.current_q = generate_question("Speed")
            st.session_state.speed_answer = ""
            st.experimental_rerun()
        else:
            st.info("กด 'เริ่มโหมดเร็ว' เพื่อเริ่มจับเวลา")
            st.stop()

    elapsed = time.time() - st.session_state.speed_start
    remain = max(0,int(time_limit-elapsed))
    st.markdown(f"⏳ เวลาที่เหลือ: **{remain} วินาที**")

    if remain<=0:
        st.warning(f"หมดเวลา! คะแนนรวม: {st.session_state.score}")
        name = st.text_input("ชื่อสำหรับบันทึก:", key="speed_name")
        if st.button("บันทึกคะแนน"):
            if name.strip():
                row = {"name":name.strip(),"score":st.session_state.score,"mode":"Speed"}
                if os.path.exists("leaderboard.csv"):
                    df=pd.read_csv("leaderboard.csv")
                    df=pd.concat([df,pd.DataFrame([row])],ignore_index=True)
                else: df=pd.DataFrame([row])
                df.to_csv("leaderboard.csv",index=False)
                st.success("บันทึกคะแนนเรียบร้อย 🎉")
                st.session_state.speed_start = None
                st.session_state.current_q = None
            else: st.warning("กรุณากรอกชื่อก่อนบันทึก")
        st.stop()

    q = st.session_state.current_q
    st.markdown(f"<div class='question-box'>{q['a']} {q['op']} {q['b']} = ?</div>", unsafe_allow_html=True)
    ans = st.text_input("ตอบที่นี่:", key="speed_answer")
    if st.button("ส่งคำตอบ (เร็ว)"):
        if ans.strip().lstrip("-").isdigit():
            ans=int(ans)
            if ans==q["correct"]: st.session_state.score+=1; st.session_state.last_result="correct"
            else: st.session_state.last_result="wrong"
            st.session_state.current_q=generate_question("Speed")
            st.session_state.speed_answer=""
            st.session_state.round+=1
            st.experimental_rerun()
        else: st.warning("กรุณากรอกตัวเลข")

    if st.session_state.last_result=="correct": st.markdown("<div class='big-emoji'>🎉</div>", unsafe_allow_html=True)
    elif st.session_state.last_result=="wrong": st.markdown("<div class='big-emoji'>❌</div>", unsafe_allow_html=True)
    st.markdown(f"ตอบถูก: {st.session_state.score} | รอบ: {st.session_state.round}")

# -------------------------
# Leaderboard
# -------------------------
elif page=="Leaderboard":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3>🏆 Leaderboard</h3>", unsafe_allow_html=True)
    if os.path.exists("leaderboard.csv"):
        df = pd.read_csv("leaderboard.csv").sort_values("score",ascending=False).reset_index(drop=True)
        for i,row in df.head(20).iterrows():
            st.markdown(f"<div class='leader-row'>#{i+1} {row['name']} — {int(row['score'])} pts ({row.get('mode','')})</div>", unsafe_allow_html=True)
    else:
        st.info("ยังไม่มีคะแนน")
    st.markdown("</div>", unsafe_allow_html=True)
