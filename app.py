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

# ファイルのアップロードを処理
@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return "ファイルが選択されていません", 400
    file = request.files['file']
    if file.filename == '':
        return "ファイル名が無効です", 400

    # アップロードファイルの拡張子を取得
    file_extension = os.path.splitext(file.filename)[1].lower()

    # アップロード可能なファイルの種類を制限
    if file_extension not in ['.pdf', '.doc', '.docx']:
        return "PDFまたはWord形式のファイルをアップロードしてください", 400

    # ファイルを保存する
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return "退職届をアップロードしました。不備がないか確認しますのでお待ちください", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000, debug=True)