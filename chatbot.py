from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import re

# ChatBotのインスタンスを作成
chatbot = ChatBot(
    'RetirementBot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///database.sqlite3',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch'
        }
    ]
)

# 学習データの用意（退職手続きに関する質問と回答）
conversation = [
    "退職したいです。",
    "退職をご希望ですね。退職届の提出が必要です。",
    "退職届はどこで入手できますか？",
    "会社のウェブサイトからダウンロード可能です。",
    "必要な手続きは何ですか？",
    "退職届の提出と業務の引き継ぎが必要です。",
    "健康保険はどうなりますか？",
    "退職後は国民健康保険に加入してください。",
    "有給休暇は消化できますか？",
    "残りの有給休暇は消化可能です。詳細は上司に相談してください。",
    "退職金は支給されますか？",
    "就業規則に基づき支給されます。人事部にお問い合わせください。",
    "離職票は発行されますか？",
    "はい、退職後に離職票を郵送いたします。",
    "退職後の年金手続きはどうすればよいですか？",
    "最寄りの年金事務所で手続きを行ってください。"
]

# トレーナーの設定と学習
trainer = ListTrainer(chatbot)
trainer.train(conversation)

# ユーザー入力の前処理関数
def preprocess(text):
    # 小文字に変換
    text = text.lower()
    # 記号を削除
    text = re.sub(r'[^\w\s]', '', text)  
    # 余分な空白を削除
    text = re.sub(r'\s+', ' ', text).strip()  
    return text

# ユーザーとの対話
print("退職手続きBotへようこそ。ご質問をどうぞ。")
while True:
    try:
        user_input = input("あなた: ")  # ユーザーからの入力を取得
        user_input = preprocess(user_input)  # 入力を前処理
        if user_input.lower() in ["終了", "exit", "bye"]:
            print("Bot: ご利用ありがとうございました。")
            break
        bot_response = chatbot.get_response(user_input)
        print(f"Bot: {bot_response}")
    except (KeyboardInterrupt, EOFError):
        print("\nBot: ご利用ありがとうございました。")
        break
# webを有効にするには、python app.pyをターミナルで実行後、終了する必要がある
