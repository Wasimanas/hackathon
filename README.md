# UPSC Answer Validator 🎓

A premium Streamlit application to validate UPSC answers using Groq's Llama 3 API.

## Features
- **PDF Upload**: Upload your handwritten or typed answer sheets in PDF format.
- **AI-Powered Evaluation**: Get detailed feedback based on UPSC standards using Groq (Llama-3.3-70b).
- **Scorecard**: Visual breakdown of marks in different dimensions.
- **Recommendations**: Actionable advice to improve your answer writing.
- **Model Answer Outline**: See what a high-scoring answer looks like.

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Up Groq API Key**:
   - The application expects a `GROQ_API` key in your `.env` file:
     ```env
     GROQ_API=your_groq_api_key_here
     ```

3. **Run the Application**:
   ```bash
   streamlit run UPSC.py
   ```

## Technology Stack
- **Streamlit**: For the web interface.
- **Groq (Llama 3.3 70b)**: For lightning-fast answer evaluation.
- **PyMuPDF**: For robust PDF text extraction.
- **Vanilla CSS**: For custom, premium UI styling.
