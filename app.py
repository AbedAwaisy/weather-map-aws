from flask import Flask, render_template, request, jsonify, send_from_directory
import requests
import matplotlib  # Ensure this is at the top
matplotlib.use('Agg')  # Set the backend before importing pyplot
import matplotlib.pyplot as plt
from config import API_KEY
from datetime import datetime, timedelta

app = Flask(__name__, template_folder="frontend", static_folder="frontend")


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/get_weather', methods=['POST'])
def get_weather():
    data = request.get_json()
    latitude = data['latitude']
    longitude = data['longitude']
    time_range = data.get('timeRange', 'today')  # Default to 'today'

    api_url = f"http://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={API_KEY}&units=metric"
    response = requests.get(api_url)
    weather_data = response.json()

    filtered_data = filter_data_by_time_range(weather_data, time_range)
    create_temperature_graph(filtered_data)
    create_wind_graph(filtered_data)
    create_rain_graph(filtered_data)

    return jsonify(filtered_data)


def filter_data_by_time_range(data, time_range):
    if time_range == 'next5days':
        return data  # Return all data as is for 'next5days'

    filtered_list = []
    current_date = datetime.now().date()
    day_offset = 1 if time_range == 'tomorrow' else 0
    target_date = (current_date + timedelta(days=day_offset)).strftime('%Y-%m-%d')

    for forecast in data['list']:
        forecast_date = forecast['dt_txt'].split(' ')[0]
        if forecast_date == target_date:
            filtered_list.append(forecast)

    return {'list': filtered_list}


def create_temperature_graph(weather_data):
    dates = [entry['dt_txt'] for entry in weather_data['list']]
    temperatures = [entry['main']['temp'] for entry in weather_data['list']]

    plt.figure(figsize=(10, 5))  # Increase figure size
    plt.plot(dates, temperatures, marker='o', linestyle='-', color='b')
    plt.title('Temperature Forecast')
    plt.xlabel('Date and Time')
    plt.ylabel('Temperature (°C)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('static/temperature_plot.png')
    plt.close()

def create_wind_graph(weather_data):
    dates = [entry['dt_txt'] for entry in weather_data['list']]
    wind_speeds = [entry['wind']['speed'] for entry in weather_data['list']]

    plt.figure(figsize=(10, 5))  # Increase figure size
    plt.plot(dates, wind_speeds, marker='o', linestyle='-', color='g')
    plt.title('Wind Speed Forecast')
    plt.xlabel('Date and Time')
    plt.ylabel('Wind Speed (m/s)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('static/wind_plot.png')
    plt.close()

def create_rain_graph(weather_data):
    dates = [entry['dt_txt'] for entry in weather_data['list']]
    rain_volumes = [entry.get('rain', {}).get('3h', 0) for entry in weather_data['list']]  # Handle possible absence of 'rain' data

    plt.figure(figsize=(10, 5))  # Increase figure size
    plt.bar(dates, rain_volumes, color='b')
    plt.title('Rain Volume Forecast')
    plt.xlabel('Date and Time')
    plt.ylabel('Rain Volume (mm)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('static/rain_plot.png')
    plt.close()



@app.route('/temperature_plot.png')
def temperature_plot():
    return send_from_directory('static', 'temperature_plot.png')


@app.route('/wind_plot.png')
def wind_plot():
    return send_from_directory('static', 'wind_plot.png')


@app.route('/rain_plot.png')
def rain_plot():
    return send_from_directory('static', 'rain_plot.png')


if __name__ == '__main__':
    app.run(debug=True)
