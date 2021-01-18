# https://towardsdatascience.com/creating-a-custom-openai-gym-environment-for-stock-trading-be532be3910e
 

# external libs
import datetime as dt
import gym
import numpy as np
import os
import pandas as pd
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO2

# internal libs
from market_trading_gym.envs import InstrumentWithIndicators

# fixes MPI issue
os.environ["KMP_DUPLICATE_LIB_OK"] = "True"



def prepare_df(ddf: pd.DataFrame) -> pd.DataFrame:
    # format headers
    ddf.columns = [x.strip() for x in ddf.columns]
    ddf.rename(columns={"Last": "Close"}, inplace=True)

    # convert Date(str) and Time(str) into datetime column
    time_values = df.Date + df.Time
    ddf["Date"] = pd.to_datetime(
        time_values, format="%Y/%m/%d %H:%M:%S.%f", errors="coerce"
    )

    # remove data before roll period for the March 2021 contract
    ddf = ddf.query("Date > '2020-12-15'")

    # extract the specific RL model columns Date, OHLC, and Volume
    desired_columns = ["Date", "Open", "High", "Low", "Close", "Volume", "VWMA", "Diff"]
    ddf = ddf[desired_columns].copy()
    ddf.sort_values("Date", ignore_index=True, inplace=True)
    return ddf


df = pd.read_csv("data/m2k-renko.csv")
df = prepare_df(df)
env = DummyVecEnv([lambda: InstrumentWithIndicators(df)])

model = PPO2(MlpPolicy, env, verbose=1)
model.learn(total_timesteps=10_000)

obs = env.reset()
for i in range(20_000):
  action, _states = model.predict(obs)
  obs, rewards, done, info = env.step(action)
  env.render()