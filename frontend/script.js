// script.js

document.addEventListener("DOMContentLoaded", function() {
    // Initialize the Leaflet map
    var map = L.map('map').setView([31.276559, 34.797594], 13);  // Adjust center and zoom level as needed

    // Add OpenStreetMap tiles to the map
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // Function to fetch weather data
    function fetchWeatherData(latitude, longitude) {
        console.log("Fetching weather data for coordinates:", latitude, longitude);
        fetch('/get_weather', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ latitude: latitude, longitude: longitude })
        })
        .then(response => response.json())
        .then(data => {
            // Process and display data
            displayWeatherData(data);
            console.log("Weather data:", data);
        })
        .catch(error => {
            console.error('Error fetching weather data:', error);
        });
    }

    // Function to display weather data
    function displayWeatherData(data) {
        var weatherDisplay = document.getElementById("weatherDataDisplay");
        weatherDisplay.innerHTML = ''; // Clear previous content

        if (data.list && data.list.length) {
            data.list.forEach(function(forecast) {
                const dateTime = new Date(forecast.dt_txt).toLocaleString();
                const temp = forecast.main.temp;
                const description = forecast.weather[0].description;
                const iconCode = forecast.weather[0].icon;
                const iconUrl = `http://openweathermap.org/img/wn/${iconCode}.png`;

                const block = document.createElement('div');
                block.className = 'forecast-block';
                block.innerHTML = `
                    <div class="forecast-date">${dateTime}</div>
                    <div class="forecast-icon"><img src="${iconUrl}" alt="${description}"></div>
                    <div class="forecast-temp">${temp.toFixed(1)}°C</div>
                    <div class="forecast-desc">${description}</div>
                `;
                weatherDisplay.appendChild(block);
            });
        } else {
            weatherDisplay.innerHTML = '<p>No weather data available.</p>';
        }
        var temperatureGraph = document.getElementById("temperatureGraph");
        temperatureGraph.src = '/temperature_plot.png';  // Update the src attribute to the new plot URL
    }

    // Update input fields on map click
    map.on('click', function(e) {
        var lat = e.latlng.lat;
        var lng = e.latlng.lng;
        document.getElementById("latitudeInput").value = lat.toFixed(4);
        document.getElementById("longitudeInput").value = lng.toFixed(4);
    });

    // Function to display predictions
    function displayPredictions() {
        console.log("Displaying predictions...");
        // Placeholder function for displaying predictions
        // Replace this with actual implementation
    }


    // Event listener for form submission
    document.getElementById("locationForm").addEventListener("submit", function(event) {
        event.preventDefault(); // Prevent form submission
        var latitude = document.getElementById("latitudeInput").value;
        var longitude = document.getElementById("longitudeInput").value;
        fetchWeatherData(latitude, longitude);
    });

    // document.getElementById("displayPredictionsBtn").addEventListener("click", function() {
    //     displayPredictions();
    // });
});
