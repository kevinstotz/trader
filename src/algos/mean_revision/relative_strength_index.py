from matplotlib import pyplot as plt
import pandas as pd
from src.algos.data_miner import DataMiner, Units
from src.algos.trend_following.trend_following_moving_average import TFMA


class RelativeStrengthIndex(TFMA):

    def __init__(self, data: pd.DataFrame) -> None:
        self.data: pd.DataFrame = data
        self.window: int = 14
        self.sell_signals: pd.DataFrame = pd.DataFrame()
        self.buy_signals: pd.DataFrame = pd.DataFrame()

    def calculate(self, window=14):
        self.window = window
        self.data['change'] = self.data['close'].diff().dropna()
        gain = self.data['change'].where(self.data['change'] > 0.0, 0)
        loss = -self.data['change'].where(self.data['change'] < 0.0, 0)
        avg_gain = gain.rolling(window=self.window).mean()
        avg_loss = loss.rolling(window=self.window).mean()
        rs = avg_gain / avg_loss
        self.data['rsi'] = 100.0 - (100.0 / (1.0 + rs))

    def display(self) -> None:
        plt.figure(figsize=(12, 8))
        plt.plot(self.data.index, self.data['rsi'], label='RSI ' + str(self.window))
        plt.xlabel('Date')
        plt.ylabel('RSi')
        plt.title('Relative Strength Index (RSI)')
        plt.legend(['rsi'], loc='upper right')
        plt.show()

    def tabulate(self, size=10) -> str:
        return self.data.head(size).to_string()

    def signal(self) -> float:
        return self.data['rsi'].take([-1]).iloc[0]


dm = DataMiner(units=Units.DAY, period=200)
rsi = RelativeStrengthIndex(data=dm.get_data())
rsi.calculate(window=50)
print(rsi.tabulate(size=300))
print(rsi.signal())
rsi.display()
