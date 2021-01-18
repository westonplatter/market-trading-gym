import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

import datetime as dt
import gym
import pandas as pd
import numpy as np

from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO2

from market_trading_gym.envs import InstrumentWithIndicators


def prepare_df(df: pd.DataFrame) -> pd.DataFrame:
    # TODO(weston) - merge date/time fields into 1 python datetime field
    return df

df = pd.read_csv('data/m2k-renko.csv')
df = prepare_df(df)

# https://towardsdatascience.com/creating-a-custom-openai-gym-environment-for-stock-trading-be532be3910e
