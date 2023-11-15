import requests
import os
from flask import Flask, request, render_template, jsonify


app = Flask(__name__)
OpenWeatherMap_api_key = os.environ.get("OPENWEATHERMAP_API_KEY")


@app.route("/")
def index():
    user_ip = request.remote_addr  # ユーザーの IP アドレスを取得
    location_info = get_location_info(user_ip)  # 位置情報を取得

    if location_info:
        weather_info = get_weather_from_location(
            location_info["latitude"],
            location_info["longitude"],
            OpenWeatherMap_api_key,
        )
        weather_info["main"]["temp"] = kelvin_to_celsius(weather_info["main"]["temp"])
        weather_info["main"]["feels_like"] = kelvin_to_celsius(
            weather_info["main"]["feels_like"]
        )
        return render_template(
            "weather.html",
            # ip=user_ip,
            location=location_info["countryName"],
            weather=weather_info["main"],
            clouds=weather_info["clouds"],
            weather_main=weather_info["weather"][0]["main"],
            weather_description=weather_info["weather"][0]["description"],
            wind=weather_info["wind"],
            rain=weather_info.get("rain"),
        )

    else:
        return "位置情報の取得に失敗しました。"


def get_location_info(ip_address):
    # FreeIP API を利用してIPから位置情報を取得
    response = requests.get(f"https://freeipapi.com/api/json/{ip_address}")
    if response.status_code == 200:
        return response.json()
    else:
        return None


@app.route("/location", methods=["POST"])
def location():
    data = request.json
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    # GeolocationAPIからのデータが提供された場合はそれを使用
    if latitude is not None and longitude is not None:
        weather_info = get_weather_from_location(
            latitude, longitude, OpenWeatherMap_api_key
        )
        return jsonify(weather_info)

    # GeolocationAPIからのデータがない場合は、IPアドレスから位置情報を取得
    user_ip = request.remote_addr  # ユーザーのIPアドレスを取得
    location_info = get_location_info(user_ip)  # IPから位置情報を取得
    if location_info:
        latitude = location_info["latitude"]
        longitude = location_info["longitude"]
        weather_info = get_weather_from_location(
            latitude, longitude, OpenWeatherMap_api_key
        )
        weather_info["main"]["temp"] = kelvin_to_celsius(weather_info["main"]["temp"])
        weather_info["main"]["feels_like"] = kelvin_to_celsius(
            weather_info["main"]["feels_like"]
        )
        return jsonify(weather_info)
    else:
        return jsonify({"error": "位置情報の取得に失敗しました。"})


def get_weather_from_location(latitude, longitude, api_key):
    # OpenWeatherMap API を使用してIPの天気予報を取得
    weather_url = (
        f"http://api.openweathermap.org/data/2.5/weather?"
        f"lat={latitude}&lon={longitude}&appid={api_key}&lang=ja"
    )
    response = requests.get(weather_url)
    return response.json()


def kelvin_to_celsius(kelvin_temp):
    return kelvin_temp - 273.15


if __name__ == "__main__":
    app.run()
