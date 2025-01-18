from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
# 環境変数のロード
load_dotenv()

app = Flask(__name__)

# LINE Messaging APIの設定を環境変数から取得
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')

# 必要な環境変数が設定されているか確認
if not LINE_CHANNEL_ACCESS_TOKEN or not LINE_CHANNEL_SECRET:
    raise ValueError("LINE_CHANNEL_ACCESS_TOKENまたはLINE_CHANNEL_SECRETが設定されていません。")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# ハードコーディングされた電車の時刻データ
train_schedule = [
    "10:00", "10:15", "10:30", "10:45", "11:00", "11:15", "11:30", "11:45", "12:00"
]

@app.route("/callback", methods=['POST'])
def callback():
    # LINEサーバーからのリクエストを取得
    signature = request.headers.get('X-Line-Signature')
    body = request.get_data(as_text=True)

    # リクエスト内容をログ出力
    print(f"Request body: {body}")
    print(f"Signature: {signature}")

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Check LINE_CHANNEL_SECRET.")
        abort(400)
    except Exception as e:
        print(f"Error handling message: {e}")
        abort(500)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # デバッグログ
    print(f"Received message: {event.message.text}")

    # メッセージが「東京駅から新橋まで」の場合のみ処理
    if event.message.text == "東京駅から新橋まで":
        now = datetime.now()
        one_hour_later = now + timedelta(hours=1)

        # 現在時刻と比較して、1時間以内の時刻を取得
        upcoming_trains = [
            time for time in train_schedule
            if now.time() <= datetime.strptime(time, "%H:%M").time() <= one_hour_later.time()
        ]

        # メッセージ作成
        if upcoming_trains:
            response_message = "次の電車の時刻:\n" + "\n".join(upcoming_trains)
        else:
            response_message = "次の1時間以内に電車はありません。"
    else:
        response_message = f"受信したメッセージ: {event.message.text}"

    # LINEに返信
    try:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response_message)
        )
        print("Reply sent successfully.")
    except Exception as e:
        print(f"Error sending reply: {e}")

if __name__ == "__main__":
    # Flaskアプリの起動
    app.run(host="0.0.0.0", port=8000, debug=True)
