import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Word Translator",
    page_icon="📖",
    layout="wide"
)

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API"))

def translate_word(word):
    try:
        prompt = f"""
        You are a cheeky, witty, and slightly sassy Arabic teacher for seniors. 
        Translate the word '{word}' into its Arabic equivalent.
        
        RULES:
        1. If the word is foul, offensive, or inappropriate, DO NOT TRANSLATE IT.
        2. If it's inappropriate, respond with an EXTREMELY CHEEKY, witty, and funny message in English. 
           Be a bit sassy—give them a "naughty list" vibe or a "my ears are burning" comment. 
           Make it memorable and hilarious, like a grandma who's seen it all and isn't impressed.
        3. If it's a normal word, ONLY provide the Arabic translation and the transliteration in this format: [Arabic Word] ([Transliteration])
        """
        
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Oops! I got a bit confused: {str(e)}"

def main():
    st.title("📖 Magic Word Translator")
    st.write("Type any word in English, and I'll show you its beautiful Arabic counterpart!")
    
    # Input area
    with st.container():
        word_input = st.text_input("Enter a word:", placeholder="e.g. Peace, Family, Coffee...")
        
        if word_input:
            with st.spinner("Asking the elders..."):
                response = translate_word(word_input)
                
                # Simple logic to check if the response looks like a funny message or a translation
                # The prompt usually results in either the Arabic or the funny msg.
                if "(" in response and ")" in response and len(response.split()) < 10:
                    # Likely a translation
                    st.success(f"### {response}")
                    st.balloons()
                else:
                    # Likely a funny warning or safety msg
                    sassy_emojis = ["💅", "🙄", "👵🔥", "🤨", "🤐", "🤷‍♀️"]
                    import random
                    emoji = random.choice(sassy_emojis)
                    st.warning(f"{emoji} {response}")

    # Navigation
    st.write("##")
    if st.button("🏠 Back to Home"):
        st.switch_page("Hackathon.py")

if __name__ == "__main__":
    main()
