from argparse import ArgumentParser
import requests


import geopy.distance
from geopy.geocoders import Nominatim
from geopy.point import Point


def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        "-l", "--location", help="Location to search for", required=True
    )
    parser.add_argument(
        "-b", "--box-size", type=int, default=500, help="Search radius in meters"
    )
    # return json
    parser.add_argument(
        "-j", "--json", action="store_true", help="Output in JSON format"
    )
    return parser.parse_args()


def get_box(point: Point, size_m: float) -> tuple[Point, Point]:
    size_km = size_m / 1000
    distance = geopy.distance.distance(kilometers=size_km / 2)
    top_center = distance.destination(point, bearing=0)
    top_right = distance.destination(top_center, bearing=90)
    bottom_center = distance.destination(point, bearing=180)
    bottom_left = distance.destination(bottom_center, bearing=270)
    return top_right, bottom_left


def get_hub_info(top_right: Point, bottom_left: Point) -> dict:
    # https://sharedmobility.github.io/Donkey.html
    url = "https://stables.donkey.bike/api/public/nearby"
    params = {
        "top_right": f"{top_right.latitude},{top_right.longitude}",
        "bottom_left": f"{bottom_left.latitude},{bottom_left.longitude}",
        "filter_type": "box",
    }
    headers = {"Accept": "application/com.donkeyrepublic.v7"}
    response = requests.get(url, params=params, headers=headers)
    return response.json()["hubs"]


def main():
    args = parse_args()
    geolocator = Nominatim(user_agent="donkapi")
    try:
        location = geolocator.geocode(args.location)
    except:
        print('No internet connection')
        return
    point = location.point
    top_right, bottom_left = get_box(point, args.box_size)
    hub_info = get_hub_info(top_right, bottom_left)
    if len(hub_info) == 0:
        print("No bike hubs found")
        return
    result = []
    for hub in hub_info:
        lat = hub["latitude"]
        long = hub["longitude"]
        distance = geopy.distance.distance(
            (lat, long), (point.latitude, point.longitude)
        )
        bikes_available = hub["available_vehicles_count"]
        result.append(
            {
                "name": hub["name"],
                "distance": int(distance.m),
                "bikes_available": bikes_available,
            }
        )
    # Sort by distance
    result.sort(key=lambda x: x["distance"])
    max_name_length = max([len(hub["name"]) for hub in result])
    if args.json:
        print({"hubs": result})
        return
    else:
        for hub in result:
            print(
                f"{hub["name"]+':':<{max_name_length+4}} {hub["distance"]:>8} m, {hub["bikes_available"]} bikes available "
            )


if __name__ == "__main__":
    main()
