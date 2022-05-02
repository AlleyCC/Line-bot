#用flask架設伺服器

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

line_bot_api = LineBotApi('kescPKLwp396j8NiHM/fv8Xp/2qmM1yyvhHM2YW4gZH5//pdXBDUaWI9x8g8JngzK9lnKKT5bKwEqjYHzC0kR+mAH1t36DGkGkSeXyFNInnQxatQ/1Hsf7yc/Hom4mjkNVSzMvBjLo8UDpqeM8GNIgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('7d32133a60286c9f6cd3968433b4ee36')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()