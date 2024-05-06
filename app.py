from flask import Flask, render_template, request, jsonify, send_from_directory
from weather_data import WeatherData  # Import the WeatherData class

app = Flask(__name__, template_folder="frontend", static_folder="frontend")
weather_data_processor = WeatherData()  # Create an instance of WeatherData

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/get_weather', methods=['POST'])
def get_weather():
    data = request.get_json()
    latitude = data['latitude']
    longitude = data['longitude']
    time_range = data.get('timeRange', 'today')
    filtered_data = weather_data_processor.get_weather_data(latitude, longitude, time_range)
    return jsonify(filtered_data)

@app.route('/temperature_plot.png')
def temperature_plot():
    return send_from_directory('static', 'temperature_plot.png')

@app.route('/wind_plot.png')
def wind_plot():
    return send_from_directory('static', 'wind_plot.png')

@app.route('/rain_plot.png')
def rain_plot():
    return send_from_directory('static', 'rain_plot.png')

@app.route('/save_location', methods=['POST'])
def save_location():
    data = request.get_json()
    result, status = weather_data_processor.save_location(data)
    return jsonify(result), status

@app.route('/get_locations', methods=['GET'])
def get_locations():
    locations = weather_data_processor.get_locations()
    return jsonify(locations)

@app.route('/get_location_data', methods=['POST'])
def get_location_data():
    data = request.get_json()
    location_name = data.get('locationName')
    result, status = weather_data_processor.get_location_data(location_name)
    return jsonify(result), status

if __name__ == '__main__':
    app.run(debug=True)
