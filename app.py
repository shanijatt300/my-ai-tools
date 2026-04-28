from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def call_deepseek(api_key, prompt):
    url = "https://api.deepinfra.com/v1/openai/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {
        "model": "deepseek-ai/DeepSeek-V3",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()['choices'][0]['message']['content']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    tool = data.get('tool')
    user_input = data.get('input')
    api_key = data.get('api_key')

    if tool == "seo":
        try:
            res = requests.get(user_input, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
            soup = BeautifulSoup(res.text, 'html.parser')
            title = soup.title.string if soup.title else "No Title"
            prompt = f"Analyze SEO for {user_input}. Title: {title}. Give score and keywords."
        except:
            return jsonify({"error": "URL not reachable"})
    
    elif tool == "email":
        prompt = f"Generate 5 cold emails for: {user_input}"
    elif tool == "shopify":
        prompt = f"Create Shopify title/desc for: {user_input}"
    elif tool == "lead":
        prompt = f"Summarize company services for this info: {user_input}"
    elif tool == "code":
        prompt = f"Audit this code for bugs: {user_input}"

    result = call_deepseek(api_key, prompt)
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)
