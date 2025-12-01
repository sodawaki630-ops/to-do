elif page=="Speed Mode":
    time_limit = st.slider("เวลา (วินาที)",10,60,20,5)

    # Init session_state keys
    if "speed_start" not in st.session_state: st.session_state.speed_start=None
    if "speed_answer" not in st.session_state: st.session_state.speed_answer=""
    if "current_q" not in st.session_state: st.session_state.current_q=None
    if st.session_state.current_q is None:
        st.session_state.current_q = generate_question("Speed")

    # Start button
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

    # Timer
    elapsed = time.time() - st.session_state.speed_start
    remain = max(0, int(time_limit - elapsed))
    st.markdown(f"⏳ เวลาที่เหลือ: **{remain} วินาที**")
    if remain <= 0:
        st.warning(f"หมดเวลา! คะแนนรวม: {st.session_state.score}")
        name = st.text_input("ชื่อสำหรับบันทึก:", key="speed_name")
        if st.button("บันทึกคะแนน"):
            if name.strip():
                row={"name":name.strip(),"score":st.session_state.score,"mode":"Speed"}
                if os.path.exists("leaderboard.csv"):
                    df=pd.read_csv("leaderboard.csv")
                    df=pd.concat([df,pd.DataFrame([row])],ignore_index=True)
                else:
                    df=pd.DataFrame([row])
                df.to_csv("leaderboard.csv",index=False)
                st.success("บันทึกคะแนนเรียบร้อย 🎉")
                st.session_state.speed_start = None
                st.session_state.current_q = None
            else:
                st.warning("กรุณากรอกชื่อก่อนบันทึก")
        st.stop()

    # Question
    q = st.session_state.current_q
    st.markdown(f"<div class='question-box'>{q['a']} {q['op']} {q['b']} = ?</div>", unsafe_allow_html=True)

    # Input & submit
    ans = st.text_input("ตอบที่นี่:", key="speed_answer")
    if st.button("ส่งคำตอบ (เร็ว)"):
        if ans.strip().lstrip("-").isdigit():
            ans = int(ans)
            if ans == q["correct"]:
                st.session_state.score +=1
                st.session_state.last_result="correct"
            else:
                st.session_state.last_result="wrong"
            st.session_state.current_q = generate_question("Speed")  # new question
            st.session_state.speed_answer = ""  # clear input
            st.session_state.round +=1
            st.experimental_rerun()
        else:
            st.warning("กรุณากรอกตัวเลข")

    # Feedback
    if st.session_state.last_result=="correct": st.markdown("<div class='big-emoji'>🎉</div>", unsafe_allow_html=True)
    elif st.session_state.last_result=="wrong": st.markdown("<div class='big-emoji'>❌</div>", unsafe_allow_html=True)
    st.markdown(f"ตอบถูก: {st.session_state.score} | รอบ: {st.session_state.round}")
