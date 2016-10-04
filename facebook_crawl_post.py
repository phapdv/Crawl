#!/usr/local/bin/python3
import os
import datetime
import csv
import json
import requests


def get_token(app_id, app_secret):
    # return access_token
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


def get_post_in_page(page_id, access_token):
    # Result list of posts
    url = 'https://graph.facebook.com/{}/posts?limit=100&\
    {}'.format(page_id, access_token)
    response = requests.get(url)
    with open('dumps.txt', 'w') as f:
        json.dump(response.json(), f, indent=4)
    return response.json()


def fb_convert_time(time):
    return datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S+0000')


def post_id_in_24h(data_post):
    # Output data_out -> list of post
    data_out = []
    current_time = datetime.datetime.utcnow()
    time_get_post = (current_time - datetime.timedelta(days=1)).replace(microsecond=0)
    data = [element for element in data_post if fb_convert_time(
        element['created_time']) > time_get_post]
    # save post_id
    if not os.path.isfile('post_id.txt'):
        f = open('post_id.txt', 'w')
        f.close()

    with open('post_id.txt', 'r+') as fp:
        file_reader = fp.read()
        for post in data:
            if post['id'] not in file_reader:
                fp.write(post['id'] + '\n')
                data_out.append(post)
    return data_out


def WriteDictToCSV(csv_file, csv_columns, dict_data):
    try:
        with open(csv_file, 'a+', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            for data in dict_data:
                writer.writerow(data)
    except IOError as e:
        print("I/O error({0})".format(e))
    return


def write_to_csv(data):
    if not os.path.isfile('post.csv'):
        f = open('post.csv', 'w')
        f.close()
    csv_columns = ['id', 'created_time', 'message', 'story']
    WriteDictToCSV('post.csv', csv_columns, data)


def main():
    APP_ID = '1283221561758248'
    APP_SECRET = 'a3c0b3755bafbeea93b8a237aab98e34'
    try:
        with open('pages.txt', 'r') as fp:
            pages = fp.readlines()
            for page in pages:
                page = page.strip('\n')
                data = get_post_in_page(page, get_token(APP_ID, APP_SECRET))
                data2 = post_id_in_24h(data['data'])
                write_to_csv(data2)
    except FileNotFoundError:
        print('Create file pages.txt with each fanpage in one line')

if __name__ == '__main__':
    main()
