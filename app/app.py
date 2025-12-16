from core.manager import load_free_games_data
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    free_games = load_free_games_data()

    return render_template("index.html", games=free_games)


if __name__ == "__main__":
    app.run(debug=True)
