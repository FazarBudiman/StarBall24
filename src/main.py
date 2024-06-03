import os
from flask import Flask, request, jsonify
import pandas as pd
import pickle

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify('Hello Fucking World !!!')

@app.route('/predict', methods=['POST'])
def predict():
  try:
    model = pickle.load(open('src/assets/model.pkl', 'rb'))
    
    data = request.get_json()

    team_name_dict={
        "arsenal" : 0,
        "aston villa": 1,
        "bournemouth":2,
        "brentford":3,
        "brighton":4,
        "burnley":5,
        "chelsea":6,
        "crystal palace":7,
        "everton":8,
        "fulham":9,
        "leeds":10,
        "leicester":11,
        "liverpool":12,
        "manchester city":13,
        "manchester united":14,
        "newcastle":15,
        "norwich":16,
        "nottingham forest":17,
        "southampton":18,
        "tottenham":19,
        "watford":20,
        "west ham":21,
        "wolves":22,
        "luton":23,
        "sheffield utd":24
    }

    day_code_dict = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6
    }

    home_team_code = team_name_dict.get(data['home_team_code'])
    away_team_code = team_name_dict.get(data['away_team_code'])
    day_code = day_code_dict.get(data['day_code'])

    new_data = {
        "HomeTeam_code": home_team_code,
        "AwayTeam_code": away_team_code,
        "Hour": data['hour'],
        "Day_code": day_code
    }

    new_df = pd.DataFrame([new_data])

    prediction = model.predict(new_df)[0]  

    outcome_mapping = {0: "Away Team Win", 1: "Draw", 2: "Home Team Win"}
    predicted_outcome = outcome_mapping.get(prediction, "Unexpected Prediction Result")

    response = {'predicted_outcome': predicted_outcome}
    return jsonify(response)

  except Exception as e:
    return jsonify({'error': str(e)}), 500

def main():
    app.run(port=int(os.environ.get('PORT', 80)),  debug=True)

if __name__ == "__main__":
    main()
