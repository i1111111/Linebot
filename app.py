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
    message = event.message.text
    # 处理用户输入
    if message == "天氣":
        reply_text = "請稍等，我幫您查詢天氣資訊！"
    else:
        reply_text = "很抱歉，我目前無法理解這個內容。"
    
    # 回覆訊息
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

# 主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
