from io import StringIO
import json
import random

import requests
import pandas

PAST_FAVORITE_MOVIES = [
    'tt0910970',
    'tt0266543',
    'tt1323594',
    'tt0268380',
    'tt2948356',
    'tt0441773',
    'tt2245084',
    'tt1690953',
    'tt1772341',
    'tt0351283',
    'tt2380307',
    'tt1192628',
    'tt2277860',
    'tt1001526',
    'tt0837562',
    'tt0481499',
    'tt0448694',
    'tt0472033',
    'tt0358082',
    'tt4302938',
    'tt3874544'
]


def convert_to_csv(movies_data):
    print("Converting movies details to csv started")
    csv_data = 'Title,Genre,Production,Rating\n'
    for item in movies_data:
        title = item['Title'].strip().replace(',', '')
        genre = item['Genre'].strip().replace(',', '|')
        production = item['Production'].strip().replace(',', '|')
        csv_data += f"{title},{genre},{production}, {random.randint(7, 10)}\n"
    print("Converting movies details to csv finished")
    return csv_data


def collect_movies_details(movies):
    print("Collecting movies details from omdbapi started")
    movies_data = []
    omdbapi_url = 'https://www.omdbapi.com/?i={}&apikey=bcf44120'
    for item in movies:
        request_url = omdbapi_url.format(item)
        try:
            movie_details = json.loads(requests.get(request_url, timeout=60).text)
            movies_data.append(movie_details)
        except Exception as e:
            print(f"Exception while getting response from api for url: '{request_url}', Exception: '{str(e)}'")
    print("Collecting movies details from omdbapi finished")
    return movies_data


def main():
    # movies_data = collect_movies_details(PAST_FAVORITE_MOVIES)
    # csv_data = convert_to_csv(movies_data)
    # print(csv_data)
    # data_set = pandas.read_csv(StringIO(csv_data))
    data_set = pandas.read_csv('my_movies_list.csv')








if __name__ == '__main__':
    main()
