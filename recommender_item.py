import pandas as pd
pd.set_option('display.max_columns', 20)

movie = pd.read_csv('movie_lens_dataset/movie.csv')
rating = pd.read_csv('movie_lens_dataset/rating.csv')

df = movie.merge(rating, how="left", on="movieId")
df.head()

comment_counts = pd.DataFrame(df["title"].value_counts())
rare_movies = comment_counts[comment_counts["title"] <= 1000].index
common_movies = df[~df["title"].isin(rare_movies)]

user_movie_df = common_movies.pivot_table(index=["userId"], columns=["title"], values="rating")


def check_film(keyword, user_movie_df):
    return [col for col in user_movie_df.columns if keyword in col]


check_film("Sherlock", user_movie_df)


def item_based_recommender(movie_name, user_movie_df):
    movie_name = user_movie_df[movie_name]
    sorted_movie_rec = pd.DataFrame(user_movie_df.corrwith(movie_name).sort_values(ascending=False))
    sorted_movie_rec.reset_index(inplace=True)
    sorted_movie_rec = sorted_movie_rec.rename(columns={'title': 'Title', 0: 'Corr'})
    return sorted_movie_rec.iloc[1:11,:]

#RECOMMEND-1
item_based_recommender("Sherlock Holmes (2009)", user_movie_df)

