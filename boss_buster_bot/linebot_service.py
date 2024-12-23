from flask import Flask, request, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import gpt_service
import os

app = Flask(__name__)

# Line Bot credentials
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


@app.route("/callback", methods=["POST"])
def callback():
    # Get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]

    # Get request body as text
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return jsonify({"message": "Invalid signature"}), 400

    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    response = gpt_service.get_law_based_answer(user_message)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response))


class LineBotApp:
    def __init__(self):
        self.app = app  # 使用 Flask 應用程式實例

    def run(self, host="0.0.0.0", port=5000):
        self.app.run(host=host, port=port)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
