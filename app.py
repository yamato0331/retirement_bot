from flask import Flask, render_template, request
from chatterbot import ChatBot
from textblob import TextBlob

app = Flask(__name__)

chatbot = ChatBot("RetirementBot")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    user_text = request.args.get('msg')
    analysis = TextBlob(user_text)
    if analysis.sentiment.polarity > 0:
        return str(chatbot.get_response(user_text)) + " 😊"
    elif analysis.sentiment.polarity < 0:
        return str(chatbot.get_response(user_text)) + " 😟"
    else:
        return str(chatbot.get_response(user_text))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000, debug=True)
