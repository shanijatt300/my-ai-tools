import streamlit as st
import requests
from bs4 import BeautifulSoup
import os

# DeepSeek API Configuration
# Note: Live hosting ke waqt 'DEEPSEEK_API_KEY' ko environment variables mein set karein
API_KEY = st.sidebar.text_input("Enter DeepSeek API Key:", type="password")
BASE_URL = "https://api.deepinfra.com/v1/openai/chat/completions"

def call_deepseek(prompt):
    if not API_KEY:
        st.error("Please enter your API Key in the sidebar!")
        return None
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    data = {
        "model": "deepseek-ai/deepseek-coder-33b-instruct", # Best for coding and logic
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    
    response = requests.post(BASE_URL, headers=headers, json=data)
    return response.json()['choices'][0]['message']['content']

# --- UI Setup ---
st.set_page_config(page_title="AI Business Suite", layout="wide")
st.title("🚀 Multi-Tool AI Agency Dashboard")

menu = ["SEO Strategist", "Cold Email Pro", "Shopify Expert", "Lead Researcher", "Code Auditor"]
choice = st.sidebar.selectbox("Select Tool", menu)

# --- Tool 1: AI SEO Strategist ---
if choice == "SEO Strategist":
    st.header("🔍 AI SEO Strategist")
    url = st.text_input("Enter Website URL:")
    if st.button("Analyze SEO"):
        try:
            res = requests.get(url, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            title = soup.title.string if soup.title else "No Title"
            desc = soup.find("meta", attrs={"name": "description"})
            desc = desc["content"] if desc else "No Description"
            
            prompt = f"Analyze this website SEO: Title: {title}, Meta: {desc}. Provide an SEO Score (0-100), 5 Keyword suggestions, and an optimized Meta Title/Description."
            report = call_deepseek(prompt)
            st.write(report)
        except Exception as e:
            st.error(f"Error fetching URL: {e}")

# --- Tool 2: Cold Email Pro ---
elif choice == "Cold Email Pro":
    st.header("📧 Cold Email Generator")
    biz_desc = st.text_area("What service are you offering?")
    target = st.text_input("Who is your target audience? (e.g. Real Estate Agents)")
    if st.button("Generate Emails"):
        prompt = f"Generate 5 personalized cold email templates for a business that does: {biz_desc}. Target audience: {target}. Use professional yet catchy tones."
        emails = call_deepseek(prompt)
        st.markdown(emails)

# --- Tool 3: Shopify Product Expert ---
elif choice == "Shopify Expert":
    st.header("🛍️ Shopify Product Optimizer")
    prod_info = st.text_area("Enter basic product details:")
    if st.button("Optimize Product"):
        prompt = f"Create a high-converting Shopify product title, an engaging description with bullet points, and SEO alt-text for this product: {prod_info}"
        content = call_deepseek(prompt)
        st.markdown(content)

# --- Tool 4: B2B Lead Researcher ---
elif choice == "Lead Researcher":
    st.header("🏢 B2B Company Researcher")
    target_url = st.text_input("Enter Company Website URL:")
    if st.button("Research Company"):
        try:
            res = requests.get(target_url, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            text = soup.get_text()[:2000] # Taking first 2000 chars for summary
            prompt = f"Summarize the services of this company based on their website text: {text}. Also, predict their target client profile."
            summary = call_deepseek(prompt)
            st.write(summary)
        except Exception as e:
            st.error("Could not reach website.")

# --- Tool 5: AI Code Auditor ---
elif choice == "Code Auditor":
    st.header("💻 AI Code Auditor")
    code_input = st.text_area("Paste your Code (HTML/CSS/Python):", height=300)
    if st.button("Audit Code"):
        prompt = f"Review this code for bugs, performance issues, and suggest improvements: \n\n {code_input}"
        audit_res = call_deepseek(prompt)
        st.code(audit_res)