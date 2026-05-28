import requests
from flask import Flask, render_template, request

# Template folder configuration for root directory
app = Flask(__name__, template_folder='templates')

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
                weather_info = {"error": "error_city"}
        except:
            weather_info = {"error": "error_system"}
    return render_template('index.html', roads=ROAD_DATA, weather=weather_info)

@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    trigger_type = None
    user_message = None
    if request.method == 'POST':
        user_message = request.form.get('message', '').strip()
        if user_message:
            if "靜宜資管特色" in user_message:
                trigger_type = "feature"
            elif "嗨" in user_message or "hello" in user_message or "你好" in user_message:
                trigger_type = "hello"
            elif "天氣" in user_message:
                trigger_type = "weather"
            elif "路口" in user_message or "交通" in user_message or "肇事" in user_message:
                trigger_type = "traffic"
            else:
                trigger_type = "default"
    return render_template('chatbot.html', user_message=user_message, trigger_type=trigger_type)

app.debug = True
