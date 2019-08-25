from gym.envs.registration import register

register(
    id='market-trading-gym-simple-stock-v0',
    entry_point='market_trading_gym.envs:SimpleStockEnv',
)
