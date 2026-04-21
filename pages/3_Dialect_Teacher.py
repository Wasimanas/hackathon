import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq
from pathlib import Path
import tempfile

# Load env
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API"))

st.set_page_config(page_title="Arabic → Saudi Speech", page_icon="🇸🇦")
st.title("🇸🇦 Dialect Teacher: Saudi Arabic")
st.caption(
    "Enter a sentence in English or Arabic to hear it in the beautiful Saudi dialect."
)

user_input = st.text_area(
    "Enter sentence", placeholder="e.g. How are you today? or كيف حالك؟", height=120
)

# Voice Selection
gender = st.radio(
    "Select Voice Gender", ["Female (Noura)", "Male (Fahad)"], horizontal=True
)
selected_voice = "noura" if "Female" in gender else "fahad"


# Step 1: Convert to Saudi Arabic with Guardrail
def convert_to_saudi(text: str) -> str:
    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a literal translator for the Saudi Arabic dialect. "
                    "CRITICAL RULES:\n"
                    "1. ZERO CONVERSATION: Never answer a question. Simply translate the text provided. Example: If the user types 'What is your name?', you MUST return the Saudi translation 'وش اسمك؟'. Do NOT say 'My name is AI' or anything similar.\n"
                    "2. TRANSLATION ONLY: Your sole job is to convert the input (English or MSA) into Saudi dialect. If the input is a greeting or a question, translate it exactly as a question/greeting.\n"
                    "3. SAFETY FIRST: If the input text contains even a hint of foul language, insults, sexual content, "
                    "violence, or extreme disrespect, you MUST return ONLY the string 'GUARDRAIL_TRIGGERED'. No exceptions.\n"
                    "4. DIALECT AUTHENTICITY: Use local Saudi idioms and natural phrasing.\n"
                    "5. OUTPUT FORMAT: Return ONLY the resulting Saudi Arabic sentence. No explanations, no prefixes."
                ),
            },
            {"role": "user", "content": text},
        ],
        temperature=0.1,  # Lower temperature for more consistent dialect application
    )
    return res.choices[0].message.content.strip()


# Step 2: Text-to-Speech using Groq
def generate_speech(text: str, file_path: str, voice: str):
    response = client.audio.speech.create(
        model="canopylabs/orpheus-arabic-saudi",
        voice=voice,
        response_format="wav",
        input=text,
    )
    response.write_to_file(file_path)


if st.button("Convert + Speak 🎧"):
    if not user_input.strip():
        st.warning("Please enter some text first!")
    else:
        with st.spinner("Processing..."):
            saudi_text = convert_to_saudi(user_input)

        if saudi_text == "GUARDRAIL_TRIGGERED":
            st.error(
                "🙄 My dear, let's keep it polite! A wise speaker chooses kind words."
            )
            st.info(
                "Try asking something like 'How is the weather?' or 'Where is the coffee?'"
            )
        else:
            st.subheader("🇸🇦 Saudi Arabic Dialect")
            st.success(saudi_text)

            with st.spinner(f"Generating {gender} voice..."):
                # Use temp file
                with tempfile.NamedTemporaryFile(
                    delete=False, suffix=".wav"
                ) as tmp_file:
                    speech_path = tmp_file.name

                try:
                    generate_speech(saudi_text, speech_path, selected_voice)
                    st.subheader("🔊 Audio Output")
                    st.audio(speech_path, format="audio/wav")
                except Exception as e:
                    st.error(f"Audio generation failed: {e}")
                    st.info(
                        "I can provide the text, but the voice assistant is resting right now."
                    )
