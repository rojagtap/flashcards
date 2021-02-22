import json
import pandas as pd
import numpy as np
from util.constants import *


class FlashCards:
    def __init__(self):
        self.df = None
        self.category = "category"

    def read_file(self, file):
        if file.endswith("json"):
            data = json.load(open(file))
            words = list(data.keys())
            meanings = ["<br/>".join(value["meanings"]) for value in data.values()]
            examples = [value.get("example") for value in data.values()]
            self.df = pd.DataFrame(zip(words, meanings, examples), columns=["word", "meaning", "example"])
        elif file.endswith("csv"):
            self.df = pd.read_csv(file, sep=':')
        else:
            raise Exception("Unsupported File Format")


    def set_defaults(self, file):
        self.read_file(file)
        self.df['probabilities'] = np.array([1 / len(self.df)] * len(self.df))
        self.df['category'] = new
        self.df['count'] = -1

    def generate(self):
        idx = np.random.choice(self.df.index, p=self.df["probabilities"])
        print(self.df.loc[idx, :])
        value_counts = self.df["category"].value_counts()
        mastered_count = value_counts.get(mastered, 0)
        learning_count = value_counts.get(learning, 0)
        reviewing_count = value_counts.get(reviewing, 0)
        return idx, self.df.loc[idx, :], self.df.shape[0], mastered_count * 100 / self.df.shape[0], learning_count * 100 / self.df.shape[0], reviewing_count * 100 / self.df.shape[0], mastered_count, learning_count, reviewing_count

    def update_prob(self):
        prob = dict()
        addition = 0
        keys = self.df['category'].unique()
        for key in keys:
            prob[key] = categories[key]
            addition += categories[key]

        addition = (1 - addition) / self.df['category'].nunique()
        prob = {key: (value + addition) for key, value in prob.items()}
        for key in keys:
            self.df.loc[self.df["category"] == key, "probabilities"] = prob[key] / self.df["category"].value_counts()[key]

    def shuffle(self, choice, idx):
        if choice == choices['no_clue']:
            self.df.loc[idx, self.category] = learning
            self.update_prob()
            return self.generate()
        else:
            if self.df.loc[idx, "category"] == new:
                self.df.loc[idx, self.category] = mastered
            elif self.df.loc[idx, "category"] == reviewing:
                self.df.loc[idx, "count"] = self.df.loc[idx, "count"] - 1
                if self.df.loc[idx, "count"] == -1:
                    self.df.loc[idx, self.category] = mastered
            elif self.df.loc[idx, "category"] == learning:
                self.df.loc[idx, self.category] = reviewing
                self.df.loc[idx, "count"] = 3
            self.update_prob()
            return self.generate()
