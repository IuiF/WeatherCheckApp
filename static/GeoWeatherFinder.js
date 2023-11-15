function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(sendPosition, showError);
    } else {
        console.log("このブラウザではGeolocationがサポートされていません.");
    }
}

function sendPosition(position) {
    fetch('/location', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            latitude: position.coords.latitude,
            longitude: position.coords.longitude
        })
    })
    .then(response => response.json())
    .then(data => {
        updateWeatherInfo(data);
    });
}

function showError(error) {
    console.log(`Geolocation error: ${error.message}`);
    fetch('/ip_weather')
    .then(response => response.json())
    .then(data => {
        updateWeatherInfo(data);
    });
}


function updateWeatherInfo(data) {
    document.getElementById('location').textContent = `${data.name} の天気情報`;
    document.getElementById('temperature').textContent = `${(data.main.temp- 273.15).toFixed(1)} °C`;
    document.getElementById('feels_like').textContent = `${(data.main.feels_like - 273.15).toFixed(1)} °C`;
    document.getElementById('humidity').textContent = `${data.main.humidity}%`;
    document.getElementById('pressure').textContent = `${data.main.pressure} hPa`;
    document.getElementById('clouds').textContent = `${data.clouds.all}%`;
    document.getElementById('weather_main').textContent = data.weather[0].main;
    document.getElementById('weather_description').textContent = data.weather[0].description;
    document.getElementById('wind_speed').textContent = `${data.wind.speed} m/s`;
    document.getElementById('wind_deg').textContent = `${data.wind.deg} 度`;
    if (data.rain) {
        document.getElementById('rain').style.display = 'block';
        document.getElementById('rain_amount').textContent = `${data.rain['1h']} mm`;
    } else {
        document.getElementById('rain').style.display = 'none';
    }
}
