import pandas as pd
import numpy as np

# Load datasets
df = pd.read_csv('dataset.csv', sep='\t', names=['user_id', 'item_id', 'rating', 'timestamp'])
movie_titles = pd.read_csv('movieIdTitles.csv')
df = pd.merge(df, movie_titles, on='item_id')

# Calculate ratings
ratings = pd.DataFrame(df.groupby('title')['rating'].mean())
ratings['numOfRatings'] = pd.DataFrame(df.groupby('title')['rating'].count())

# Create pivot table
moviemat = df.pivot_table(index='user_id', columns='title', values='rating')

# Calculate recommendations
for i in ratings.index:
    if i not in moviemat.columns:
        continue  # Skip if movie is not in the pivot table

    movieUserRatings = moviemat[i]
    similarToThatMovie = moviemat.corrwith(movieUserRatings)
    corr_toMovie = pd.DataFrame(similarToThatMovie, columns=['Correlation'])
    corr_toMovie.dropna(inplace=True)
    corr_toMovie = corr_toMovie.join(ratings['numOfRatings'])
    result = corr_toMovie[corr_toMovie['numOfRatings'] > 100].sort_values('Correlation', ascending=False)

    # Ensure there are enough recommendations
    if result.shape[0] >= 5:
        ratings.loc[i, 'FirstMovieRecommendation'] = result.iloc[1:2].index.values[0]
        ratings.loc[i, 'SecondMovieRecommendation'] = result.iloc[2:3].index.values[0]
        ratings.loc[i, 'ThirdMovieRecommendation'] = result.iloc[3:4].index.values[0]
        ratings.loc[i, 'FourthMovieRecommendation'] = result.iloc[4:5].index.values[0]
    else:
        ratings.loc[i, 'FirstMovieRecommendation'] = '-'
        ratings.loc[i, 'SecondMovieRecommendation'] = '-'
        ratings.loc[i, 'ThirdMovieRecommendation'] = '-'
        ratings.loc[i, 'FourthMovieRecommendation'] = '-'

ratings = ratings.fillna('-')
ratings.to_csv('MovieRecommendations.csv', encoding='utf-8')
