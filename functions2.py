import datetime
import matrix_factorization_utilities
import pandas as pd
import numpy as np

tic = datetime.datetime.now()
ratingsb = pd.read_csv("static/data/books/ratings.csv")
# print(ratingsb)

ratingsb = ratingsb[['user_id', 'book_id', 'rating']]

ratings_df = ratingsb.groupby(['user_id', 'book_id']).aggregate(np.max)

len(ratingsb['user_id'].unique())

count_ratings = ratingsb.groupby('rating').count()
count_ratings['perc_total'] = round(count_ratings['user_id'] * 100 / count_ratings['user_id'].sum(), 1)

book_list = pd.read_csv("static/data/books/books.csv")
# print(book_list['original_title'])
tags = pd.read_csv("static/data/books/book_tags.csv")
authors = book_list['authors']

ratingsb = pd.merge(ratingsb, book_list)

user_ratingsml = ratingsb.pivot_table(index=['user_id'], columns=['original_title'], values='rating')
# print(user_ratingsml.columns)

user_ratingsml = user_ratingsml.dropna(thresh=5, axis=1).fillna(0)
# print("Done")
# print(user_ratingsml.to_csv("static/data/books/names1.csv"))

item_similarity_df = user_ratingsml.corr(method="pearson")

# print("Done")
toc = datetime.datetime.now()
print(toc - tic)


# print(item_similarity_df.to_csv("static/data/books/namess"))
def get_similar_books_content_based(book_name, user_rating):
    similar_score = item_similarity_df[book_name] * (user_rating - 2.5)
    similar_score = similar_score.sort_values(ascending=False)

    # print(similar_score[:10])
    bookss = []
    for books, rating in similar_score[:10].iteritems():
        bookss.append(books)
    return bookss


# print(get_similar_books_content_based("Cirque Du Freak (Cirque du Freak, #1) ", 7))
