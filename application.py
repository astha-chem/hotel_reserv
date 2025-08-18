import joblib
import numpy as np
from config.paths_config import MODEL_OUTPUT_PATH
from flask import Flask, render_template,request
from src.logger import get_logger
app = Flask(__name__)

logger = get_logger(__name__)
loaded_model = joblib.load(MODEL_OUTPUT_PATH)
print("loaded model")
@app.route('/',methods=['GET','POST'])
def index():
    # logger.info("inside index route")
    logger.info(f"Request method: {request.method}, {request.form}")
    if request.method=='POST':
        logger.info(f"Request method: {request.method}, {request.form}")
        lead_time = int(request.form["lead_time"])
        no_of_special_request = int(request.form["no_of_special_request"])
        avg_price_per_room = float(request.form["avg_price_per_room"])
        arrival_month = int(request.form["arrival_month"])
        arrival_date = int(request.form["arrival_date"])

        market_segment_type = int(request.form["market_segment_type"])
        no_of_week_nights = int(request.form["no_of_week_nights"])
        no_of_weekend_nights = int(request.form["no_of_weekend_nights"])

        type_of_meal_plan = int(request.form["type_of_meal_plan"])
        room_type_reserved = int(request.form["room_type_reserved"])


        features = np.array([[lead_time,no_of_special_request,avg_price_per_room,arrival_month,arrival_date,market_segment_type,no_of_week_nights,no_of_weekend_nights,type_of_meal_plan,room_type_reserved]])
        logger.info("built features. Running prediction")
        prediction = loaded_model.predict(features)
        logger.info(f"predicted {prediction[0]}")
        return render_template('index.html', prediction=prediction[0])
    # if request.method != 'POST':
    #     raise Exception("Inspecting request in debugger")
    return render_template("index.html" , prediction=None)

if __name__=="__main__":
    logger.info("app started")
    app.run(host='0.0.0.0' , port=8080)
