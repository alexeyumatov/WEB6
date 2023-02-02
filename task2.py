import sys

from samles.geocoder import get_coordinates, get_ll_span
from samles.mapapi_PG import show_map
from samles.distance import lonlat_distance
from samles.business import find_business


def main():
    toponym_to_find = " ".join(sys.argv[1:])

    lat, lon = get_coordinates(toponym_to_find)
    address_ll = f'{lat},{lon}'
    span = f'0.005,0.005'

    org = find_business(address_ll, span, 'аптека')
    point = org['geometry']['coordinates']
    org_lat, org_lon = float(point[0]), float(point[1])
    point_param = f'pt={org_lat},{org_lon},pm2dgl'

    show_map(f'll={address_ll}&spn={span}', 'map', add_params=point_param)

    point_param = point_param + f'~{address_ll},pm2rdl'

    show_map(f'll={address_ll}&spn={span}', 'map', add_params=point_param)

    show_map(map_type='map', add_params=point_param)

    name = org['properties']['CompanyMetaData']['name']
    address = org['properties']['CompanyMetaData']['address']
    hours = org['properties']['CompanyMetaData']['Hours']['text']
    dist = round(lonlat_distance((lon, lat), (org_lon, org_lat)))

    snippet = f"Organisation name:\t{name}\nAddress:\t{address}" \
              f"\nWorking hours:\t{hours}\nDistance:\t{dist} m"
    print(snippet)


if __name__ == '__main__':
    main()
