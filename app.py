from flask import Flask, render_template, request, jsonify
import requests
from config import API_KEY

app = Flask(__name__, template_folder="frontend", static_folder="frontend")

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/get_weather', methods=['POST'])
def get_weather():
    # Example API endpoint (You need to replace 'Your_API_Key' with your actual OpenWeatherMap API key)
    api_url = f"http://api.openweathermap.org/data/2.5/forecast?id=524901&appid={API_KEY}"

    response = requests.get(api_url)
    data = response.json()  # Converts the JSON response to a Python dictionary
    return jsonify(data)  # Returns data as JSON

if __name__ == '__main__':
    app.run(debug=True)
