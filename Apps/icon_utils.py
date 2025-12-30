def get_icon_url(icon_name):
    base_url = "https://raw.githubusercontent.com/visualcrossing/WeatherIcons/main/SVG/1st%20Set%20-%20Color/"
    mapping = {
        'clear-day': 'clear-day.svg',
        'clear-night': 'clear-night.svg',
        'partly-cloudy-day': 'partly-cloudy-day.svg',
        'partly-cloudy-night': 'partly-cloudy-night.svg',
        'cloudy': 'cloudy.svg',
        'rain': 'rain.svg',
        'showers-day': 'rain.svg',
        'showers-night': 'rain.svg',
        'thunder-rain': 'thunderstorm.svg',
        'thunder-showers-day': 'thunderstorm.svg',
        'thunder-showers-night': 'thunderstorm.svg',
        'snow': 'snow.svg',
        'fog': 'fog.svg',
        'wind': 'wind.svg'
    }
    return base_url + mapping.get(icon_name, 'clear-day.svg')
