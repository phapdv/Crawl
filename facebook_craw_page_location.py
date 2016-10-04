#!/usr/local/bin/python3
import requests


def get_token(app_id, app_secret):
    # access_token=1283221561758248|XsNkW030RHAd9NbXDTx1GXlLga8
    data_get = ['client_id={0}',
                'client_secret={1}',
                'grant_type=client_credentials']
    url = 'https://graph.facebook.com/oauth/access_token?' + \
        '&'.join(data_get).format(app_id, app_secret)
    response = requests.get(url)

    if response.status_code == 200:
        return response.text
    else:
        return False


def get_pages(keyword, latitude, longitude, distance, access_token):
    data_get = ['q={0}',
                'type=place',
                'center={1},{2}',
                'distance={3}',
                '{4}']
    url = 'https://graph.facebook.com/search?' + \
        '&'.join(data_get).format(keyword, latitude, longitude, distance, access_token)
    response = requests.get(url)

    if response.status_code == 200:
        page_ids = [page['id'] for page in response.json()['data']]
        url_pages = ['https://graph.facebook.com/{}?fields=website,name,location&{}'.format(
            page_id, access_token) for page_id in page_ids]
        return [requests.get(url_page).json() for url_page in url_pages]
    else:
        return False


def main():
    APP_ID = '1283221561758248'
    APP_SECRET = 'a3c0b3755bafbeea93b8a237aab98e34'
    keywords = ["coffee", "tea", "cafe", "caphe", "tra da"]
    latitude = '21.027875'
    longitude = '105.853654'
    distance = 1000
    access_token = get_token(APP_ID, APP_SECRET)
    for keyword in keywords:
        for i in get_pages(keyword, latitude, longitude, distance, access_token):
            print(i)

if __name__ == '__main__':
    main()
