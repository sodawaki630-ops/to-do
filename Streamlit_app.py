ULTRA_NEON_CSS = """
<style>
/* ———————————— Global ———————————— */
body {
    background: radial-gradient(circle at top, #0f0f1c 0%, #050510 70%);
    color: #e7faff;
    font-family: 'Trebuchet MS', sans-serif;
}

/* ———————————— Title ———————————— */
.title {
    font-size: 46px;
    text-align: center;
    color: #00eaff;
    margin-top: 10px;
    margin-bottom: 5px;
    text-shadow: 
        0 0 8px #00eaff,
        0 0 16px #00eaff,
        0 0 32px #00eaff;
    animation: glowPulse 2s infinite ease-in-out;
}

@keyframes glowPulse {
    0%   { text-shadow: 0 0 8px #00eaff; }
    50%  { text-shadow: 0 0 20px #00fff2, 0 0 40px #00caff; }
    100% { text-shadow: 0 0 8px #00eaff; }
}

/* ———————————— Card / Frame ———————————— */
.card {
    background: rgba(255, 255, 255, 0.03);
    border: 2px solid rgba(0, 255, 255, 0.25);
    padding: 20px;
    border-radius: 20px;
    box-shadow:
        0 0 10px rgba(0, 255, 255, 0.2),
        inset 0 0 20px rgba(0, 255, 255, 0.06);
    backdrop-filter: blur(6px);
    margin-top: 15px;
}

/* ———————————— Big Emoji ———————————— */
.big-emoji {
    font-size: 110px;
    text-align: center;
    animation: pop 0.35s ease-out;
}

@keyframes pop {
    0% { transform: scale(0.3); opacity: 0; }
    80% { transform: scale(1.1); opacity: 1; }
    100% { transform: scale(1); }
}

/* ———————————— Neon Buttons ———————————— */
.btn-neon {
    width: 100%;
    padding: 14px;
    border-radius: 14px;
    border: 2px solid #00f6ff;
    background: rgba(0, 255, 255, 0.07);
    color: #b9faff;
    font-size: 18px;
    letter-spacing: 1px;
    transition: 0.25s;
}

.btn-neon:hover {
    background: #00eaff;
    color: #00141a;
    transform: translateY(-2px);
    box-shadow:
        0 0 8px #00eaff,
        0 0 16px #00eaff,
        0 0 30px #00d8ff;
}

/* ———————————— Input Neon ———————————— */
input[type="text"] {
    background: rgba(0, 255, 255, 0.05);
    border: 2px solid rgba(0, 255, 255, 0.3);
    border-radius: 10px;
    padding: 10px;
    color: #e7fff9;
    font-size: 18px;
    box-shadow: inset 0 0 10px rgba(0,255,255,0.15);
}

input[type="text"]:focus {
    outline: none !important;
    border: 2px solid #00eaff;
    box-shadow:
        0 0 10px #00eaff,
        0 0 20px #00eaff;
}

/* ———————————— Question Text ———————————— */
.question-box {
    font-size: 42px;
    text-align: center;
    color: #affbff;
    margin: 20px 0;
    text-shadow: 
        0 0 8px #00faff,
        0 0 16px #00d8ff;
}

/* ———————————— Sidebar ———————————— */
.css-1d391kg, .css-hxt7ib {
    background: rgba(0,0,0,0.25) !important;
    backdrop-filter: blur(10px) !important;
    border-right: 1px solid rgba(0,255,255,0.2);
}

/* ———————————— Leaderboard Row ———————————— */
.leader-row {
    padding: 10px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    font-size: 18px;
    color: #b9faff;
}
</style>
"""
