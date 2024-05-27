from flask import Flask, request, jsonify
import pandas as pd
import pickle

# Assuming the saved model filename is 'model.joblib' in your Google Drive
app = Flask(__name__)

@app.route('/home', methods=['GET'])
def hello():
  return "Hello World"

@app.route('/predict', methods=['POST'])
def predict():

  try:
    model_path = 'model.pkl' 
    model = pickle.load(open(model_path, 'rb'))
    
    data = request.get_json()

    new_data = {
        "HomeTeam_code": data['home_team_code'],
        "AwayTeam_code": data['away_team_code'],
        "Hour": data['hour'],
        "Day_code": data['day_code']
    }

    new_df = pd.DataFrame([new_data])

    prediction = model.predict(new_df)[0]  

    outcome_mapping = {0: "Away Team Wins", 1: "Draw", 2: "Home Team Wins"}
    predicted_outcome = outcome_mapping.get(prediction, "Unexpected Prediction Result")

    response = {'predicted_outcome': predicted_outcome}
    return jsonify(response)

  except Exception as e:
    return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000) 
