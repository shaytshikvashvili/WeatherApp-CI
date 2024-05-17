from flask import Flask, render_template, request
import requests

app = Flask(__name__)


def get_weather(location):
    API_URL = "http://api.weatherapi.com/v1/forecast.json"
    API_KEY = "5df4e04e275c4861a6584634231506"

    params = {"q": location, "key": API_KEY, "days": 7}

    response = requests.get(API_URL, params=params)
    data = response.json()

    if response.status_code == 200:

        forecast_data = {"location": data["location"]["name"], "country": data["location"]["country"]}

        for day in data["forecast"]["forecastday"]:
            date = day['date']
            max_temp_c = day['day']['maxtemp_c']
            min_temp_c = day['day']['mintemp_c']
            avg_humidity = day['day']['avghumidity']

            forecast_data[date] = {"max_temp_c": f"{max_temp_c}°C", "min_temp_c": f"{min_temp_c}°C", "avg_humidity": f"{avg_humidity}%"}

        return forecast_data
    else:
        return None


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/weather', methods=['POST'])
def weather():
    location = request.form["location"]
    weather_info = get_weather(location)

    if not weather_info:
        error_message = "Failed to retrieve weather information for the specified location."
        return render_template("index.html", error=error_message)

    return render_template("weather.html", weather=weather_info)


if __name__ == '__main__':
    app.run(host="0.0.0.0")
