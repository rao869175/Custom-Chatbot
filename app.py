from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    user_message = request.form.get("user_message")

    # Custom check for developer name question
    if user_message.strip().lower() == "what is your developer name?":
        return jsonify({"bot_reply": "Rao Zain"})

    # Otherwise — send message to Groq API
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": "Bearer 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",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {
                "role": "system",
                "content": "You are a professional health assistant chatbot. Answer only health-related questions clearly and concisely. "
                           "If a question is unrelated to health, reply: 'Sorry, I can only assist with health-related information.'"
            },
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.5
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        choices = data.get('choices')
        if choices and 'message' in choices[0]:
            reply = choices[0]['message']['content']
            return jsonify({"bot_reply": reply.strip()})
        else:
            return jsonify({"bot_reply": "Sorry, I couldn't get a valid response. Please try again."})

    except Exception as e:
        return jsonify({"bot_reply": f"API request failed: {e}"})


if __name__ == "__main__":
    app.run(debug=True)
