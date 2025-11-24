from flask import Flask, render_template
from loader import load_free_games_data 

app = Flask(__name__)

@app.route('/')
def home():
    free_games = load_free_games_data() 
    
    return render_template('index.html', games=free_games) 

if __name__ == '__main__':
    app.run(debug=True)
