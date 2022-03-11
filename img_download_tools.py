import requests


def download_image(img_url, img_path):
    response = requests.get(img_url)
    response.raise_for_status()

    with open(img_path, 'wb') as file:
        file.write(response.content)