import pandas as pd
import numpy as np
from util.constants import *


class FlashCards:

    def __init__(self):
        self.file = None
        self.df = None
        self.category = "category"

    def set_defaults(self, file):
        self.file = file
        self.df = pd.read_csv(file)
        self.df['probabilities'] = np.array([1 / len(self.df)] * len(self.df))
        self.df['category'] = new
        self.df['count'] = -1

    def generate(self):
        idx = np.random.choice(self.df.index, p=self.df["probabilities"])
        print(self.df.head())
        return idx, self.df.loc[idx, :]

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
            self.df.loc[self.df["category"] == key, "probabilities"] = prob[key] / self.df["category"].value_counts()[
                key]

    def shuffle(self, choice, idx):
        print(choice)
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
