import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
pd.set_option('display.expand_frame_repr', False)

df = pd.read_csv("the_movies_dataset\movies_metadata.csv", low_memory=False)


def content_based_recommender(title, cosine_sim, dataframe):
    dataframe = dataframe[~dataframe["title"].isna()]
    indices = pd.Series(dataframe.index, index=dataframe['title'])
    indices = indices[~indices.index.duplicated(keep='last')]
    movie_index = indices[title]
    similarity_scores = pd.DataFrame(cosine_sim[movie_index], columns=["score"])
    movie_indices = similarity_scores.sort_values("score", ascending=False)[1:11].index
    return dataframe['title'].iloc[movie_indices]


def calculate_cosine_sim(dataframe):
    tfidf = TfidfVectorizer(stop_words='english')
    dataframe['overview'] = dataframe['overview'].fillna('')
    tfidf_matrix = tfidf.fit_transform(dataframe['overview'])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return cosine_sim



cosine_sim = calculate_cosine_sim(df)

#RECOMMEND-1
content_based_recommender('The Dark Knight Rises', cosine_sim, df)

#RECOMMEND-2
content_based_recommender('The Godfather', cosine_sim, df)

#RECOMMEND-3
content_based_recommender('Sherlock Holmes', cosine_sim, df)
