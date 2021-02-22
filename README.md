# flashcards
Flashcards web app for learning anything. Developed using Flask

Python version 3.7.6
## How to use:
 - run `pip install -r requirements.txt` in the project directory to install dependencies
 - add data in the format:
      words: meanings: examples (each on separate line)
   and save as csv
 - run app using `python main.py -m Flask` to start the app and use on [http://localhost:5000](http://localhost:5000)


### csv format

    word:meaning:example
    testword0:testmeaning0:testexample0
    testword1:testmeaning1:testexample1
    testword2:testmeaning2:                       # in case there is no example sentence
    ...


### json format

    {
      "word0": {"meanings": ["meaning0", "meaning1", ...], "example": "example sentence"},
      "word1": {"meanings": ["meaning0", "meaning1", ...]}, ...
    }
