from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('Spk+zx1Cu/+CjwAyWKl3LcfSHkTQ1cXmeAU10EWkDvYdk6otZJicpzeYu6fH0dAVU8oKF8jFJdCioLMPlhIND2AVe/zsY533PWHkF+ZdRJJyBsf92JHiF+bOjoPaJDZbZ+ZDQFx2rksyuHabfc2RgwdB04t89/1O/w1cDnyilFU=')
webhook_handler = WebhookHandler('85488642ac423be5bf7f12a55d2091d1')

@app.route("/")
def home():
    return "LINE BOT API Server is Running"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        webhook_handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@webhook_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()