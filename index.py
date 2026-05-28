from flask import Flask, render_template, request
import requests

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
        msg = user_message.lower()
        
        if "靜宜資管特色" in msg:
            bot_response = "靜宜大學管理資訊系統學系（資管系）具備卓越的教學特色與核心優勢。首先，本系致力於「資訊技術」與「管理科學」的深度融合，不僅培養學生撰寫程式、建置資料庫、網頁開發與大數據分析的扎實技術，更強調企業流程管理、數位行銷與專案管理的實務能力，建構跨領域的數位轉型人才。其次，多元化的產學合作是本系一大亮點。學系長期與台灣中部科學園區、各大型企業及醫療機構合作，提供豐富的企業實習機會，讓學生在畢業前即能進入職場累積實戰經驗，縮短學用落差，達成畢業即就業的目標。再者，資管系擁有現代化的雲端運算實驗室與物聯網教學設備，並積極推動國際化學習，鼓勵學生參與海外交換計畫與雙聯學位，開拓國際視野。在核心課程設計上，強調專案專題實作（Capstone），大三至大四期間學生須分組完成一套具備商用價值的完整系統，從中磨練團隊合作與解決問題的能力。教學團隊亦高度重視證照輔導，引導學生考取國內外知名的專業技術證照，大幅提升就業競爭力。總結來說，靜宜資管以完善的導師輔導制度、優質的產學鏈結、扎實的跨域課程，成為中部地區培育新世代資管科技專才的搖籃。"
        elif "嗨" in msg or "hello" in msg or "你好" in msg:
            bot_response = "你好！我是 MIS 智能助手，有什麼我可以幫忙的嗎？"
        elif "天氣" in msg:
            bot_response = "您可以到首頁輸入縣市名稱（例如：臺中市），即可查詢即時天氣與降雨機率喔！"
        elif "路口" in msg or "交通" in msg or "肇事" in msg:
            bot_response = "臺中市前三大易肇事路口為：1.市政路與環中路口、2.中清路與五權路口、3.太原路與崇德路口。"
        else:
            bot_response = f"我收到您的訊息了：「{user_message}」。您可以輸入「靜宜資管特色」來查看專屬功能！"

    return render_template('chatbot.html', user_message=user_message, bot_response=bot_response)

app.debug = True
