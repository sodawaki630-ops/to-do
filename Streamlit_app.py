import streamlit as st
import pandas as pd
import os

st.title("🏆 Leaderboard")

if os.path.exists("leaderboard.csv"):
    df = pd.read_csv("leaderboard.csv")
    df = df.sort_values("score", ascending=False)
    st.dataframe(df)
else:
    st.info("ยังไม่มีคะแนนถูกบันทึก")
