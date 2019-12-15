import json
import random

import numpy as np
import pandas
import requests
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

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
    csv_data = 'title,genre,production,rating\n'
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
    dataset = pandas.read_csv('my_movies_list.csv')

    # dealing with production dummy variable
    # production is a single valued variable (which means production can either be disney, WB or dreamworks etc).
    # so we will remove one dummy variable in order to avoid dummy trap for production, hence at the end we will be
    # having (n-1) dummy variables for production
    dataset = pandas.get_dummies(dataset, columns=['production'], prefix='p', drop_first=True)

    # dealing with genre dummy variables
    # set_index: Sets the index to which the functions relate.
    data_frame = dataset.set_index('title').genre.str.split('|', expand=True)
    data_frame_columns_length = data_frame.shape[1]
    for i in range(data_frame_columns_length):
        data_frame[i] = data_frame[i].str.strip()
    cleaned_dataset = data_frame.stack()
    genre_dummy_dataset = pandas.get_dummies(cleaned_dataset, prefix='g').groupby(level=0).sum()
    # merge genre dummy dataset with main dataset
    dataset = dataset.drop(columns=['genre'])
    dataset = pandas.concat([dataset.set_index('title'), genre_dummy_dataset], axis=1, sort=True)

    X = dataset.iloc[:, 1:].values
    y = dataset.iloc[:, 0].values

    # make sure data is split correctly
    if (len(dataset.columns) - 1) == X.shape[1]:
        print("Data is split correctly")
    else:
        raise Exception("Data is not split correctly")

    # splitting into training and testing data sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    print("Completed")


if __name__ == '__main__':
    main()
