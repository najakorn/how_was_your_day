import streamlit as st
import random
import requests
from datetime import date


def send_telegram_message(message):
    bot_token = st.secrets["telegram"]["bot_token"]
    chat_id = st.secrets["telegram"]["chat_id"]
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            st.success("Message sent to my Telegram! 💌")
        else:
            st.warning(f"Failed to send message. Error: {response.text}")
    except Exception as e:
        st.error(f"Telegram message failed: {e}")

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

reward_gifs = [
    {
        "gif": "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExMXIybmhzdXJ2YjM5MjVhMXAwa2JpcHNycW9iajdrejloMTc4NTVycyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/EbaEWv3icphQI/giphy.gif",
        "caption": "You’ve made it another 5 days in a row, baobeir!"
    },
    {
        "gif": "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExcjhnaTJjOGdpZ21mOXpnajd3cHpueHNyNHVwZHl0eTR5aHExbDk5eiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/DorxfW5xBGSG8bVxRa/giphy.gif",
        "caption": "That’s 5 more days of cuteness. Virtual hug loading..."
    },
    {
        "gif": "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDFkc3N3anBkM29ocW5hYXV2ODVhMmxxeDg4dnVzOHd5ODdmb2h3byZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/T0ph30SEe8W15fLHIU/giphy.gif",
        "caption": "OMG 5 more days?? You’re on a roll and I’m OBSESSED"
    },
    {
        "gif": "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExcm9paWdhYmg3dzg3NGd1emYzZTB5cXlhYmk3ems4ODN1dzlnNHFkNyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Bv76prPEWdr4nxovaK/giphy.gif",
        "caption": "Another 5-day streak! You’ve earned the right to kiss me and play with me like this!"
    },
    {
        "gif": "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExZXp1dWNhc3dvMG80enJmdXB6Ymo4ejBtYWxrcWV3NGtmOTRiamU1eiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/H4uE6w9G1uK4M/giphy.gif",
        "caption": "Another 5-day streak! Wait for meee!! I’m waddling as fast as I can to come kiss you!"
    },
    
]

genie_note = st.text_area("Tell me about it:", placeholder="")

# Initialize streak tracking
if "last_checkin" not in st.session_state:
    st.session_state.last_checkin = None
    st.session_state.streak = 0

# Submit button logic
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

    if st.session_state.last_checkin != today:
        if st.session_state.last_checkin == today.fromordinal(today.toordinal() - 1):
            st.session_state.streak += 1
        else:
            st.session_state.streak = 1
        st.session_state.last_checkin = today

    final_message = genie_note.strip() if genie_note.strip() else random.choice(messages[score])

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

    # Send to Telegram
    telegram_msg = f"""✨ Genie Check-In ✨
Mood: {score} - {mood_label}
Message: {final_message}"""
    send_telegram_message(telegram_msg)

    if score == 5:
        st.balloons()

    if st.session_state.streak % 5 == 0 and st.session_state.streak > 0:
        reward = random.choice(reward_gifs)
        st.balloons()
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
