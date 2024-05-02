# Project Overview

Weather Data Logger is a web application that displays and logs weather data for various locations using real-time data fetched from the OpenWeatherMap API. Users can select a location interactively on a map, fetch weather data for that location, and visualize the data through graphs generated using matplotlib. The application also supports saving favorite locations to AWS DynamoDB and retrieving them for quick access.

## Technologies and Functionalities

- **Frontend:** HTML, CSS, JavaScript integrated with Leaflet.js for interactive maps.
- **Backend:** Python Flask serves the backend API that interacts with OpenWeatherMap and AWS services. Data visualization is handled by matplotlib to generate static graph images.
- **AWS Lambda:** Utilizes two Lambda functions (SaveWeatherLocation and FetchWeatherLocationData) for handling data storage and retrieval from AWS DynamoDB.
- **AWS DynamoDB:** Used to store location data persistently.
- **IAM Configuration:** Proper IAM roles are configured for secure AWS service access.
- **boto3:** Python library used for interfacing with AWS services.
- **OpenWeatherMap API:** Fetches real-time weather data.

## Setup Instructions

### Environment Setup and Dependencies

1. Clone the repository:

   ```bash
   git clone https://github.com/AbedAwaisy/weather-map-aws.git
   cd weather-map-aws
   ```

2. Install dependencies:

   Ensure Python 3.6+ is installed, then set up a virtual environment and install the required packages:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

### AWS Configuration

1. **Lambda Functions:** Ensure SaveWeatherLocation and FetchWeatherLocationData functions are set up in AWS Lambda. (Both lambda functions code can be found as zipped files under "lambda_zips" directory)
2. **DynamoDB:** Set up a DynamoDB table to store location data. Create a simple table with this schema:
   - locationName(String,PK)
   - latitude(Numeric)
   - longitude(Numeric)
   - timeRange(String)
3. **IAM Roles:** If you are not working with root user, create an IAM role with permissions to access Lambda and DynamoDB. Attach policies that allow invoking Lambda functions and reading/writing to DynamoDB.
4. **AWS Client:** Set up boto3 in your local development environment to interact with AWS services.

   To configure AWS CLI with `aws configure`, follow these steps:
   - Install AWS CLI if not already installed.
   - Open terminal or command prompt.
   - Run `aws configure` command.
   - Enter your AWS Access Key ID, Secret Access Key, default region name, and default output format as prompted.

### OpenWeatherMap API Key

Obtain an API key from OpenWeatherMap and configure it within your application, replace it with the placeholder in "config.py" file.

## Usage Guide

### Running the Project

Start the Flask server locally:

```bash
python app.py
```

Navigate to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your web browser to access the application.

### Interacting with the Service

- **View Weather Data:** Click on the map to choose a location, select a time range, and submit to view weather data along with generated graphs.
- **Save Locations:** Enter a location name and click 'Save Location' to store it in AWS DynamoDB.
- **Fetch Saved Locations:** Use the dropdown to select a saved location and view its stored data.
- **View Graphs:** Click on graphs to view them in full size in new tab.

## API Testing with Postman

To test the API functionality, you can set up Postman:

- Set up a GET request to your local server's endpoint ('127.0.0.1:5000/'). This should return the index.html file.

## AWS Free Tier Usage and Billing Alerts

Be mindful of AWS Free Tier limits. Set up billing alerts in AWS Budgets to receive notifications when usage approaches your budget threshold.

1. Navigate to AWS Budgets.
2. Create a new budget with a type 'Cost budget'.
3. Set the alert threshold (e.g., $0.10) to get notifications on crossing this limit.