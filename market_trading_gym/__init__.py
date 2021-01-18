from gym.envs.registration import register

register(
    id="instrument-with-indicators-v0",
    entry_point="market_trading_gym.envs:InstrumentWithIndicators",
)
