import streamlit as st
import random
import requests
from datetime import date
from utils import send_telegram_message, update_streak
from gif import reward_gifs

st.set_page_config(page_title="How was your day?", page_icon="🌈")
st.title("Heeelllloooo... how was your day, baobeir?")

score = st.radio(
    " ",
    options=[1, 2, 3, 4, 5],
    format_func=lambda x: {
        1: "🥲 Rough",
        2: "😔 Meh",
        3: "😌 Okay",
        4: "😊 Good",
        5: "🥳 Amazing!"
    }[x],
    horizontal=True
)

genie_note = st.text_area("Tell me about it:", placeholder="")

if "last_checkin" not in st.session_state:
    st.session_state.last_checkin = None
    st.session_state.streak = 0

if st.button("Submit"):
    mood_label = {
        1: "🥲 Rough",
        2: "😔 Meh",
        3: "😌 Okay",
        4: "😊 Good",
        5: "🥳 Amazing!"
    }[score]

    messages = {
        1: "Mood booster loading… 98%… 99%… okay, now imagine me hugging you. Got it?",
        2: "Bit meh? I'd make you laugh, let's get on the phone 😌📲",
        3: "Bet it would've been better with me 😉",
        4: "You glowing from afar and I felt it ☀️",
        5: "WOOHOO! Well done! You better be doing a happy dance. I am, for you 🥳"
    }

    today = date.today()
    update_streak(today)
    
    final_message = genie_note.strip()

    st.markdown(
    f"""
    <div style="
        background-color: #f0f4ff;
        padding: 16px 20px;
        margin-top: 20px;
        border-radius: 20px;
        border: 2px solid #a6c8ff;
        font-size: 15px;
        font-weight: 500;
        color: #333;
        text-align: center;
        max-width: 80%;
        margin-left: auto;
        margin-right: auto;
    ">
        {messages[score]}
    </div>
    """,
    unsafe_allow_html=True)
    st.markdown("")


    telegram_msg = f"""✨ Genie Check-In ✨
Mood: {score} - {mood_label}
Message: {final_message}"""
    send_telegram_message(telegram_msg)

    if score == 5:
        st.balloons()

    # if st.button("💌 New message for you"):
    #     st.markdown("")
    
    if st.session_state.streak % 3 == 0 and st.session_state.streak > 0:
        reward = random.choice(reward_gifs)
        st.markdown(
    f"""
    <div style="
        background: #fef3f8;
        border-radius: 16px;
        padding: 15px 20px;
        margin-top: 15px;
        text-align: center;
        font-size: 15px;
        font-weight: 500;
        color: #5c2a4a;
        box-shadow: 0 0 12px rgba(255, 182, 193, 0.6);
    ">
        {reward["caption"]}
    </div>
    """,
    unsafe_allow_html=True
)
        st.image(reward["gif"], use_container_width=True)
