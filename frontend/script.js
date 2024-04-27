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
            let dayContainer = null;

            data.list.forEach(function(forecast) {
                const forecastDateTime = new Date(forecast.dt_txt);
                const forecastDate = forecastDateTime.toLocaleDateString();
                const temp = forecast.main.temp;
                const description = forecast.weather[0].description;
                const iconCode = forecast.weather[0].icon;
                const iconUrl = `http://openweathermap.org/img/wn/${iconCode}.png`;

                if (forecastDate !== lastDisplayedDate) {
                    lastDisplayedDate = forecastDate;
                    dayContainer = document.createElement('div');
                    dayContainer.className = 'day-container';

                    const dateHeader = document.createElement('div');
                    dateHeader.className = 'day-title';
                    dateHeader.textContent = forecastDate;
                    dayContainer.appendChild(dateHeader);

                    weatherDisplay.appendChild(dayContainer);
                }

                const block = document.createElement('div');
                block.className = 'forecast-block';
                block.innerHTML = `
                    <div class="forecast-date">${forecastDateTime.toLocaleString()}</div>
                    <div class="forecast-icon"><img src="${iconUrl}" alt="${description}"></div>
                    <div class="forecast-temp">${temp.toFixed(1)}°C</div>
                    <div class="forecast-desc">${description}</div>
                `;
                dayContainer.appendChild(block);
            });
        } else {
            weatherDisplay.innerHTML = '<p>No weather data available.</p>';
        }
        updateGraphs(); // Update graphs after displaying weather data
    }

    // This function will be called when the 'Save Location' button is clicked
    function saveLocation() {
        const latitude = document.getElementById("latitudeInput").value;
        const longitude = document.getElementById("longitudeInput").value;
        const locationName = document.getElementById("locationName").value;
        const timeRange = document.getElementById("timeRange").value;

        if (!latitude || !longitude || !locationName) {
            alert("Please ensure all fields are filled out correctly.");
            return;
        }

        // Prepare data to be sent to the backend
        const locationData = {
            latitude,
            longitude,
            locationName,
            timeRange
        };

        // Send data to the backend using POST request
        fetch('/save_location', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(locationData)
        })
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok.');
            return response.json();
        })
        .then(data => {
            console.log("Location saved successfully:", data);
            alert("Location saved successfully!");
        })
        .catch(error => {
            console.error('Error saving location:', error);
            alert(`Failed to save location: ${error.message}`);
        });
    }

    function fetchLocations() {
        fetch('/get_locations')
        .then(response => response.json())
        .then(locations => {
            const select = document.getElementById('locationList');
            // Clear existing options, remove this line if you want to keep the 'My Home' option
            select.innerHTML = '';
            locations.forEach(location => {
                const option = document.createElement('option');
                option.value = location;
                option.textContent = location;
                select.appendChild(option);
            });
        })
        .catch(error => console.error('Error fetching locations:', error));
    }
    // Function to handle fetching location data
    function fetchLocationData() {
        const locationName = document.getElementById('locationList').value;
        if (!locationName) {
            alert('Please select a location.');
            return;
        }

        // Send the request to the backend with the selected location name
        fetch('/get_location_data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ locationName: locationName })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Location data received:', data);
            const locationData = JSON.parse(data.body);
            console.log('Parsed location data:', locationData);
            populateFields(locationData.latitude, locationData.longitude, locationData.timeRange, locationData.locationName);
            fetchWeatherData(locationData.latitude, locationData.longitude, locationData.timeRange);
        })
        .catch(error => console.error('Error fetching location data:', error));
    }

    // Event listener for the Fetch Location button
    document.getElementById('fetchLocationBtn').addEventListener('click', fetchLocationData);
    // Call fetchLocations to populate the dropdown on page load
    fetchLocations();
    function populateFields(latitude, longitude, timeRange, locationName) {
    // Get the input fields from the DOM
        const latitudeInput = document.getElementById('latitudeInput');
        const longitudeInput = document.getElementById('longitudeInput');
        const timeRangeSelect = document.getElementById('timeRange');
        const locationNameInput = document.getElementById('locationName'); // Assuming this input exists

        // Set the values of the input fields
        latitudeInput.value = latitude;
        longitudeInput.value = longitude;
        timeRangeSelect.value = timeRange;
        locationNameInput.value = locationName; // This assumes you have a field for location name

        console.log(`Fields populated: Latitude=${latitude}, Longitude=${longitude}, TimeRange=${timeRange}, LocationName=${locationName}`);
    }



    map.on('click', function(e) {
        document.getElementById("latitudeInput").value = e.latlng.lat.toFixed(4);
        document.getElementById("longitudeInput").value = e.latlng.lng.toFixed(4);
    });
    document.getElementById('saveLocationBtn').addEventListener('click', saveLocation);


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
