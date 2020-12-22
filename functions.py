import numpy as np
import pandas as pd
import matrix_factorization_utilities
import os
import datetime

tic = datetime.datetime.now()
ratings = pd.read_csv("static/data/ratings.csv")

ratings = ratings[['userId', 'movieId', 'rating']]


len(ratings['userId'].unique())

count_ratings = ratings.groupby('rating').count()
count_ratings['perc_total'] = round(count_ratings['userId'] * 100 / count_ratings['userId'].sum(), 1)

movie_list = pd.read_csv('static/data/movies.csv')
tags = pd.read_csv('static/data/tags.csv')
genres = movie_list['genres']

genre_list = ""
for index, row in movie_list.iterrows():
    genre_list += row.genres + "|"
genre_list_split = genre_list.split('|')
new_list = list(set(genre_list_split))
new_list.remove('')

movies_with_genres = movie_list.copy()

for genre in new_list:
    movies_with_genres[genre] = movies_with_genres.apply(lambda _: int(genre in _.genres), axis=1)

no_of_users = len(ratings['userId'].unique())
no_of_movies = len(ratings['movieId'].unique())

sparsity = round(1.0 - len(ratings) / (1.0 * (no_of_movies * no_of_users)), 3)
len(ratings['movieId'].unique())

avg_movie_rating = pd.DataFrame(ratings.groupby('movieId')['rating'].agg(['mean', 'count']))
avg_movie_rating['movieId1'] = avg_movie_rating.index

np.percentile(avg_movie_rating['count'], 70)

avg_rating_all = ratings['rating'].mean()

min_reviews = 30
movie_score = avg_movie_rating.loc[avg_movie_rating['count'] > min_reviews]


def weighted_rating(x, m = min_reviews, C = avg_rating_all):
    v = x['count']
    R = x['mean']
    # IMDB formula
    return (v / (v + m) * R) + (m / (m + v) * C)


movie_score['weighted_score'] = movie_score.apply(weighted_rating, axis=1)

movie_score = pd.merge(movie_score, movies_with_genres, on='movieId')
pd.DataFrame(movie_score.sort_values(['weighted_score'], ascending=False)[
                 ['title', 'count', 'mean', 'weighted_score', 'genres']][:10])


def best_movies_by_genre(genre, top_n):
    return pd.DataFrame(movie_score.loc[(movie_score[genre] == 1)].sort_values(['weighted_score'],
                                                                               ascending=False)[
                            ['title', 'count', 'mean', 'weighted_score']][:top_n])["title"]


ratings_df = pd.pivot_table(ratings, index='userId', columns='movieId', aggfunc=np.max)
temp = ratings_df.drop([i for i in range(6, 7121)], axis=0)

U, M = matrix_factorization_utilities.low_rank_matrix_factorization(
    temp.to_numpy(), num_features=5, regularization_amount=1.0)
ratings_movies = pd.merge(ratings, movie_list, on='movieId')


def get_other_movies(movie_name):
    df_movie_users_series = ratings_movies.loc[ratings_movies['title'] == movie_name]['userId']
    df_movie_users = pd.DataFrame(df_movie_users_series, columns=['userId'])
    other_movies = pd.merge(df_movie_users, ratings_movies, on='userId')
    other_users_watched = pd.DataFrame(other_movies.groupby('title')['userId'].count()).sort_values('userId',ascending=False)
    other_users_watched['perc_who_watched'] = round(other_users_watched['userId'] * 100 / other_users_watched['userId'][0], 1)
    titles = []
    for i, row in other_users_watched[:10].iterrows():
        titles.append(i)
    return titles


# get_other_movies("Toy Story (1995)")

from sklearn.neighbors import NearestNeighbors

# only include movies with more than 10 ratings
movie_plus_10_ratings = avg_movie_rating.loc[avg_movie_rating['count'] >= 10]

filtered_ratings = pd.merge(movie_plus_10_ratings, ratings, on="movieId")

movie_wide = filtered_ratings.pivot(index='movieId', columns='userId', values='rating').fillna(0)

model_knn = NearestNeighbors(metric='cosine', algorithm='brute')

model_knn.fit(movie_wide)


ratingsml = pd.read_csv("static/data/movielens-data/ratings.csv")
movies = pd.read_csv("static/data/movielens-data/movies.csv")
ratingsml = pd.merge(movies, ratingsml)
print("Done")
user_ratingsml = ratingsml.pivot_table(index=['userId'], columns=['title'], values='rating')
print("Done")

user_ratingsml = user_ratingsml.dropna(thresh=10, axis=1).fillna(0)
print("Done")


movie_similarity_df = user_ratingsml.corr(method="pearson")

print("Done")

def get_similar_movies_content_based(movie_name, user_rating):
    similar_movies = movie_similarity_df[movie_name] * (user_rating - 2.5)
    similar_movies = similar_movies.sort_values(ascending=False)
    # print(similar_score[:10])
    moviees = []
    for moviee,rating in similar_movies[:10].iteritems():
        moviees.append(moviee)
    return moviees


toc = datetime.datetime.now()
print(toc-tic)
# print(get_similar_movies_content_based("Toy Story (1995)", 7))
