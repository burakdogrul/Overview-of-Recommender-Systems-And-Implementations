import pandas as pd
from surprise import Reader, SVD, Dataset, accuracy
from surprise.model_selection import GridSearchCV, train_test_split, cross_validate
pd.set_option('display.max_columns', None)

movie = pd.read_csv('movie_lens_dataset/movie.csv')
rating = pd.read_csv('movie_lens_dataset/rating.csv')
df = movie.merge(rating, how="left", on="movieId")


movie_ids = [130219, 356, 4422, 541]
movies = ["The Dark Knight (2011)",
          "Cries and Whispers (Viskningar och rop) (1972)",
          "Forrest Gump (1994)",
          "Blade Runner (1982)"]


sample_df = df[df.movieId.isin(movie_ids)]
user_movie_df = sample_df.pivot_table(index=["userId"], columns=["title"], values="rating")

reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(sample_df[['userId', 'movieId', 'rating']], reader)

trainset, testset = train_test_split(data, test_size=.25)
svd_model = SVD()
svd_model.fit(trainset)
predictions = svd_model.test(testset)

cross_validate(svd_model, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)

##RECOMMEND-1
svd_model.predict(uid=1.0, iid=541, verbose=True)

#RECOMMEND-2
svd_model.predict(uid=1.0, iid=356, verbose=True)
