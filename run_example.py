import gym
import market_trading_gym
import numpy as np

env = gym.make('market-trading-gym-simple-stock-v0')

RENDER_ENV = False
EPISODES = 1


def gen_action(row):
    return 0


def moving_average(data_set, periods=3):
    weights = np.ones(periods) / periods
    return np.convolve(data_set, weights, mode='valid')


if __name__ == '__main__':
    initial_state = env.reset(symbol="TLT")
    action = gen_action(initial_state)

    done = False

    window = 5
    last_row = initial_state


    closes = np.array([])
    actions = np.array([])
    positions = np.array([])


    for episode in range(EPISODES):
        while done == False:
            row, done = env.step(action)
            closes = np.append(closes, [row.close])[-window:]

            closes_med = np.median(closes)

            ma = moving_average(closes, window)

            min_diff = 0.50

            diff = row.close - last_row.close

            msg = f"{np.around(diff, decimals=3)}. {row.close}"

            if abs(row.close - closes_med) > min_diff:
                if diff > 0:
                    msg += " significant vol. SHORT?"
                    actions = np.append(actions, [-1])
                    positions = np.append(actions, [-1])
                else:
                    msg += " significant vol. BUY?"
                    actions = np.append(actions, [+1])
                    positions = np.append(actions, [+1])

            else:
                action = 0
                position = 0

                actions = np.append(actions, [action])
                positions = np.append(positions, [position])


                # do I have positions to unwind?
                # if np.isin(-1, actions[-3:]):
                #     if np.sum(positions[-3:]) != 0:
                #         msg += f" buy to cover. {positions[-3:]}"
                #         actions = np.append(actions, [+1])
                #         positions = np.append(positions, [+1])
                # if np.isin(+1, actions[-3:]):
                #     if np.sum(positions[-3:]) != 0:
                #         msg += f" sell to unwind. {actions[-3:]}"
                #         actions = np.append(actions, [-1])
                #         positions = np.append(positions, [-1])


            print(msg)

            last_row = row

        # print(actions)
