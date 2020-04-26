from flask import Flask, render_template, request
import os

from util.constants import choices
from util.shuffle import FlashCards

model = FlashCards()
app = Flask(__name__)

UPLOAD_PATH = 'files/'
app.config['UPLOAD_FOLDER'] = UPLOAD_PATH


# noinspection PyBroadException
@app.route('/', methods=['GET', "POST"])
def index():
    if request.method == 'POST':
        if "file" in request.files:
            file = request.files['file']
            if file.filename == '':
                errors = "Empty File BC"
                return render_template("index.html", errors=errors)
            try:
                path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(path)
                model.set_defaults(path)
                idx, flashcard = model.generate()
                return render_template("cards.html", flashcard=flashcard.head(), idx=idx)
            except:
                errors = "Haggu"
                return render_template("index.html", errors=errors)
        else:
            if request.form.get('knew_it'):
                print("here")
                choice = choices['knew_it']
                idx = request.form.get("knew_it")
                idx, flashcard = model.shuffle(choice, int(idx))
                return render_template("cards.html", flashcard=flashcard.head(), idx=idx)
            elif request.form.get('no_clue'):
                print("no here")
                choice = choices['no_clue']
                idx = request.form.get("no_clue")
                idx, flashcard = model.shuffle(choice, int(idx))
                return render_template("cards.html", flashcard=flashcard.head(), idx=idx)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
