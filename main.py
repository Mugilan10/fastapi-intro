from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id":item_id, "name":"Sample Item"} 

@app.get("/weather/{city}")
def get_weather(city:str):
    try:
        response = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1")
        geo_data = response.json()
        if "results" not in geo_data:
            return("City not found")
        latitude = geo_data["results"][0]["latitude"]
        longitude = geo_data["results"][0]["longitude"]
        response2 = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true")
        weather_data = response2.json()
        temp = weather_data["current_weather"]["temperature"]
        wind = weather_data["current_weather"]["windspeed"]
        return {"city": city, "temperature": temp, "windspeed":wind}
    except requests.exceptions.ConnectionError:
        return("Connection error")