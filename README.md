# 🎓 AI Research Assistant

A premium, interactive AI-powered assistant built with **Streamlit** and **Gemini 1.5 Pro/Flash** to accelerate academic and literature research. This tool helps researchers summarize papers, extract key methodologies, brainstorm hypotheses, and perform interactive Q&A on uploaded PDF documents.

---

## ✨ Features

- **📄 Paper Summarizer & Analyzer**: Input raw text or upload research PDFs to generate structured summaries including the *Abstract*, *Key Research Questions*, *Methodology*, *Key Findings*, *Limitations*, and *Generated Citations* (APA, MLA, Chicago).
- **💬 Research Companion (Chat)**: Brainstorm research directions, refine hypotheses, and draft literature reviews with a dedicated AI research partner.
- **📁 Interactive Document Q&A**: Upload a research paper (PDF) and ask detailed questions. The assistant parses the document and answers based directly on the paper's contents.
- **🎨 Premium UI Design**: Elegant glassmorphic dashboard styled with a custom dark/light aesthetic, responsive tables, interactive alerts, and intuitive tab navigation.

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.9 or higher
- A **Google Gemini API Key** (Get one from [Google AI Studio](https://aistudio.google.com/))

### 1. Clone or Download the Project
```bash
git clone <your-repository-url>
cd AI_Research
```

### 2. Set Up a Virtual Environment (Recommended)
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate   # On Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Your API Key
You can pass your API Key in two ways:
- **Option A (Environment Variable)**: Create a `.env` file in the root directory:
  ```env
  GEMINI_API_KEY=your_actual_gemini_api_key_here
  ```
- **Option B (UI Sidebar)**: Paste your key directly into the secure sidebar input field in the Streamlit application.

### 5. Run the Application
```bash
streamlit run app.py
```

---

## 🚀 How to Deploy on GitHub

Follow these steps to push your local repository to GitHub:

### Step 1: Initialize Git Local Repository
Open your terminal in the project folder and run:
```bash
git init
git add .
git commit -m "Initial commit: AI Research Assistant Streamlit app"
```

### Step 2: Create a New GitHub Repository
1. Go to your [GitHub account](https://github.com/) and click **New repository** (or visit `https://github.com/new`).
2. Name your repository (e.g., `ai-research-assistant`).
3. Leave "Initialize this repository with..." options **unchecked** (since we already initialized it locally).
4. Click **Create repository**.

### Step 3: Link and Push to GitHub
Copy the commands from the GitHub instruction page and run them in your terminal:
```bash
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo-name>.git
git push -u origin main
```

---

## ☁️ Deploying to Streamlit Community Cloud (Free Hosting)

Once your code is on GitHub, you can deploy it online for free:

1. Sign up/log in at [Streamlit Share](https://share.streamlit.io/).
2. Click **New app** and connect your GitHub account.
3. Select your repository, the `main` branch, and set the main file path to `app.py`.
4. In the **Advanced settings**, you can add your `GEMINI_API_KEY` under **Secrets**:
   ```toml
   GEMINI_API_KEY = "your_actual_api_key"
   ```
5. Click **Deploy!** Your app will be live on the web in a few minutes.

---

## 🔒 License
This project is open-source and available under the [MIT License](LICENSE).
