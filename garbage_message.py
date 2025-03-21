import calendar
import datetime
import pandas as pd
import requests, os
from linebot.v3 import WebhookHandler
from linebot.v3.messaging import Configuration, MessagingApi, ApiClient, PushMessageRequest, ApiException, TextMessage

configuration = Configuration(
    access_token = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
)

LINE_CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET")
handler = WebhookHandler(LINE_CHANNEL_SECRET)

with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

def get_nth_week(day):
    return (day - 1) // 7 + 1

def get_nth_dow(year, month, day):
    return get_nth_week(day), calendar.weekday(year, month, day)

schedule = pd.DataFrame([
    ["Mon"     , "Tue"        , "Wed", "Thurs"   , "Fri"       , "Sat"       , "Sun"],
    ["燃えるゴミ", "布類"       , ""   , "燃えるゴミ", "古紙類"     , "プラスチック", ""   ],
    ["燃えるゴミ", "ペットボトル", ""   , "燃えるゴミ", "ビン、缶"    , "プラスチック", ""   ],
    ["燃えるゴミ", "不燃ゴミ"   , ""   , "燃えるゴミ", "古紙類"      , "プラスチック", ""   ],
    ["燃えるゴミ", "ペットボトル", ""   , "燃えるゴミ", "ビン、缶"    , "プラスチック", ""   ],
    ["燃えるゴミ", ""          , ""   , "燃えるゴミ", "電池、蛍光灯", "プラスチック", ""   ],
])

date_jp = ['月','火','水','木','金',"土",'日']

# 現在日時取得
today = datetime.datetime.now()
# 現在日時に+1日のタイムデルタを加算
tomorrow = today + datetime.timedelta(days = 1)
#明日の(第n週、X曜日)を取得
tom_nth_dow = get_nth_dow(tomorrow.year, tomorrow.month, tomorrow.day)
date_check = schedule.iat[tom_nth_dow]

text1 = "第"+str(tom_nth_dow[0])+date_jp[tom_nth_dow[1]]+"曜日"
text2 = "＜ゴミの日通知＞ 明日は\n"+date_check+"収集の日\n("+text1+")じゃけん。\n忘れんと捨てないかんけん!!"

if date_check == "":
    print("明日のゴミ出しはありません")
else:
    message=TextMessage(text=text2)
    print(message)
    line_bot_api.push_message_with_http_info(
        PushMessageRequest(
            to = os.environ.get("TO"),
            messages=[message]
        )
    )