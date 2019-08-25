import gym
from gym import error, spaces, utils
from gym.utils import seeding

from pathlib import Path

import glob
import csv
import os
import pandas as pd
import pyarrow.parquet as pq
from random import randint


class SimpleStockEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.random_state = randint(0, 200)
        self.row_number = None
        self.last_row_number = None

    def step(self, action):
        self.row_number += 1
        row = self.df.iloc[self.row_number]
        done = (self.last_row_number == row.name)
        return (row, done)

    def reset(self, **kwargs):
        symbol = kwargs["symbol"]
        dfs = []
        for fn in Path('data/finx-data-catcher').glob(f'**/*{symbol}*.json'):
            dfs.append(pd.read_json(str(fn)))
        self.df = pd.concat(dfs)
        self.row_number = self.random_state
        self.last_row_number = len(self.df.index)-1
        return self.df.iloc[self.row_number]

    def render(self, mode='human', close=False):
        # print("LendingclubEnv.render")
        x = 1
