import requests


def download_image(img_url, save_to):
    response = requests.get(img_url)
    response.raise_for_status()

    with open(save_to, 'wb') as file:
        file.write(response.content)