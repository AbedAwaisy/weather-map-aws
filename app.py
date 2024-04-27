import boto3
from flask import Flask, render_template, request, jsonify, send_from_directory, json
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

@app.route('/save_location', methods=['POST'])
def save_location():
    data = request.get_json()
    print("Received location data:", data)

    # Create a boto3 client for the Lambda service
    lambda_client = boto3.client('lambda')
    save_location_to_text(data['locationName'])
    try:
        # Invoking the Lambda function
        response = lambda_client.invoke(
            FunctionName='SaveWeatherLocation',  # Replace with your Lambda function name
            InvocationType='RequestResponse',
            Payload=json.dumps(data)  # Convert the dictionary to a JSON string
        )
        # Read the response from Lambda
        response_payload = response['Payload'].read()
        return jsonify(json.loads(response_payload)), response['StatusCode']
    except Exception as e:
        print(f"Error invoking Lambda function: {str(e)}")
        return jsonify({"message": "Failed to invoke Lambda function"}), 500

def save_location_to_text(location_name):
    # Specify the path to your file
    file_path = 'locations.txt'
    try:
        # Open the file in append mode
        with open(file_path, 'a') as file:
            # Write the location name followed by a newline
            file.write(location_name + '\n')
    except Exception as e:
        print(f"Failed to save location to text file: {str(e)}")

@app.route('/get_locations', methods=['GET'])
def get_locations():
    file_path = 'locations.txt'
    try:
        with open(file_path, 'r') as file:
            locations = file.readlines()
        # Remove newline characters
        locations = [location.strip() for location in locations]
        return jsonify(locations)
    except FileNotFoundError:
        return jsonify([]), 200

@app.route('/get_location_data', methods=['POST'])
def get_location_data():
    data = request.get_json()
    location_name = data.get('locationName')

    # Assume lambda_client is already defined and configured
    try:
        # Invoking the Lambda function to get data for a specific location
        lambda_client = boto3.client('lambda')

        response = lambda_client.invoke(
            FunctionName='FetchWeatherLocationData',
            InvocationType='RequestResponse',
            Payload=json.dumps({'locationName': location_name})
        )
        response_payload = json.loads(response['Payload'].read())
        return jsonify(response_payload), 200
    except Exception as e:
        print(f"Error invoking Lambda function: {str(e)}")
        return jsonify({"message": "Failed to retrieve location data"}), 500

if __name__ == '__main__':
    app.run(debug=True)
