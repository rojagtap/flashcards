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
                idx, flashcard, n_total, p_mastered, p_learning, p_reviewing,  n_mastered, n_learning, n_reviewing = model.generate()
                word, meaning, category, example = flashcard["word"], flashcard["meaning"], flashcard["category"], flashcard["example"]
                if type(example) == float:
                    example = None
                return render_template("cards.html", word=word, meaning=meaning, category=category, idx=idx, example=example, total=n_total, mastered=p_mastered, learning=p_learning, reviewing=p_reviewing, n_mastered=n_mastered, n_learning=n_learning, n_reviewing=n_reviewing)
            except Exception as ex:
                errors = ex
                return render_template("index.html", errors=errors)
        else:
            if request.form.get('knew_it'):
                choice = choices['knew_it']
                idx = request.form.get("knew_it")
                idx, flashcard, n_total, p_mastered, p_learning, p_reviewing,  n_mastered, n_learning, n_reviewing = model.shuffle(choice, int(idx))
                word, meaning, category, example = flashcard["word"], flashcard["meaning"], flashcard["category"], flashcard["example"]
                if type(example) == float:
                    example = None
                return render_template("cards.html", word=word, meaning=meaning, category=category, idx=idx, example=example, total=n_total, mastered=p_mastered, learning=p_learning, reviewing=p_reviewing, n_mastered=n_mastered, n_learning=n_learning, n_reviewing=n_reviewing)
            elif request.form.get('no_clue'):
                choice = choices['no_clue']
                idx = request.form.get("no_clue")
                idx, flashcard, n_total, p_mastered, p_learning, p_reviewing,  n_mastered, n_learning, n_reviewing = model.shuffle(choice, int(idx))
                word, meaning, category, example = flashcard["word"], flashcard["meaning"], flashcard["category"], flashcard["example"]
                if type(example) == float:
                    example = None
                return render_template("cards.html", word=word, meaning=meaning, category=category, idx=idx, example=example, total=n_total, mastered=p_mastered, learning=p_learning, reviewing=p_reviewing, n_mastered=n_mastered, n_learning=n_learning, n_reviewing=n_reviewing)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
