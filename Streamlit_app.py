import streamlit as st, random, time, pandas as pd, os

st.set_page_config(page_title="Neon Math Rush", layout="centered", page_icon="🧮")

# -------------------------
# CSS Neon
st.markdown("""
<style>
body{background:radial-gradient(circle,#0f0f1c,#050510);color:#e7faff;font-family:sans-serif;}
.title{font-size:46px;text-align:center;color:#00eaff;text-shadow:0 0 8px #00eaff,0 0 16px #00eaff;}
.card{background:rgba(255,255,255,0.03);border:2px solid rgba(0,255,255,0.25);padding:20px;border-radius:20px;margin-top:15px;}
.big-emoji{font-size:110px;text-align:center;}
input[type="text"]{background:rgba(0,255,255,0.05);border:2px solid rgba(0,255,255,0.3);border-radius:10px;padding:10px;color:#e7fff9;font-size:18px;}
.question-box{font-size:42px;text-align:center;color:#affbff;margin:20px 0;}
.leader-row{padding:10px;border-bottom:1px solid rgba(255,255,255,0.05);}
</style>
""",unsafe_allow_html=True)

# -------------------------
# Session State Init
keys=["score","round","current_q","last_result","speed_start","speed_answer","play_answer","game_mode","speed_name","combo"]
for k in keys:
    if k not in st.session_state:
        st.session_state[k] = 0 if k in ["score","round","combo"] else None if k in ["current_q","speed_start"] else ""

# -------------------------
# Helper Functions
def gen_q(mode):
    a,b = random.randint(1,10), random.randint(1,10)
    if mode=="Medium": a,b=random.randint(5,20),random.randint(1,15); op=random.choice(["+","-","×"])
    elif mode=="Hard": a,b=random.randint(10,80),random.randint(5,30); op=random.choice(["+","-","×","÷"])
    elif mode=="Speed": a,b=random.randint(1,15),random.randint(1,15); op=random.choice(["+","-","×"])
    else: op=random.choice(["+","-"])
    if op=="÷": b=random.randint(1,12); a=b*random.randint(1,10)
    correct = a+b if op=="+" else a-b if op=="-" else a*b if op=="×" else a//b
    return {"a":a,"b":b,"op":op,"correct":correct}

def check_ans(ans,q):
    if ans.strip().lstrip("-").isdigit(): return int(ans)==q["correct"]
    return None

def show_emoji(result,combo=0):
    if result=="correct": st.markdown(f"<div class='big-emoji'>🎉{'🔥'*combo}</div>",unsafe_allow_html=True)
    elif result=="wrong": st.markdown("<div class='big-emoji'>❌</div>",unsafe_allow_html=True)

# -------------------------
# Sidebar
st.sidebar.title("📱 Menu")
page = st.sidebar.radio("", ["Home","Play","Speed Mode","Leaderboard"])
st.markdown("<h1 class='title'>NEON MATH RUSH</h1>",unsafe_allow_html=True)

# -------------------------
if page=="Home":
    st.markdown("<div class='card'>",unsafe_allow_html=True)
    st.markdown("### 🎮 วิธีเล่น")
    st.markdown("- เลือก Play หรือ Speed Mode")
    st.markdown("- Hard Mode: ตัวเลขใหญ่+ผสม + - × ÷")
    st.markdown("- Speed Combo: ตอบต่อเนื่องได้ Combo Multiplier")
    st.markdown("</div>",unsafe_allow_html=True)

