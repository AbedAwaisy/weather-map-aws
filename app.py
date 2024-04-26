from flask import Flask, render_template, request, jsonify, send_from_directory
import requests
import matplotlib.pyplot as plt
from config import API_KEY
import os

app = Flask(__name__, template_folder="frontend", static_folder="frontend")

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/get_weather', methods=['POST'])
def get_weather():
    data = request.get_json()
    latitude = data['latitude']
    longitude = data['longitude']
    api_url = f"http://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={API_KEY}&units=metric"

    response = requests.get(api_url)
    weather_data = response.json()
    create_temperature_graph(weather_data)  # Call to create the graph
    return jsonify(weather_data)

def create_temperature_graph(weather_data):
    dates = [entry['dt_txt'] for entry in weather_data['list']]
    temperatures = [entry['main']['temp'] for entry in weather_data['list']]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, temperatures, marker='o', linestyle='-', color='b')
    plt.title('Temperature Forecast')
    plt.xlabel('Date and Time')
    plt.ylabel('Temperature (°C)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('static/temperature_plot.png')  # Save the plot to the static folder
    plt.close()

@app.route('/temperature_plot.png')
def temperature_plot():
    return send_from_directory('static', 'temperature_plot.png')

if __name__ == '__main__':
    app.run(debug=True)
