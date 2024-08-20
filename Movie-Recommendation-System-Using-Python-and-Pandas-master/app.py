from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load the recommendations data
df_result = pd.read_csv('MovieRecommendations.csv')

@app.route('/')
def index():
    movies = df_result['title'].tolist()
    return render_template('index.html', movies=movies)

@app.route('/recommend', methods=['POST'])
def recommend():
    selected_movie = request.form.get('movie')
    print(f"Selected movie: {selected_movie}")  # Debug print

    if selected_movie in df_result['title'].values:
        list_result = df_result[df_result['title'] == selected_movie]
        print(f"List result: {list_result}")  # Debug print

        recommendations = {
            'First': list_result['FirstMovieRecommendation'].values[0],
            'Second': list_result['SecondMovieRecommendation'].values[0],
            'Third': list_result['ThirdMovieRecommendation'].values[0],
            'Fourth': list_result['FourthMovieRecommendation'].values[0]
        }
    else:
        recommendations = {
            'First': 'No recommendations available',
            'Second': '',
            'Third': '',
            'Fourth': ''
        }

    print(f"Recommendations: {recommendations}")  # Debug print
    return render_template('recommendations.html', movie=selected_movie, recommendations=recommendations)
if __name__ == '__main__':
    app.run(debug=True)
