import streamlit as st
import os
import google.generativeai as genai
from pypdf import PdfReader
from dotenv import load_dotenv

# Load local environment variables (if any)
load_dotenv()

# App Page Configurations
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom CSS for premium design (glassmorphic styling, modern typography, custom animations)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Plus+Jakarta+Sans:wght@300;400;500;700&display=swap');
    
    /* Theme overrides */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    
    /* Elegant gradients and headers */
    .title-gradient {
        background: linear-gradient(135deg, #FF6B6B 0%, #4D96FF 50%, #6BCB77 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3.2rem;
        margin-bottom: 0.5rem;
    }
    
    .subtitle-text {
        font-size: 1.1rem;
        color: #A0AEC0;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Premium card containers */
    .research-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        transition: all 0.3s ease;
    }
    
    .research-card:hover {
        border: 1px solid rgba(255, 255, 255, 0.15);
        box-shadow: 0 12px 40px 0 rgba(77, 150, 255, 0.15);
        transform: translateY(-2px);
    }
    
    /* Glassmorphic sidebar card */
    .sidebar-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 16px;
        margin-top: 15px;
    }
    
    /* Custom buttons */
    div.stButton > button {
        background: linear-gradient(135deg, #4D96FF 0%, #3B82F6 100%);
        color: white;
        border: none;
        padding: 10px 24px;
        font-weight: 600;
        border-radius: 8px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(77, 150, 255, 0.25);
        width: 100%;
    }
    
    div.stButton > button:hover {
        background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%);
        box-shadow: 0 6px 20px rgba(77, 150, 255, 0.4);
        transform: translateY(-1px);
        color: white;
    }
    
    /* Alerts and badges */
    .status-badge {
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
    }
    .status-success {
        background-color: rgba(76, 175, 80, 0.15);
        color: #4CAF50;
        border: 1px solid rgba(76, 175, 80, 0.3);
    }
    .status-warning {
        background-color: rgba(255, 152, 0, 0.15);
        color: #FF9800;
        border: 1px solid rgba(255, 152, 0, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Helper function to extract PDF text
def extract_pdf_text(uploaded_file):
    try:
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
        return text
    except Exception as e:
        st.error(f"Error parsing PDF: {str(e)}")
        return None

# Initializing Session State variables
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "uploaded_pdf_text" not in st.session_state:
    st.session_state.uploaded_pdf_text = ""
if "uploaded_pdf_name" not in st.session_state:
    st.session_state.uploaded_pdf_name = ""
if "summary_output" not in st.session_state:
    st.session_state.summary_output = ""

# Sidebar Setup
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/education.png", width=70)
    st.title("Settings")
    
    # API Key Configuration
    st.subheader("🔑 API Authentication")
    api_key_input = st.text_input(
        "Enter Gemini API Key",
        type="password",
        value=os.getenv("GEMINI_API_KEY", ""),
        help="Get an API Key from Google AI Studio. The key is processed locally and not stored."
    )
    
    # Model Selection
    model_choice = st.selectbox(
        "Choose Gemini Model",
        options=["gemini-1.5-flash", "gemini-1.5-pro"],
        index=0,
        help="Gemini 1.5 Flash is recommended for fast summaries. Gemini 1.5 Pro is excellent for complex analysis."
    )
    
    # Status Indicators
    st.markdown("---")
    st.subheader("⚙️ System Status")
    if api_key_input:
        st.markdown('<div class="status-badge status-success">🟢 Connected to Gemini</div>', unsafe_allow_html=True)
        genai.configure(api_key=api_key_input)
    else:
        st.markdown('<div class="status-badge status-warning">🟡 Missing API Key</div>', unsafe_allow_html=True)
        st.caption("Please configure your API Key to enable the AI engine.")
        
    st.markdown("""
    <div class="sidebar-card">
        <h4>💡 Quick Guide</h4>
        <ol style="padding-left: 15px; margin: 0; font-size: 0.85rem; color: #CBD5E1;">
            <li>Input API Key first.</li>
            <li>Select a tab on the main page.</li>
            <li>Upload a research PDF or write raw text.</li>
            <li>Generate structured insights instantly.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

# Main Application Layout
st.markdown('<h1 class="title-gradient">🎓 AI Research Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">Empower your academic workflows: analyze papers, chat with a research partner, and query document archives.</p>', unsafe_allow_html=True)

# Main Navigation Tabs
tab_summarize, tab_chat, tab_qa = st.tabs([
    "📄 Paper Summarizer", 
    "💬 Literature Partner", 
    "📁 Document Q&A"
])

# ----------------- PAGE 1: PAPER SUMMARIZER -----------------
with tab_summarize:
    st.subheader("Summarize & Structure Research Articles")
    st.write("Upload a research paper PDF or paste raw text below to generate a comprehensive, structured briefing.")

    col_input, col_action = st.columns([2, 1])
    
    with col_input:
        input_type = st.radio("Choose Input Format", ["Upload PDF File", "Paste Text Content"], horizontal=True)
        
        pdf_text = ""
        if input_type == "Upload PDF File":
            uploaded_file = st.file_uploader("Upload Research PDF", type=["pdf"])
            if uploaded_file:
                # Cache PDF parsing in session state
                if st.session_state.uploaded_pdf_name != uploaded_file.name:
                    with st.spinner("Extracting text from PDF..."):
                        extracted = extract_pdf_text(uploaded_file)
                        if extracted:
                            st.session_state.uploaded_pdf_text = extracted
                            st.session_state.uploaded_pdf_name = uploaded_file.name
                            st.success(f"Successfully extracted {len(extracted)} characters from '{uploaded_file.name}'!")
                pdf_text = st.session_state.uploaded_pdf_text
        else:
            pdf_text = st.text_area("Paste Article Text", height=250, placeholder="Paste the text of the paper here...")

    with col_action:
        st.markdown("""
        <div class="research-card">
            <h4>⚡ Insights Setup</h4>
            <p style="font-size: 0.85rem; color: #A0AEC0;">Configure how you want the AI to analyze your source paper.</p>
        </div>
        """, unsafe_allow_html=True)
        
        detail_level = st.select_slider(
            "Detail Depth",
            options=["Brief Outline", "Balanced Summary", "Comprehensive Analysis"],
            value="Balanced Summary"
        )
        
        summarize_button = st.button("🚀 Analyze & Summarize")

    # Summarization Execution
    if summarize_button:
        if not api_key_input:
            st.error("Please add your Gemini API Key in the sidebar before running.")
        elif not pdf_text.strip():
            st.error("Please upload a PDF or enter some text to summarize.")
        else:
            with st.spinner("Running deep literature analysis..."):
                try:
                    model = genai.GenerativeModel(model_choice)
                    
                    system_prompt = f"""You are a senior academic researcher and professor. Generate a high-quality, professional, and detailed {detail_level} summary of the research paper provided below.
                    Structure your response using these exact markdown headers:
                    
                    ## 📌 Overview & Abstract
                    (Provide a concise 3-4 sentence explanation of the paper's core contribution and value)
                    
                    ## 🔍 Research Questions & Hypotheses
                    (What exact questions are the authors trying to answer?)
                    
                    ## 🧪 Methodology & Setup
                    (Describe the study design, dataset, experimental setup, tools, or algorithms used)
                    
                    ## 📊 Key Findings & Results
                    (What were the main outputs, achievements, data trends, or outcomes?)
                    
                    ## ⚠️ Limitations & Future Work
                    (What boundaries, weaknesses, or open areas of research are outlined?)
                    
                    ## 📚 Generated Citations
                    - **APA**: (Generate APA style citation)
                    - **MLA**: (Generate MLA style citation)
                    - **Chicago**: (Generate Chicago style citation)
                    
                    Here is the paper text to analyze:
                    {pdf_text[:80000]} # Limit to 80k characters for basic safety, though Gemini can handle more
                    """
                    
                    response = model.generate_content(system_prompt)
                    st.session_state.summary_output = response.text
                except Exception as e:
                    st.error(f"Error communicating with Gemini API: {str(e)}")

    if st.session_state.summary_output:
        st.markdown("### 📋 Analysis Results")
        st.markdown(f'<div class="research-card">{st.session_state.summary_output}</div>', unsafe_allow_html=True)
        
        st.download_button(
            label="📥 Download Summary (Markdown)",
            data=st.session_state.summary_output,
            file_name=f"summary_{st.session_state.uploaded_pdf_name.replace('.pdf', '') or 'research'}.md",
            mime="text/markdown"
        )

# ----------------- PAGE 2: LITERATURE COMPANION (CHAT) -----------------
with tab_chat:
    st.subheader("💬 Literature & Research Companion")
    st.write("Brainstorm hypotheses, draft review outlines, or discuss complex methodologies with your AI partner.")
    
    # Clear history button
    if st.button("🗑️ Reset Chat History", key="clear_chat"):
        st.session_state.chat_history = []
        st.rerun()

    # Display chat messages
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            
    # Chat user input
    user_msg = st.chat_input("Ask a research question or brainstorm an idea...")
    
    if user_msg:
        # Show user message
        with st.chat_message("user"):
            st.write(user_msg)
        st.session_state.chat_history.append({"role": "user", "content": user_msg})
        
        if not api_key_input:
            st.error("Please add your Gemini API Key in the sidebar before typing.")
        else:
            with st.spinner("Refining response..."):
                try:
                    # Construct message list history for Gemini chat format
                    model = genai.GenerativeModel(model_choice)
                    chat = model.start_chat(history=[])
                    
                    # Define research system guidelines in chat context
                    chat_context = f"""You are a professional, peer-review-level research companion. Support the researcher with rigorous, academic, and logically sound advice. 
                    Be constructive, suggest references or methodologies where appropriate, and push for scientific clarity.
                    
                    The researcher asks: {user_msg}
                    """
                    
                    # Send message and get output
                    response = chat.send_message(chat_context)
                    
                    with st.chat_message("assistant"):
                        st.write(response.text)
                    st.session_state.chat_history.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"Error generating chat response: {str(e)}")

# ----------------- PAGE 3: DOCUMENT Q&A -----------------
with tab_qa:
    st.subheader("📁 Interactive Document Q&A")
    st.write("Query your uploaded document directly. The model will focus its answers strictly on the context of the PDF.")
    
    # Check if a PDF has already been uploaded in Summarizer tab
    current_pdf_name = st.session_state.uploaded_pdf_name
    current_pdf_text = st.session_state.uploaded_pdf_text
    
    if current_pdf_name:
        st.info(f"Using currently loaded paper: **{current_pdf_name}** ({len(current_pdf_text)} characters loaded).")
        
        qa_input = st.text_input("Ask a question about this paper:", placeholder="e.g. What datasets were used? What is the main baseline model?")
        
        if st.button("🔍 Query Document"):
            if not api_key_input:
                st.error("Please add your Gemini API Key in the sidebar first.")
            elif not qa_input.strip():
                st.error("Please type a valid question.")
            else:
                with st.spinner("Analyzing document references..."):
                    try:
                        model = genai.GenerativeModel(model_choice)
                        
                        prompt = f"""You are an expert research analyst. Answer the user's question by referencing the provided research paper content. 
                        Be precise, factual, and specify context details (e.g. section titles or figures) from the paper. 
                        If the text does not contain the answer, say "Based on the provided text, this information is not explicitly mentioned."
                        
                        --- DOCUMENT CONTENT ---
                        {current_pdf_text[:100000]} # Safe context limit
                        
                        --- USER QUESTION ---
                        {qa_input}
                        """
                        
                        response = model.generate_content(prompt)
                        st.markdown("#### 💡 Answer")
                        st.markdown(f'<div class="research-card">{response.text}</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error querying Gemini model: {str(e)}")
    else:
        st.warning("⚠️ No document uploaded yet. Go to the 'Paper Summarizer' tab and upload a PDF to enable Document Q&A.")
