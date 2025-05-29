import streamlit as st
import requests
from datetime import timedelta

# def send_telegram_message(message):
#     bot_token = st.secrets["telegram"]["bot_token"]
#     chat_id = st.secrets["telegram"]["chat_id"]
#     url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
#     payload = {"chat_id": chat_id, "text": message}
#     try:
#         response = requests.post(url, data=payload)
#         if response.status_code == 200:
#             st.success("Message sent to my Telegram! 💌")
#         else:
#             st.warning(f"Failed to send message. Error: {response.text}")
#     except Exception as e:
#         st.error(f"Telegram message failed: {e}")

def send_telegram_message(message):
    try:
        bot_token = st.secrets["telegram"]["bot_token"]
        chat_id = st.secrets["telegram"]["chat_id"]
    except KeyError:
        st.warning("⚠️ Telegram secrets not found. Message not sent.")
        return

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


def update_streak(today):
    yesterday = today - timedelta(days=1)
    if st.session_state.last_checkin != today:
        if st.session_state.last_checkin == yesterday:
            st.session_state.streak += 1
        else:
            st.session_state.streak = 1
        st.session_state.last_checkin = today
