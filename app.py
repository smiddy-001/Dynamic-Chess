from flask import Flask, render_template
from chessEngine import start_game

COLORS = {"White":"ffffff",
          "Rich black":"111420",
          "Off Red":"ee1e0b",
          "Aureolin":"eee52f",
          "Lime green":"17cc26",
          "Celtic Blue":"2b68d9",
          "Dark violet":"9828b6"}

IS_DARK = False

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route('/')
def index():
    return render_template('index.html', chess_board=start_game(), cell_size=24, color1=COLORS["Rich black"], color2=COLORS["White"])


if __name__ == '__main__':
    app.run(debug=True)
    # flask run --extra-files app/templates/
