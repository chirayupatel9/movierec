import numpy as np
import pandas as pd
import pickle
import scipy.sparse as sp
from scipy.sparse.linalg import svds

ratings = pd.read_csv("static/data/music/song_data1.csv")

ratings = ratings[['user_id', 'song_id', 'listen_count']]
ratings_df = ratings.groupby(['user_id', 'song_id']).aggregate(np.max)

count_ratings = ratings.groupby('listen_count').count()
count_ratings['perc_total'] = round(count_ratings['user_id'] * 100 / count_ratings['user_id'].sum(), 1)

song_list = pd.read_csv('static/data/music/song_data.csv')
artist_name = song_list['artist_name']

avg_song_rating = pd.DataFrame(ratings.groupby('song_id')['listen_count'].agg(['mean', 'count']))
avg_song_rating['song_id1'] = avg_song_rating.index

np.percentile(avg_song_rating['count'], 70)

avg_rating_all = ratings['listen_count'].mean()
min_reviews = 30
song_score = avg_song_rating.loc[avg_song_rating['count'] > min_reviews]
ratings.sort_values('listen_count')

ratings_df1 = pd.pivot_table(ratings, index='user_id', columns='song_id', aggfunc=np.max)

ratings_movies = pd.merge(ratings, song_list, on='song_id')


def getsomemusic(song_name):
    df_movie_users_series = ratings_movies.loc[ratings_movies['title'] == song_name]['user_id']
    df_movie_users = pd.DataFrame(df_movie_users_series, columns=['user_id'])
    other_movies = pd.merge(df_movie_users, ratings_movies, on='user_id')
    other_users_watched = pd.DataFrame(other_movies.groupby('title')['user_id'].count()).sort_values('user_id',ascending=False)
    other_users_watched['perc_who_watched'] = round(other_users_watched['user_id'] * 100 / other_users_watched['user_id'][0], 1)
    # print(other_users_watched[:10])
    titles = []
    for i, row in other_users_watched[:10].iterrows():
        titles.append(i)
    return titles

    # return other_users_watched[:10]

getsomemusic('That Tree (feat. Kid Cudi)')
# getsomemusic('Borders')
