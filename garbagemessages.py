import calendar
import datetime
import pandas as pd
# import requests
import requests, os
from linebot.v3 import WebhookHandler
from linebot.v3.messaging import Configuration, MessagingApi, ApiClient, PushMessageRequest, ApiException, TextMessage

configuration = Configuration(
    # access_token = 'wz9wy77xkhIA3KRLtDZI5T8YhtyLwGD6UTVDXbIw3sSVti8qKnaJjpm091uBzGQqc2AcrzinmL68Ns4BFMii8q1pA4ViQuuocPxh4qd5NVJh02LNQlQWYE1BEjbVamuEYYAqBoy3rhTp7fz8z2pe8AdB04t89/1O/w1cDnyilFU='
    access_token = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
)

LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]
handler = WebhookHandler(LINE_CHANNEL_SECRET)

headler = {
    "Content_Type": "application/json",
    "Authorization": "Bearer " + LINE_CHANNEL_ACCESS_TOKEN
}

with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)


        # message=TextMessage(text='届いたんかね？')

        # line_bot_api.push_message_with_http_info(
        #     PushMessageRequest(
        #         to='U19f467cfd98ea214b39f33fccb6f8a6b',
        #         messages=[message]
        #     )
        # )


# def get_nth_week(year, month, day, firstweekday=0):
#     first_dow = datetime.date(year, month, 1).weekday()
#     offset = (first_dow - firstweekday) % 7
#     return (day + offset - 1) // 7 + 1

# def get_nth_dow(year, month, day):
#     return get_nth_week(year, month, day, 6), calendar.weekday(year, month, day)

def get_nth_week(day):
    return (day - 1) // 7 + 1

def get_nth_dow(year, month, day):
    return get_nth_week(day), calendar.weekday(year, month, day)

# def send_line(text):
#     url = 'https://notify-api.line.me/api/notify'
#     token = 'DH9Fcyyam72VHKqj8fmBFstBJOuPobRpQUL4gDPvRCS'
#     headers = {'Authorization' : 'Bearer ' + token}
#     message = text
#     payload = {'message' : message}
#     p = requests.post(url, headers=headers, data=payload)
#     print(p)

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
text2 = "🐦‍⬛か〜\n明日は"+date_check+"収集の日("+text1+")じゃけん。\n忘れんと捨てないかんけん!!"

if date_check == "":
    print("明日のゴミ出しはありません")
else:
    # send_line(text2)
    message=TextMessage(text=text2)

    line_bot_api.push_message_with_http_info(
        PushMessageRequest(
            # to='U19f467cfd98ea214b39f33fccb6f8a6b',
            to = os.environ["TO"]
            messages=[message]
        )
    )


# print(get_nth_week(2023, 12, 3, 6))

# print(text1)
# print(text2)

# send_line(text2)
# print(pd.__version__)