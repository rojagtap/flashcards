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
                errors = "File Not Found"
                return render_template("index.html", errors=errors)
            try:
                if not(os.path.isdir(app.config['UPLOAD_FOLDER'])):
                    os.mkdir(app.config['UPLOAD_FOLDER'])
                path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(path)
                model.set_defaults(path)
                idx, flashcard = model.generate()
                word, meaning, category = flashcard["word"], flashcard["meaning"], flashcard["category"]
                return render_template("cards.html", word=word, meaning=meaning, category=category, idx=idx)
            except Exception as ex:
                errors = ex
                return render_template("index.html", errors=errors)
        else:
            if request.form.get('knew_it'):
                choice = choices['knew_it']
                idx = request.form.get("knew_it")
                idx, flashcard = model.shuffle(choice, int(idx))
                word, meaning, category = flashcard["word"], flashcard["meaning"], flashcard["category"]
                return render_template("cards.html", word=word, meaning=meaning, category=category, idx=idx)
            elif request.form.get('no_clue'):
                choice = choices['no_clue']
                idx = request.form.get("no_clue")
                idx, flashcard = model.shuffle(choice, int(idx))
                word, meaning, category = flashcard["word"], flashcard["meaning"], flashcard["category"]
                return render_template("cards.html", word=word, meaning=meaning, category=category, idx=idx)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
