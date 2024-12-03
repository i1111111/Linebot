# -*- coding: utf-8 -*-

#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re
app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('60Cu38jaKl8XCZL5n8K+TJvs7heExFNDNHKvkYq8fv83wQRdb2G3kJWpVo4B0RzzSv0xlcyvTktzRfK95nK9GiW64PDQtJDYG/zkf+2UjFb6u2U3PrY4+RYbZL+gBOzJ3dwGM94xRCuPx5rDeLB6qAdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('9f8c5f245a4a4d2734a2e7ac1477f6f0')

line_bot_api.push_message('U0d6d8cfdae6abfa3e4628b1ab7b976c9', TextSendMessage(text='你可以開始了'))

# 監聽所有來自 /callback 的 Post Request
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
        abort(400)

    return 'OK'

#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token,message)
    if re.match('告訴我秘密',message):
        audio_message = AudioSendMessage(
            original_content_url='https://campus-studio.com/download/twsong.mp3',
            duration=81000
        )
        line_bot_api.reply_message(event.reply_token, audio_message)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
