import requests
import datetime

def get_weather_forecast():
    api_key = 'YOUR_API_KEY'  # Replace with your OpenWeatherMap API key
    city = 'Matsuyama'
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={api_key}'

    response = requests.get(url)
    data = response.json()
    
    if response.status_code == 200:
        # Get tomorrow's date
        tomorrow_date = (datetime.datetime.now() + datetime.timedelta(days=1)).date()

        # Extract weather forecast for tomorrow
        for forecast in data['list']:
            forecast_date = datetime.datetime.fromtimestamp(forecast['dt']).date()
            if forecast_date == tomorrow_date:
                weather_description = forecast['weather'][0]['description']
                temperature = forecast['main']['temp']
                print(f"Date: {forecast_date}, Weather: {weather_description}, Temperature: {temperature}°C")
                break
    else:
        print("Failed to get data from OpenWeatherMap API.")

get_weather_forecast()
