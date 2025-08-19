import requests
from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()

DISCORD_WEBHOOK_URL = None

# Prefer Streamlit secrets if available, fallback to env var
try:
    if hasattr(st, "secrets") and "DISCORD_WEBHOOK_URL" in st.secrets:
        DISCORD_WEBHOOK_URL = st.secrets["DISCORD_WEBHOOK_URL"]
except Exception:
    # Accessing st.secrets can raise if not configured; ignore
    pass

if not DISCORD_WEBHOOK_URL:
    DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")


def send_discord_message(message: str, timeout: float = 2.0, silent: bool = True) -> bool:
    """
    Send a message to a Discord channel via webhook.

    Safety features:
    - No-op if webhook URL is missing or blank.
    - Short request timeout to avoid blocking Streamlit runs.
    - Swallows network errors by default (silent=True) to prevent UI crashes.

    Returns True if the message was sent (HTTP 2xx), else False.
    """
    url = (DISCORD_WEBHOOK_URL or "").strip()
    if not url:
        # Warn only once per session to avoid spam on reruns
        key = "_discord_webhook_warned"
        if not silent and not st.session_state.get(key, False):
            st.info("Discord webhook not configured. Set DISCORD_WEBHOOK_URL in .env or st.secrets.")
            st.session_state[key] = True
        return False

    try:
        data = {"content": message}
        resp = requests.post(url, json=data, timeout=timeout)
        return 200 <= resp.status_code < 300
    except Exception as e:
        if not silent:
            st.warning(f"Discord notification failed: {e}")
        return False