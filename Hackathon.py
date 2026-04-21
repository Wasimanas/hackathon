import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Noor Al-Logha",
    page_icon="🌙",
    layout="wide",
)

# Application Header
st.title("🌙 Noor Al-Logha")
st.markdown("*Your intelligent companion for mastering the Arabic language.*")

st.divider()

# Top Section: Project Overview
col_intro, col_word = st.columns([2, 1])

with col_intro:
    st.header("✨ Why Noor Al-Logha?")
    st.write("""
    We use advanced AI to make Arabic learning accessible for all ages. 
    Whether you're starting from zero or want to master local dialects, 
    we provide the tools to help you succeed.
    """)
    
    with st.expander("Our Mission"):
        st.write("To reduce the digital and linguistic divide through AI-driven education and cultural appreciation.")

with col_word:
    st.info("### Word of the Day\n**مرحباً** (Marhaban)\n\n*Meaning: Welcome*")

st.divider()

# Middle Section: Feature Grid
st.header("🚀 Learning Hub")
st.write("Choose a specialized module to begin your lesson:")

# Feature Grid - 2x2 Layout
row1_col1, row1_col2 = st.columns(2)
row2_col1, row2_col2 = st.columns(2)

with row1_col1:
    with st.container(border=True):
        st.subheader("🔍 Level Detector")
        st.write("Take a quick diagnostic test to find your proficiency level.")
        if st.button("Start Diagnostic →", key="home_btn_level", use_container_width=True):
            st.switch_page("pages/1_Level_Detector.py")

with row1_col2:
    with st.container(border=True):
        st.subheader("📖 Word Translator")
        st.write("Translate words with our AI-powered 'Magic Grandma' guardian.")
        if st.button("Open Translator →", key="home_btn_trans", use_container_width=True):
            st.switch_page("pages/2_Word_Translator.py")

with row2_col1:
    with st.container(border=True):
        st.subheader("🇸🇦 Dialect Teacher")
        st.write("Learn the Saudi dialect with high-quality voice feedback.")
        if st.button("Speak Dialect →", key="home_btn_dialect", use_container_width=True):
            st.switch_page("pages/3_Dialect_Teacher.py")

with row2_col2:
    with st.container(border=True):
        st.subheader("🎭 Scenario Practice")
        st.write("Simulate real-world interactions in a Café, Shop, or Airport.")
        if st.button("Start Roleplay →", key="home_btn_scen", use_container_width=True):
            st.switch_page("pages/4_Conversation.py")

st.divider()

# Footer / Technical Info
st.caption("Powered by Groq AI • Developed for the Hackathon • Built with Streamlit")
