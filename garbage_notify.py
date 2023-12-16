import calendar
import datetime
import pandas as pd
import requests

def get_nth_week(year, month, day, firstweekday=0):
    first_dow = datetime.date(year, month, 1).weekday()
    offset = (first_dow - firstweekday) % 7
    return (day + offset - 1) // 7 + 1

def get_nth_dow(year, month, day):
    return get_nth_week(year, month, day, 6), calendar.weekday(year, month, day)

def send_line(text):
    url = 'https://notify-api.line.me/api/notify'
    token = 'DH9Fcyyam72VHKqj8fmBFstBJOuPobRpQUL4gDPvRCS'
    headers = {'Authorization' : 'Bearer ' + token}
    message = text
    payload = {'message' : message}
    p = requests.post(url, headers=headers, data=payload)
    print(p)

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
    send_line(text2)

# send_line(text2)
# print(pd.__version__)