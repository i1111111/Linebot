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
import datetime

app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('60Cu38jaKl8XCZL5n8K+TJvs7heExFNDNHKvkYq8fv83wQRdb2G3kJWpVo4B0RzzSv0xlcyvTktzRfK95nK9GiW64PDQtJDYG/zkf+2UjFb6u2U3PrY4+RYbZL+gBOzJ3dwGM94xRCuPx5rDeLB6qAdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('9f8c5f245a4a4d2734a2e7ac1477f6f0')

# 推送欢迎信息
line_bot_api.push_message(
    'U0d6d8cfdae6abfa3e4628b1ab7b976c9', 
    TextSendMessage(text=f"您好,目前時間是 {datetime.datetime.now().strftime('%Y/%m/%d %H:%M')} ，請問需要什麼服務呢?")
)

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

# 訊息傳遞區塊
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = text=event.message.text
    if re.match('告訴我秘密',message):
        buttons_template_message = TemplateSendMessage(
        alt_text='這是樣板傳送訊息',
        template=ButtonsTemplate(
            thumbnail_image_url='https://i.imgur.com/kNBl363.jpg',
            title='中華民國',
            text='選單功能－TemplateSendMessage',
            actions=[
                PostbackAction(
                    label='這是PostbackAction',
                    display_text='顯示文字',
                    data='實際資料'
                ),
                MessageAction(
                    label='這是MessageAction',
                    text='實際資料'
                ),
                URIAction(
                    label='這是URIAction',
                    uri='https://en.wikipedia.org/wiki/Taiwan'
                )
            ]
        )
    )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)