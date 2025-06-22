from flask import Flask, request
import requests

from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Use your actual OpenRouter API key here
OPENROUTER_API_KEY = "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"

def get_chatgpt_response(prompt):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://shinigami-x.onrender.com",
        "X-Title": "whatsapp-agent"
    }
    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

    try:
        response.raise_for_status()
        json_response = response.json()
        if 'choices' in json_response:
            return json_response['choices'][0]['message']['content']
        else:
            return "Error: 'choices' not found in OpenRouter response."
    except Exception as e:
        return f"OpenRouter API Error: {str(e)}"

@app.route("/", methods=["GET"])
def home():
    return "Shinigami.X is online!"
    
@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.form.get('Body')
    resp = MessagingResponse()

    if incoming_msg:
        reply = get_chatgpt_response(incoming_msg)
        resp.message(reply)
    else:
        resp.message("Send something!")
    
    return str(resp), 200

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Default to 10000 if PORT not set
    app.run(host="0.0.0.0", port=port, debug=True)

