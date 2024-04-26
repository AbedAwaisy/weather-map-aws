// script.js

document.addEventListener("DOMContentLoaded", function() {
    var map = L.map('map').setView([31.276559, 34.797594], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    function fetchWeatherData(latitude, longitude, timeRange) {
        console.log("Fetching weather data for coordinates:", latitude, longitude, "Time Range:", timeRange);
        fetch('/get_weather', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ latitude: latitude, longitude: longitude, timeRange: timeRange })
        })
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok.');
            return response.json();
        })
        .then(data => {
            console.log("Weather data received:", data);
            displayWeatherData(data);
        })
        .catch(error => {
            console.error('Error fetching weather data:', error);
            document.getElementById("weatherDataDisplay").innerHTML = `<p class="error">Failed to load data: ${error.message}</p>`;
        });
    }

    // Function to update the display of graphs
    function updateGraphs() {
        var d = new Date();  // Create a new Date object to get the current time
        var n = d.getTime(); // Use the timestamp to prevent caching issues

        // Get the elements by their IDs and update their 'src' attributes
        var tempGraph = document.getElementById("temperature_plot");
        var windGraph = document.getElementById("wind_plot");
        var rainGraph = document.getElementById("rain_plot");

        // Update the image sources
        tempGraph.src = '/temperature_plot.png?time=' + n;
        windGraph.src = '/wind_plot.png?time=' + n;
        rainGraph.src = '/rain_plot.png?time=' + n;

        // Update the links for new tabs
        tempGraph.parentNode.href = '/temperature_plot.png?time=' + n;
        windGraph.parentNode.href = '/wind_plot.png?time=' + n;
        rainGraph.parentNode.href = '/rain_plot.png?time=' + n;
    }

    // Make sure to call updateGraphs() function after the data is displayed
    function displayWeatherData(data) {
        var weatherDisplay = document.getElementById("weatherDataDisplay");
        weatherDisplay.innerHTML = ''; // Clear previous content

        if (data.list && data.list.length) {
            let lastDisplayedDate = "";

            data.list.forEach(function(forecast) {
                const forecastDateTime = new Date(forecast.dt_txt);
                const forecastDate = forecastDateTime.toLocaleDateString();
                const temp = forecast.main.temp;
                const description = forecast.weather[0].description;
                const iconCode = forecast.weather[0].icon;
                const iconUrl = `http://openweathermap.org/img/wn/${iconCode}.png`;

                if (forecastDate !== lastDisplayedDate) {
                    lastDisplayedDate = forecastDate;
                    const dateHeader = document.createElement('div');
                    dateHeader.className = 'day-title';
                    dateHeader.textContent = forecastDate;
                    weatherDisplay.appendChild(dateHeader);
                }

                const block = document.createElement('div');
                block.className = 'forecast-block';
                block.innerHTML = `
                    <div class="forecast-date">${forecastDateTime.toLocaleString()}</div>
                    <div class="forecast-icon"><img src="${iconUrl}" alt="${description}"></div>
                    <div class="forecast-temp">${temp.toFixed(1)}°C</div>
                    <div class="forecast-desc">${description}</div>
                `;
                weatherDisplay.appendChild(block);
            });
        } else {
            weatherDisplay.innerHTML = '<p>No weather data available.</p>';
        }
        updateGraphs(); // Update graphs after displaying weather data
    }


    map.on('click', function(e) {
        document.getElementById("latitudeInput").value = e.latlng.lat.toFixed(4);
        document.getElementById("longitudeInput").value = e.latlng.lng.toFixed(4);
    });

    document.getElementById("locationForm").addEventListener("submit", function(event) {
        event.preventDefault();
        const latitude = document.getElementById("latitudeInput").value;
        const longitude = document.getElementById("longitudeInput").value;
        const timeRange = document.getElementById("timeRange").value;

        if (!latitude || !longitude) {
            alert("Please ensure latitude and longitude are entered.");
        } else {
            fetchWeatherData(latitude, longitude, timeRange);
        }
    });
});
