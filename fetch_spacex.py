import requests


from pathlib import Path
from img_download_tools import download_image


def fetch_spacex_last_launch(dir_name):
    spacex_url = 'https://api.spacexdata.com/v4/launches/5eb87d1fffd86e000604b36b'
    try:
        spacex_response = requests.get(spacex_url)
        spacex_response.raise_for_status()
    except:
        print('SpaceX server is not available')

    launch_info = spacex_response.json()
    launch_img_links = launch_info['links']['flickr']['original']

    for link in launch_img_links:
        img_url = link
        img_name = link.split('/')[-1]
        Path(dir_name).mkdir(exist_ok=True)
        img_path = f'{dir_name}/{img_name}'

        download_image(img_url, img_path)

if __name__ == '__main__':
    space_x_dir = 'spaceX'
    fetch_spacex_last_launch(space_x_dir)