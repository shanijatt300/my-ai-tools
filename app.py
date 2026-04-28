import streamlit as st
import requests
from bs4 import BeautifulSoup

# --- Page UI Configuration ---
st.set_page_config(page_title="Alishan's AI Suite", layout="wide", page_icon="🚀")

# Custom CSS for Modern Look
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .main-title { color: #1E1E1E; font-size: 40px; font-weight: bold; text-align: center; margin-bottom: 20px; }
    .tool-box { background: white; padding: 25px; border-radius: 15px; border: 1px solid #ddd; }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar: API Activation & Tool Selection ---
st.sidebar.header("🔧 Control Panel")
api_key_input = st.sidebar.text_input("Enter DeepSeek API Key:", type="password")

if "active_api" not in st.session_state:
    st.session_state.active_api = None

if st.sidebar.button("Activate API Key ✅"):
    if api_key_input:
        st.session_state.active_api = api_key_input
        st.sidebar.success("API Key Activated Successfully!")
    else:
        st.sidebar.error("Please enter a valid key.")

st.sidebar.divider()
tool_choice = st.sidebar.radio("Select a Tool:", [
    "🔍 AI SEO Strategist", 
    "📧 Cold Email Pro", 
    "🛍️ Shopify Product Expert", 
    "🏢 B2B Lead Researcher", 
    "💻 AI Code Auditor"
])

# --- Core AI Function ---
def get_ai_response(prompt):
    if not st.session_state.active_api:
        st.error("❌ API Key Active Nahi Hai! Sidebar se activate karein.")
        return None
    
    url = "https://api.deepinfra.com/v1/openai/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {st.session_state.active_api}"
    }
    data = {
        "model": "deepseek-ai/DeepSeek-V3",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.6
    }
    
    try:
        with st.spinner("AI Generating Response..."):
            response = requests.post(url, headers=headers, json=data)
            return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: API response mein masla hai. Check Balance/Key. ({str(e)})"

# --- Main Logic for 5 Tools ---
st.markdown(f"<div class='main-title'>{tool_choice}</div>", unsafe_allow_html=True)

# 1. SEO Strategist
if tool_choice == "🔍 AI SEO Strategist":
    url = st.text_input("Website URL (e.g., https://example.com):")
    if st.button("Analyze Now"):
        try:
            # Scraping to get site context
            headers = {'User-Agent': 'Mozilla/5.0'}
            res = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            title = soup.title.string if soup.title else "No Title Found"
            
            prompt = f"Perform a professional SEO audit for {url}. Title: {title}. Provide SEO Score, 5 target keywords, and better Meta Description."
            st.markdown(get_ai_response(prompt))
        except:
            st.error("Website scan nahi ho saki. URL check karein.")

# 2. Cold Email Pro
elif tool_choice == "📧 Cold Email Pro":
    service = st.text_area("Your Service (Web Dev, SEO, etc.):")
    niche = st.text_input("Target Client (e.g., Real Estate, Gyms):")
    if st.button("Generate 5 Emails"):
        prompt = f"Write 5 personalized cold emails to sell {service} to {niche}. Make them short and high-converting."
        st.markdown(get_ai_response(prompt))

# 3. Shopify Product Expert
elif tool_choice == "🛍️ Shopify Product Expert":
    p_info = st.text_area("Product Details:")
    if st.button("Create Listing"):
        prompt = f"Create a high-converting Shopify Title, Description, and SEO Alt Tags for: {p_info}"
        st.markdown(get_ai_response(prompt))

# 4. B2B Lead Researcher
elif tool_choice == "🏢 B2B Lead Researcher":
    target_site = st.text_input("Company URL to Research:")
    if st.button("Get Insights"):
        try:
            res = requests.get(target_site, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
            text_context = res.text[:2000]
            prompt = f"Based on this text, what does this company do and who is their ideal client? Text: {text_context}"
            st.markdown(get_ai_response(prompt))
        except:
            st.error("Site research fail ho gayi.")

# 5. AI Code Auditor
elif tool_choice == "💻 AI Code Auditor":
    code = st.text_area("Paste Code Here (Python/HTML/CSS):", height=250)
    if st.button("Audit Code"):
        prompt = f"Analyze this code for bugs, security risks, and optimization. Suggest improvements: \n{code}"
        st.markdown(get_ai_response(prompt))

st.sidebar.markdown("---")
st.sidebar.info("Developed by Alishan | Digital Expert")