# -------------------------
elif page=="Play":
    st.markdown("<div class='card'>",unsafe_allow_html=True)
    mode = st.selectbox("ระดับความยาก", ["Easy","Medium","Hard"], index=["Easy","Medium","Hard"].index(st.session_state.game_mode))
    st.session_state.game_mode = mode
    if st.session_state.current_q is None: st.session_state.current_q = gen_q(mode)
    q = st.session_state.current_q
    st.markdown(f"<div class='question-box'>{q['a']} {q['op']} {q['b']} = ?</div>",unsafe_allow_html=True)
    ans = st.text_input("คำตอบ:", key="play_answer")
    
    if st.button("ส่ง"):
        res = check_ans(ans,q)
        if res is not None:
            if res:
                st.session_state.score += 1 + st.session_state.combo
                st.session_state.last_result = "correct"
                st.session_state.combo += 1
            else:
                st.session_state.last_result = "wrong"
                st.session_state.combo = 0
            st.session_state.current_q = gen_q(mode)
            st.session_state.round += 1
            st.session_state.play_answer = ""
            st.experimental_rerun()
        else: st.warning("กรุณากรอกตัวเลข")
    
    show_emoji(st.session_state.last_result, st.session_state.combo)
    st.markdown(f"รอบ:{st.session_state.round} | คะแนน:{st.session_state.score} | Combo:{st.session_state.combo}")

# -------------------------
elif page=="Speed Mode":
    time_limit = st.slider("เวลา (วินาที)",10,60,20,5)
    if st.session_state.current_q is None: st.session_state.current_q = gen_q("Speed")
    if st.session_state.speed_start is None:
        if st.button("เริ่ม ▶"):
            st.session_state.speed_start = time.time()
            st.session_state.score = 0
            st.session_state.round = 0
            st.session_state.combo = 0
            st.session_state.current_q = gen_q("Speed")
            st.session_state.speed_answer = ""
            st.experimental_rerun()
        else: st.info("กดเริ่มเพื่อจับเวลา"); st.stop()
    elapsed = time.time() - st.session_state.speed_start
    remain = max(0,int(time_limit - elapsed))
    st.markdown(f"⏳ เวลาที่เหลือ: **{remain} วินาที**")
    
    if remain <= 0:
        st.warning(f"หมดเวลา! คะแนน:{st.session_state.score}")
        name = st.text_input("ชื่อ:", key="speed_name")
        if st.button("บันทึก"):
            if name.strip():
                row = {"name":name.strip(), "score":st.session_state.score, "mode":"Speed"}
                df = pd.read_csv("leaderboard.csv") if os.path.exists("leaderboard.csv") else pd.DataFrame()
                df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
                df.to_csv("leaderboard.csv", index=False)
                st.success("บันทึกคะแนน 🎉")
                st.session_state.speed_start = None
                st.session_state.current_q = None
                st.session_state.combo = 0
            else: st.warning("กรุณากรอกชื่อ")
        st.stop()
    
    q = st.session_state.current_q
    st.markdown(f"<div class='question-box'>{q['a']} {q['op']} {q['b']} = ?</div>",unsafe_allow_html=True)
    ans = st.text_input("ตอบที่นี่:", key="speed_answer")
    
    if st.button("ส่ง (เร็ว)"):
        res = check_ans(ans,q)
        if res is not None:
            if res:
                st.session_state.score += 1 + st.session_state.combo
                st.session_state.last_result = "correct"
                st.session_state.combo += 1
            else:
                st.session_state.last_result = "wrong"
                st.session_state.combo = 0
            st.session_state.current_q = gen_q("Speed")
            st.session_state.speed_answer = ""
            st.session_state.round += 1
            st.experimental_rerun()
        else: st.warning("กรุณากรอกตัวเลข")
    
    show_emoji(st.session_state.last_result, st.session_state.combo)
    st.markdown(f"ตอบถูก:{st.session_state.score} | รอบ:{st.session_state.round} | Combo:{st.session_state.combo}")

# -------------------------
elif page=="Leaderboard":
    st.markdown("<div class='card'>",unsafe_allow_html=True)
    st.markdown("<h3>🏆 Leaderboard</h3>",unsafe_allow_html=True)
    if os.path.exists("leaderboard.csv"):
        df = pd.read_csv("leaderboard.csv").sort_values("score", ascending=False).reset_index(drop=True)
        for i,row in df.head(20).iterrows():
            st.markdown(f"<div class='leader-row'>#{i+1} {row['name']} — {int(row['score'])} pts ({row.get('mode','')})</div>",unsafe_allow_html=True)
    else: st.info("ยังไม่มีคะแนน")
    st.markdown("</div>",unsafe_allow_html=True)
