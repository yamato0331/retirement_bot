import os

os.system("pip install --upgrade pip")

from flask import Flask, render_template, request
from chatterbot import ChatBot
from textblob import TextBlob

app = Flask(__name__)

chatbot = ChatBot("RetirementBot")
# アップロード先のディレクトリ
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# アップロード用のHTMLフォームの表示
@app.route("/")
def home():
    return render_template("index.html")  # index.htmlというテンプレートを表示

# ボットの応答を取得
@app.route("/get")
def get_bot_response():
    user_text = request.args.get('msg')
    return str(chatbot.get_response(user_text))

import os

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
    # アップロードフォルダが存在しない場合は作成
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(host='0.0.0.0', port=10000, debug=True)
