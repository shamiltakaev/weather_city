from app import app
from flask import render_template
from app.forms import SearchForm
import datetime
import requests

city = "Аргун" # input()

def get_weather(city):
    url_to_coords = f"https://geocode-maps.yandex.ru/1.x?apikey=a51286fd-602b-4dc7-a21a-7594bf3786d6&geocode={city}&format=json"

    req = requests.get(url_to_coords).json()

    latit, longt = req['response']['GeoObjectCollection']['featureMember'][0]["GeoObject"]["Point"]["pos"].split()

    url = f"https://api.open-meteo.com/v1/forecast?latitude={latit}&longitude={longt}&hourly=temperature_2m"
    request = requests.get(url)

    # print(request.json()["hourly"]["temperature_2m"]
    #     [datetime.datetime.now().hour-1])
    # print(request.json()["hourly"]["temperature_2m"])
    items = []
    for temp, date in zip(request.json()["hourly"]["temperature_2m"], request.json()["hourly"]["time"]):
        items.append(
            {
                "time": datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M").strftime("%d.%m.%Y-%H:%M"),
                "temp": temp
                }
                )
        # print(datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M").strftime("%d.%m.%Y-%H:%M"), temp)
    return items
    # d = datetime.datetime.strptime(request.json()["hourly"]["time"][0], "%Y-%m-%dT%H:%M")
    # print(d.strftime("%d/%m/%Y"))

# get_weather(city)

@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
def index():
    form = SearchForm()
    items = []
    if form.validate_on_submit():
        items = get_weather("Аргун")
        now_time = items[datetime.datetime.now().hour]["temp"]
    return render_template("index.html", items=items, now_time=now_time, form=form)