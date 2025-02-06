import json
import requests
from geopy import distance
from pprint import pprint


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


apikey = 
point = input("Ваше местоположение?")
coords = fetch_coordinates(apikey, point)


def my_distance():
    with open("coffee.json", "r", encoding="CP1251") as my_file:
        file_contents = my_file.read()
    contents_list = json.loads(file_contents)
    for data in contents_list:
        distance_my = (distance.distance(coords, (data['Longitude_WGS84'], data['Longitude_WGS84'])).km)
        coffee_list = {
        "title": data['Name'],
        "distance": distance_my,
        "longitude": data['Longitude_WGS84'],
        "latitude": data['Latitude_WGS84']
        }
        pprint(coffee_list, sort_dicts=False)

def min_distance():
    coordinate = my_distance()
    return coordinate['distance']


def main():
    print("Ваши координаты:", coords)
    print(min_distance())


if __name__ == '__main__':
    main()