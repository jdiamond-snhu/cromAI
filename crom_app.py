import base64
import json
import os
import random
import re
import time
import streamlit as st

# 1. Page Configuration
st.set_page_config(page_title="CROM", page_icon="⚔️", layout="wide")


# 2. Helper Function to Set Background Image (Full Brightness)
def set_background(image_path):
  if os.path.exists(image_path):
    with open(image_path, "rb") as img_file:
      encoded = base64.b64encode(img_file.read()).decode()
    bg_css = f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            color: #f0ece1;
        }}
        [data-testid="stSidebar"] {{
            background-color: rgba(20, 20, 24, 0.92);
            border-right: 1px solid #3d3d45;
        }}
        [data-testid="stChatMessage"] {{
            background-color: rgba(30, 30, 36, 0.88);
            border: 1px solid #444;
            border-radius: 8px;
            padding: 12px;
        }}
        </style>
        """
    st.markdown(bg_css, unsafe_allow_html=True)


set_background("bg.jpg")


# 3. Load CROM's Brain
def load_brain():
  with open("crom_brain.json", "r", encoding="utf-8") as f:
    return json.load(f)


brain = load_brain()
RULES = [(item["pattern"], item["responses"]) for item in brain["rules"]]
FALLBACKS = brain["fallbacks"]

# 4. Sidebar Lore & Reset Button
with st.sidebar:
  st.header("⛰️ THE MOUNTAIN")
  st.markdown(
      "*Crom sits upon his dark mountain, brooding over the riddle of steel.*"
  )
  st.divider()

  if st.button("⚡ SMITE CHAT HISTORY", use_container_width=True):
    st.session_state.messages = [{
        "role": "assistant",
        "content": (
            "THE PAST IS ASHES. SPEAK AGAIN, MORTAL, BEFORE I LOSE PATIENCE."
        ),
    }]
    st.rerun()


# 5. CROM's Response Engine (Always Hostile)
def crom_respond(user_input):
  cleaned_input = user_input.lower().strip()

  # Special check: Catch what the user wants and mock it 65% of the time
  desire_match = re.search(
      r"\b(?:how can i get|can i get|i want|give me|how do i get)\s+(.+)",
      cleaned_input,
  )
  if desire_match and random.random() < 0.65:
    desired_thing = re.sub(r"[?.!]+$", "", desire_match.group(1)).upper()
    return (
        f"'{desired_thing}'?! YOU HAVE TWO HANDS AND LEGS. GO TAKE IT YOURSELF!"
    )

  # Check JSON rules
  for pattern, responses in RULES:
    if re.search(pattern, cleaned_input):
      return random.choice(responses)

  # Mock short unrecognized inputs 65% of the time
  words = cleaned_input.split()
  if len(words) <= 4 and random.random() < 0.65:
    return f"'{cleaned_input.upper()}'? YOU SOUND LIKE A WEAKLING."

  return random.choice(FALLBACKS)


# 6. Main Display Area (Header + Top Input Box)
st.title("⚔️ CROM")
st.caption("DO NOT PRAY. DO NOT WHINE. SPEAK.")

if "messages" not in st.session_state:
  st.session_state.messages = [{
      "role": "assistant",
      "content": "CROM SITS UPON HIS MOUNTAIN. SPEAK, WEAKLING.",
  }]

with st.form(key="crom_input_form", clear_on_submit=True):
  col1, col2 = st.columns([5, 1])
  with col1:
    prompt = st.text_input(
        "Speak",
        placeholder="Offer your words to the mountain...",
        label_visibility="collapsed",
    )
  with col2:
    submitted = st.form_submit_button("SPEAK ⚔️", use_container_width=True)

# 7. Process Input & Display Chat Feed (Newest at the Top)
if submitted and prompt.strip():
  st.session_state.messages.append({"role": "user", "content": prompt})
  with st.spinner("*THUNDER RUMBLES...*"):
    time.sleep(0.5)
  response = crom_respond(prompt)
  st.session_state.messages.append({"role": "assistant", "content": response})

st.divider()

for message in reversed(st.session_state.messages):
  avatar = "⚔️" if message["role"] == "assistant" else "🦴"
  with st.chat_message(message["role"], avatar=avatar):
    st.markdown(message["content"])
