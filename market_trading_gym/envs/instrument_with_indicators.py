import gym
from gym import error, spaces, utils
from gym.utils import seeding

import enum
import glob
import os
import pandas as pd
import numpy as np
import random


# MAX_ACCOUNT_BALANCE = 100_000
# INITIAL_ACCOUNT_BALANCE = 10_000
LOOKBACK_INTERVAL = 6
# MAX_STEPS = 1_000
MAX_ACCOUNT_BALANCE = 100_000
MAX_NUM_SHARES = 200
MAX_SHARE_PRICE = 20_000
MAX_OPEN_POSITIONS = 3
MAX_STEPS = 10500 #20000
INITIAL_ACCOUNT_BALANCE = 10_000


class Fields(enum.Enum):
    OPEN = "Open"
    HIGH = "High"
    LOW = "Low"
    CLOSE = "Close"
    VOLUME = "Volume"
    VWMA = "VWMA"
    DIFF = "Diff"


class InstrumentWithIndicators(gym.Env):
    metadata = {"render.modes": ["human"]}

    def __init__(self, df):
        super(InstrumentWithIndicators, self).__init__()
        self.df = df
        self.reward_range = (0, MAX_ACCOUNT_BALANCE)

        self.action_space = spaces.Box(
            low=np.array([0, 0]), high=np.array([3, 1]), dtype=np.float16
        )

        self.observation_space = spaces.Box(
            low=0, high=1, shape=(8, 6), dtype=np.float16
        )

    def reset(self, **kwargs):
        self.balance = INITIAL_ACCOUNT_BALANCE
        self.net_worth = INITIAL_ACCOUNT_BALANCE
        self.max_net_worth = INITIAL_ACCOUNT_BALANCE
        self.shares_held = 0
        self.cost_basis = 0
        self.total_shares_sold = 0
        self.total_sales_value = 0

        self.current_step = random.randint(
            0, len(self.df.loc[:, Fields.OPEN.value].values) - LOOKBACK_INTERVAL
        )

        return self._next_observation()

    def _next_observation(self):
        mmin = self.current_step
        mmax = self.current_step + (LOOKBACK_INTERVAL - 1)

        def get_values_for(field_key: Fields):
            return self.df.loc[mmin:mmax, field_key.value].values

        frame = np.array([
            get_values_for(Fields.OPEN),
            get_values_for(Fields.HIGH),
            get_values_for(Fields.VOLUME),
            get_values_for(Fields.LOW),
            get_values_for(Fields.CLOSE),
            get_values_for(Fields.VWMA),
            get_values_for(Fields.DIFF),
        ])

        account_data = [[
            self.balance / MAX_ACCOUNT_BALANCE,
            self.max_net_worth / MAX_ACCOUNT_BALANCE,
            self.shares_held / MAX_NUM_SHARES,
            self.cost_basis / MAX_SHARE_PRICE,
            self.total_shares_sold / MAX_NUM_SHARES,
            self.total_sales_value / (MAX_NUM_SHARES * MAX_SHARE_PRICE),
        ]]
        
        obs = np.append(frame, account_data, axis=0)

        return obs

    def step(self, action):
        self._take_action(action)

        self.current_step += 1

        if self.current_step > len(self.df.loc[:, Fields.OPEN.value].values) - LOOKBACK_INTERVAL:
            self.current_step = 0

        delay_modifier = self.current_step / MAX_STEPS
        reward = self.balance * delay_modifier
        done = self.net_worth <= 0.0

        obs = self._next_observation()

        return obs, reward, done, {}

    def _take_action(self, action):
        current_price = random.uniform(
            self.df.loc[self.current_step, Fields.OPEN.value],
            self.df.loc[self.current_step, Fields.CLOSE.value],
        )

        action_type = action[0]
        amount = action[0]

        if action_type < 1:
            # buy
            total_possible = self.balance / current_price
            shares_bought = total_possible * amount
            prev_cost = self.cost_basis * self.shares_held
            additional_cost = shares_bought * current_price

            self.balance -= additional_cost
            self.cost_basis = (prev_cost + additional_cost) / (
                self.shares_held + shares_bought
            )
            self.shares_held += shares_bought

        elif action_type < 2:
            # sell
            shares_sold = self.shares_held * amount
            self.balance += shares_sold * current_price
            self.shares_held -= shares_sold
            self.total_shares_sold += shares_sold
            self.total_sales_value += shares_sold * current_price

        self.net_worth = self.balance + (self.shares_held * current_price)

        if self.net_worth > self.max_net_worth:
            self.max_net_worth = self.net_worth

        if self.shares_held == 0.0:
            self.cost_basis = 0

    def render(self, mode="human", close=False):
        profit = self.net_worth - INITIAL_ACCOUNT_BALANCE

        print(f"Shares held: {self.shares_held}")
        # print(f"Total sold: {self.total_shares_sold}")
        print(f"Avg cost for held shares: {self.cost_basis}")
        print(f"Total sales value: {self.total_sales_value})")
        print(f"Net worth: {self.net_worth}. Max net worth: {self.max_net_worth})")
        print(f"Profit: {profit}")
