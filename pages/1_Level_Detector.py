import streamlit as st
import json
import os

# Set page configuration
st.set_page_config(
    page_title="Level Detector",
    page_icon="🔍",
    layout="wide"
)

def load_questions():
    with open('questions.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def run_detector():
    st.title("🔍 Arabic Level Detector")
    st.write("Answer the following questions to find your perfect starting point.")
    
    questions = load_questions()
    
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 0
    if 'answers' not in st.session_state:
        st.session_state.answers = []
    if 'test_complete' not in st.session_state:
        st.session_state.test_complete = False

    # Flatten questions for easier iteration: 2 beginner, 2 intermediate, 2 advanced
    all_qs = questions['beginner'] + questions['intermediate'] + questions['advanced']
    
    if not st.session_state.test_complete:
        if st.session_state.current_step < len(all_qs):
            q = all_qs[st.session_state.current_step]
            
            st.write(f"### Question {st.session_state.current_step + 1} of {len(all_qs)}")
            st.info(q['question'])
            
            # Show progress bar
            progress = st.session_state.current_step / len(all_qs)
            st.progress(progress)
            
            with st.form(key=f"q_form_{st.session_state.current_step}"):
                choice = st.radio("Choose the correct answer:", q['options'], key=f"radio_{st.session_state.current_step}")
                submit = st.form_submit_button("Next Question →")
                
                if submit:
                    if choice == q['answer']:
                        st.session_state.score += 1
                    st.session_state.current_step += 1
                    st.rerun()
        else:
            st.session_state.test_complete = True
            st.rerun()
            
    else:
        # Results logic
        score = st.session_state.score
        level = ""
        desc = ""
        color = ""
        
        if score <= 2:
            level = "Beginner (مبتدئ)"
            desc = "You are just starting your Arabic journey! We'll begin with the basics like the alphabet and core greetings."
            color = "#1e3c72"
        elif score <= 4:
            level = "Intermediate (متوسط)"
            desc = "You have a good grasp of the basics. We'll focus on sentence structure and practical conversations."
            color = "#f39c12"
        else:
            level = "Advanced (متقدم)"
            desc = "Impressive! You understand complex Arabic. Let's delve into literature, poetry, and advanced linguistics."
            color = "#27ae60"
            
        # Save result to JSON (only once per complete)
        if not st.session_state.get('result_saved', False):
            user_result = {
                "score": score,
                "level": level,
                "timestamp": str(st.session_state.get('start_time', 'unknown'))
            }
            
            if not os.path.exists('user_results.json'):
                with open('user_results.json', 'w') as f:
                    json.dump([], f)
            
            with open('user_results.json', 'r+') as f:
                data = json.load(f)
                data.append(user_result)
                f.seek(0)
                json.dump(data, f, indent=2)
            
            st.session_state.result_saved = True

        st.success(f"### Your Level: {level}")
        st.write(f"**Score:** {score} / {len(all_qs)}")
        st.info(desc)
        
        st.write("##")
        if st.button("🔄 Retake Test"):
            st.session_state.score = 0
            st.session_state.current_step = 0
            st.session_state.test_complete = False
            st.session_state.result_saved = False
            st.rerun()
            
        if st.button("🏠 Go back to Home"):
            st.switch_page("Hackathon.py")

if __name__ == "__main__":
    run_detector()
