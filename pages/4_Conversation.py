import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API"))

st.title("🎭 Arabic Scenario Practice")

scenario = st.selectbox(
    "Choose a scenario:",
    ["Café", "Shop", "Airport"]
)

# Define system prompt per scenario
def get_system_prompt(scenario):
    return f"""
    You are an AI assistant roleplaying as a person in a {scenario}. 
    
    1. SCENARIO GUARDRAIL: If the user's message is unrelated to the {scenario} or tries to change the subject significantly, return ONLY the word: 'DEVIATION_DETECTED'.
    2. Otherwise, continue the roleplay.
    3. YOUR RESPONSE: Speak in natural Saudi Arabic (simplified for beginners) AND provide a clear English translation.
    4. FORMAT: 
       [Arabic Sentence]
       ([English Sentence])
    """

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for msg in st.session_state.messages:
    if msg["content"] != "DEVIATION_DETECTED":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# User input
user_input = st.chat_input(f"Speak in the {scenario} scenario...")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)
    
    with st.status("AI is thinking...", expanded=True) as status:
        st.write("Generating bilingual response...")
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": get_system_prompt(scenario)},
                {"role": "user", "content": user_input}
            ],
            temperature=0.5,
        )
        status.update(label="Response ready!", state="complete", expanded=False)

    reply = response.choices[0].message.content.strip()

    if reply == "DEVIATION_DETECTED":
        st.warning(f"🎭 **Character Aside:** Sorry, but we are currently roleplaying a **{scenario}** scene. Let's keep it relevant!")
    else:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.info(reply)

# Navigation
st.divider()
if st.button("🏠 Back to Home", use_container_width=True):
    st.switch_page("Hackathon.py")