import requests
import matplotlib  # Ensure this is at the top
matplotlib.use('Agg')  # Set the backend before importing pyplot
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from config import API_KEY
import boto3
import json


class WeatherData:
    def __init__(self):
        self.api_key = API_KEY
        self.base_url = "http://api.openweathermap.org/data/2.5/forecast"
        self.lambda_client = boto3.client('lambda')

    def get_weather_data(self, latitude, longitude, time_range):
        api_url = f"{self.base_url}?lat={latitude}&lon={longitude}&appid={self.api_key}&units=metric"
        response = requests.get(api_url)
        weather_data = response.json()

        filtered_data = self.filter_data_by_time_range(weather_data, time_range)
        self.create_temperature_graph(filtered_data)
        self.create_wind_graph(filtered_data)
        self.create_rain_graph(filtered_data)

        return filtered_data

    def filter_data_by_time_range(self, data, time_range):
        if time_range == 'next5days':
            return data

        filtered_list = []
        current_date = datetime.now().date()
        day_offset = 1 if time_range == 'tomorrow' else 0
        target_date = (current_date + timedelta(days=day_offset)).strftime('%Y-%m-%d')

        for forecast in data['list']:
            forecast_date = forecast['dt_txt'].split(' ')[0]
            if forecast_date == target_date:
                filtered_list.append(forecast)

        return {'list': filtered_list}

    def create_temperature_graph(self, weather_data):
        dates = [entry['dt_txt'] for entry in weather_data['list']]
        temperatures = [entry['main']['temp'] for entry in weather_data['list']]

        plt.figure(figsize=(10, 5))
        plt.plot(dates, temperatures, marker='o', linestyle='-', color='b')
        plt.title('Temperature Forecast')
        plt.xlabel('Date and Time')
        plt.ylabel('Temperature (°C)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('static/temperature_plot.png')
        plt.close()

    def create_wind_graph(self, weather_data):
        dates = [entry['dt_txt'] for entry in weather_data['list']]
        wind_speeds = [entry['wind']['speed'] for entry in weather_data['list']]

        plt.figure(figsize=(10, 5))
        plt.plot(dates, wind_speeds, marker='o', linestyle='-', color='g')
        plt.title('Wind Speed Forecast')
        plt.xlabel('Date and Time')
        plt.ylabel('Wind Speed (m/s)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('static/wind_plot.png')
        plt.close()

    def create_rain_graph(self, weather_data):
        dates = [entry['dt_txt'] for entry in weather_data['list']]
        rain_volumes = [entry.get('rain', {}).get('3h', 0) for entry in weather_data['list']]

        plt.figure(figsize=(10, 5))
        plt.bar(dates, rain_volumes, color='b')
        plt.title('Rain Volume Forecast')
        plt.xlabel('Date and Time')
        plt.ylabel('Rain Volume (mm)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('static/rain_plot.png')
        plt.close()

    def save_location(self, data):
        location_name = data['locationName']
        self.save_location_to_text(location_name)

        try:
            response = self.lambda_client.invoke(
                FunctionName='SaveWeatherLocation',
                InvocationType='RequestResponse',
                Payload=json.dumps(data)
            )
            response_payload = response['Payload'].read()
            return json.loads(response_payload), response['StatusCode']
        except Exception as e:
            return {"message": f"Failed to invoke Lambda function: {str(e)}"}, 500

    def save_location_to_text(self, location_name):
        file_path = 'locations.txt'
        try:
            with open(file_path, 'a') as file:
                file.write(location_name + '\n')
        except Exception as e:
            print(f"Failed to save location to text file: {str(e)}")

    def get_locations(self):
        file_path = 'locations.txt'
        try:
            with open(file_path, 'r') as file:
                locations = file.readlines()
            return [location.strip() for location in locations]
        except FileNotFoundError:
            return []

    def get_location_data(self, location_name):
        try:
            response = self.lambda_client.invoke(
                FunctionName='FetchWeatherLocationData',
                InvocationType='RequestResponse',
                Payload=json.dumps({'locationName': location_name})
            )
            response_payload = json.loads(response['Payload'].read())
            return response_payload, 200
        except Exception as e:
            return {"message": f"Failed to retrieve location data: {str(e)}"}, 500
