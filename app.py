from flask import Flask, render_template, request
from chatterbot import ChatBot
from transformers import pipeline

app = Flask(__name__)

chatbot = ChatBot("RetirementBot")
sentiment_pipeline = pipeline("sentiment-analysis")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    user_text = request.args.get('msg')
    sentiment = sentiment_pipeline(user_text)[0]
    if sentiment['label'] == 'POSITIVE':
        return str(chatbot.get_response(user_text)) + " 😊"
    elif sentiment['label'] == 'NEGATIVE':
        return str(chatbot.get_response(user_text)) + " 😟"
    else:
        return str(chatbot.get_response(user_text))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000, debug=True)
