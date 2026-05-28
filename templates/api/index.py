import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__, template_folder='../templates')

ROAD_DATA = [
    "西屯區：環中路與市政路口", "北區：中清路與五權路口", 
    "北區：太原路與崇德路口", "烏日區：高鐵東路與高鐵五路口",
    "神岡區：中山路與大富路口", "北屯區：環中東路與太原路口",
    "太平區：市民大道與環中東路口", "神岡區：中山路與大洲路口",
    "西區：台灣大道與五權路口", "西屯區：台灣大道與黎明路口"
]

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_info = None
    if request.method == 'POST':
        city = request.form.get('city', '').strip()
        api_key = "YOUR_API_KEY" 
        url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={api_key}&locationName={city}&elementName=Wx,PoP"
        try:
            res = requests.get(url).json()
            if res.get('success') == 'true' and res['records']['location']:
                loc = res['records']['location'][0]
                wx = loc['weatherElement'][0]['time'][0]['parameter']['parameterName']
                pop = loc['weatherElement'][1]['time'][0]['parameter']['parameterName']
                weather_info = {"city": city, "wx": wx, "pop": pop}
            else:
                weather_info = {"error": "查無資料，請輸入正確縣市名稱（如：臺中市）"}
        except:
            weather_info = {"error": "系統連線錯誤或 API 金鑰失效"}
    return render_template('index.html', roads=ROAD_DATA, weather=weather_info)

@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    bot_response = None
    user_message = None
    if request.method == 'POST':
        user_message = request.form.get('message', '').strip()
        if user_message and "靜宜資管特色" in user_message:
            bot_response = "SPECIAL_FEATURE"
        elif user_message and ("嗨" in user_message or "hello" in user_message or "你好" in user_message):
            bot_response = "你好！我是 MIS 智能助手，有什麼我可以幫忙的嗎？"
        elif user_message and "天氣" in user_message:
            bot_response = "您可以到首頁輸入縣市名稱（例如：臺中市），即可查詢即時天氣與降雨機率喔！"
        elif user_message and ("路口" in user_message or "交通" in user_message or "肇事" in user_message):
            bot_response = "臺中市前三大易肇事路口為：1.市政路與環中路口、2.中清路與五權路口、3.太原路與崇德路口。"
        else:
            bot_response = "我收到您的訊息了。您可以輸入「靜宜資管特色」來查看專屬功能！"
    return render_template('chatbot.html', user_message=user_message, bot_response=bot_response)

app.debug = True
