import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
Api_key=os.getenv("openweather_api")
historyfile="your_history.json"

def view_your_history():
    if not os.path.exists(historyfile):
        print("No history found.")
        return
    try:
        with open(historyfile, "r") as file:
            history= json.load(file)
    except:
        print("Error reading history.")
        return

    print("SEARCH HISTORY (LAST 5)")
    for search_history in history:
        print(search_history["city"], ", ", search_history["country"], " - ", search_history["temp"], "°C, ", search_history["cond"], " (AQI: ", search_history["aqi"], ")")



def weather():
    city_name = input("Enter the city name : ")
    whether = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city_name, "appid": Api_key, "units": "metric"}


    try:
        response = requests.get(whether, params=params)
        if response.status_code == 404:
            print("City does not exist.\n")
            return
        if response.status_code != 200:
            print("Could not get the Data.\n")
            return
        whether_data= response.json()
    except:
        print("Internet Issue.\n")
        return

    latitude = whether_data.get("coord", {}).get("lat")
    longitude = whether_data.get("coord", {}).get("lon")
    name= whether_data.get("name")
    country= whether_data.get("sys", {}).get("country")
    temperature= whether_data.get("main", {}).get("temp")
    feels= whether_data.get("main", {}).get("feels_like")
    humidity= whether_data.get("main", {}).get("humidity")
    wind_speed= whether_data.get("wind", {}).get("speed", 0) * 3.6 
    condition= whether_data.get("weather", [{}])[0].get("description", "N/A")

    aqi_url= "https://api.openweathermap.org/data/2.5/air_pollution"
    aqi_params= {"lat": latitude, "lon": longitude, "appid": Api_key}

    try:
        response2= requests.get(aqi_url, params=aqi_params)
        aqi_data= response2.json()
        aqi= aqi_data.get("list", [{}])[0].get("main", {}).get("aqi")
    except:
        print("Error in AQI data.\n")
        return
    
    public_advisory= ""
    if(aqi == 1): public_advisory= "Satisfactory"
    elif(aqi == 2): public_advisory= "Fair, Neither too good nor too bad."
    elif(aqi == 3): public_advisory= "Moderate. Sensitive individuals should reduce outdoor activity."
    elif(aqi == 4): public_advisory= "Poor, Try staying Indoor while you can."
    elif(aqi == 5): public_advisory= "Very Poor, Do not go outside unless compulsory."

    print("\n\n\nWeather in ", name, ", ", country)
    print("Temperature: ", temperature, "°C (Feels like ", feels, "°C)")
    print("Humidity: ", humidity, "%")
    print("Wind Speed: ", round(wind_speed, 1), " km/h")
    print("Condition: ", condition)
    print("Air Quality Index: ", aqi)
    print("Advisory: ", public_advisory)

    history= []
    if os.path.exists(historyfile):
        try:
            with open(historyfile, "r") as file:
                history= json.load(file)
        except:
            history= []

    record= {
        "city": name,
        "country": country,
        "temp": temperature,
        "cond": condition,
        "aqi": aqi
    }

    history.insert(0, record)
    if len(history) > 5:
        history= history[:5]

    with open(historyfile, "w") as file:
        json.dump(history, file, indent=4)


def main():
    while True:
        print("\nWEATHER DASHBOARD")
        print("1. Search city weather")
        print("2. View search history")
        print("3. Exit")
        
        choice= input("Select an option: ")
        
        if choice =="1": weather()
        elif choice =="2": view_your_history()
        elif choice =="3": 
            print("Bye ,See you again.")
            break   

if __name__== "__main__":
    main()


