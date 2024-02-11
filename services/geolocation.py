import json
from shapely.geometry import shape, GeometryCollection, Point
import requests

with open('map.geojson', 'r') as f:
    js = json.load(f)

# point_out = Point(30.2645, 59.9720)
# point_in = Point(30.3034, 59.9650)
def point_into_poligon(point):
    for feature in js['features']:

        polygon = shape(feature['geometry'])

        if polygon.contains(point):
            print ("ваш адресс входит в зону доставки")
            return True
        else:
            print("Ваш адресс вне зоны доставки")
            return False



def fetch_coordinates(adress):
    city = 'Санкт-Петербург, поселок Шушары, '
    adress += city
    apikey = '89a291dc-67e8-4eb7-a6c1-d7e107279f4b'
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": adress,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    print(lon, lat)
    adress_lon_lat = Point(lon, lat)
    return adress_lon_lat

def check_adress(adress):
    point = fetch_coordinates(adress)
    return point_into_poligon(point)
# apikey = '89a291dc-67e8-4eb7-a6c1-d7e107279f4b'  # ваш ключ
#
# coords = fetch_coordinates(apikey, "Внуково")
# print(coords)  # ('37.295014', '55.608562')
#
# coords = fetch_coordinates(apikey, "Серпуховская")
# print(coords)  # ('37.624992', '55.726872')
#
# coords = fetch_coordinates(apikey, "Красная площадь")
# print(coords)  # ('37.621031', '55.753595')
#
# coords = fetch_coordinates(apikey, "Санкт-Петербург, ул. Красного Курсанта")
# print(coords)  # None
# adress = Point(float(coords[0]), float(coords[1]),)
# print(adress)
# point_into_poligon(adress)
if __name__ == '__main__':
    city = 'Санкт-Петербург, '
    adress = city+'Чкаловский, 12'
    check_adress(adress)