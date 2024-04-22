// script.js

document.addEventListener("DOMContentLoaded", function() {
    // Function to fetch weather data
    function fetchWeatherData(location) {
        console.log("Fetching weather data for location:", location);
        fetch('/get_weather', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ location: location })
        })
        .then(response => response.json())
        .then(data => {
            // Process and display data (to be implemented)
            displayWeatherData(data);
            console.log("Weather data:", data);
        })
        .catch(error => {
            console.error('Error fetching weather data:', error);
        });
    }
    // Function to display weather data
    function displayWeatherData(data) {
        // Assuming 'data' contains weather information in a suitable format
        // Display the weather data in the weatherDataDisplay div
        var weatherDisplay = document.getElementById("weatherDataDisplay");
        weatherDisplay.innerHTML = "<pre>" + JSON.stringify(data, null, 2) + "</pre>";
    }
    // Function to display predictions
    function displayPredictions() {
        console.log("Displaying predictions...");
        // Placeholder function for displaying predictions
        // Replace this with actual implementation
    }

    // Event listeners
    document.getElementById("locationForm").addEventListener("submit", function(event) {
        event.preventDefault(); // Prevent form submission
        fetchWeatherData(document.getElementById("locationInput").value);
    });

    document.getElementById("fetchDataBtn").addEventListener("click", function() {
        fetchWeatherData(document.getElementById("locationInput").value);
    });

    document.getElementById("displayPredictionsBtn").addEventListener("click", function() {
        displayPredictions();
    });
});
