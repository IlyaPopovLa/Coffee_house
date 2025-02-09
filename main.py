import json
import requests
import os
from geopy import distance
from pprint import pprint
from dotenv import load_dotenv


load_dotenv()
apikey=os.getenv('API_KEY')


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


def my_distance(coords):
    coffee_shops = []
    with open("coffee.json", "r", encoding="CP1251") as my_file:
        file_contents = my_file.read()
    contents_list = json.loads(file_contents)
    for data in contents_list:
        data_coffees = distance.distance(coords, (data['Longitude_WGS84'], data['Longitude_WGS84'])).km
        coffee_shop = {
        "title": data['Name'],
        "distance": data_coffees,
        "longitude": data['Longitude_WGS84'],
        "latitude": data['Latitude_WGS84']
        }
        coffee_shops.append(coffee_shop)
    return coffee_shops


def min_distance(coords):
    coffee_shops = []
    coordinate = my_distance(coords)
    for shop in coordinate:
        coffee_shops.append(shop['distance'])
    min_distance = min(coffee_shops)
    closest_coffee_shop = [shop for shop in coordinate if shop['distance'] == min_distance][0]
    return closest_coffee_shop


def main():
    point = input("Ваше местоположение?")
    coords = fetch_coordinates(apikey, point)
    print("Ваши координаты:", coords)
    closest_shop = min_distance(coords)
    pprint(closest_shop)


if __name__ == '__main__':
    main()