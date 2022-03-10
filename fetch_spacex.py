import requests
import os


from pathlib import Path
from img_download_tools import download_image
from urllib import parse


def fetch_spacex_last_launch(dir_name):
    spacex_url = 'https://api.spacexdata.com/v4/launches/5eb87d1fffd86e000604b36b'
    spacex_response = requests.get(spacex_url)
    spacex_response.raise_for_status()

    launch_info = spacex_response.json()
    launch_img_links = launch_info['links']['flickr']['original']

    for link in launch_img_links:
        img_link_parsed = parse.urlsplit(link)
        img_link_path = parse.unquote(img_link_parsed.path)
        img_path_parsed = os.path.split(img_link_path)
        img_path = f'{dir_name}/{img_path_parsed[1]}'

        download_image(link, img_path)


if __name__ == '__main__':
    space_x_dir = 'spaceX'
    Path(space_x_dir).mkdir(exist_ok=True)
    try:
        fetch_spacex_last_launch(space_x_dir)
    except requests.HTTPError:
        print('SpaceX server is not available.')
