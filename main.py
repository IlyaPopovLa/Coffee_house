import json
import requests
import os
import folium
from geopy import distance
from pprint import pprint
from dotenv import load_dotenv


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
    return lat, lon


def my_distance(coords):
    coffee_shops = []
    with open("coffee.json", "r", encoding="CP1251") as my_file:
        file_contents = my_file.read()
    contents_list = json.loads(file_contents)
    for data in contents_list:
        shop_coords = (data['Latitude_WGS84'], data['Longitude_WGS84'])
        distance_to_shop = distance.distance(coords, shop_coords).km
        coffee_shop = {
        "title": data['Name'],
        "distance": distance_to_shop,
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
    distance_coffee_shops = min(coffee_shops)
    closest_coffee_shop = [shop for shop in coordinate if shop['distance'] == distance_coffee_shops]
    return closest_coffee_shop


def first_coffee_shops(coords):
    coffee_shops = my_distance(coords)
    sorted_shops = sorted(coffee_shops, key=lambda shop: shop['distance'])
    return sorted_shops[:5]


def save_map(coords):
    coffee_shops = first_coffee_shops(coords)
    my_map = folium.Map(
        location = coords,
        zoom_start = 12,
    )
    for shop in coffee_shops:
        folium.Marker(
            location = coords,
            popup = "Вы тут",
            icon = folium.Icon(color="red")
        ).add_to(my_map)

        folium.Marker(
            location = [shop['latitude'], shop['longitude']],
            popup = shop['title'],
            icon = folium.Icon(color="green")
        ).add_to(my_map)
    my_map.save("map.html")


def main():
    load_dotenv()
    apikey = os.getenv('API_KEY')
    point = input("Ваше местоположение?")
    coords = fetch_coordinates(apikey, point)
    print("Ваши координаты:", coords)
    closest_shop = first_coffee_shops(coords)
    pprint(closest_shop)
    save_map(coords)


if __name__ == '__main__':
    main()