import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from src.algos.data_miner import DataMiner, Units
from src.algos.trend_following.trend_following_moving_average import TFMA


class RateOfChange(TFMA):

    def __init__(self, data: pd.DataFrame, period: int = 20) -> None:
        self.data: pd.DataFrame = data
        self.period: int = period
        self.sell_signals: pd.DataFrame = pd.DataFrame()
        self.buy_signals: pd.DataFrame = pd.DataFrame()

    def calculate(self) -> None:
        self.data['ROC'] = 188.0 * (self.data['close'] / self.data['close'].pct_change(periods=self.period))
        self.data['buy'] = (self.data['close']).where((self.data['ROC'] > 0) & (self.data['ROC'].shift(1) < 0))
        self.data['sell'] = (self.data['close']).where((self.data['ROC'] < 0) & (self.data['ROC'].shift(1) > 0))

    def signal(self):
        # Buy securities when a buy signal is generated and sell them when a sell signal is generated
        # 1 for Buy, -1 for Sell, 0 for Hold
        self.data['signal'] = np.where(self.data['buy'], 1, np.where(self.data['sell'], -1, 0))
        return self.data['signal']

    def strategy_return(self):
        self.data['returns'] = self.data['signal'].shift(1) * self.data['close'].pct_change()
        self.data['returns+1'] = 1 + self.data['returns']
        self.data['cumulative_returns'] = (1 + self.data['returns']).cumprod()
        return self.data['cumulative_returns'].tail(1)

    def display(self) -> None:
        plt.figure(figsize=(12, 8))

        plt.plot(self.data.index, self.data['ROC'], label='ROC ' + str(self.period))
        plt.plot(self.data.index, self.data['signal'], label='signal')
        plt.plot(self.data.index, self.data['close'], label='close')

        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.title('Rate Of Change (' + str(self.period) + ')')
        plt.legend(['ROC', 'signal', 'close'], loc='upper right')
        plt.show()

    def tabulate(self, size=10) -> str:
        return self.data.head(size).to_string()


dm = DataMiner(units=Units.DAY, period=200)

roc = RateOfChange(data=dm.get_data())
roc.calculate()
print(roc.tabulate(size=300))
print("Signal:")
print(roc.signal())
print("ROC Return: " + str(roc.strategy_return()))
# print("Buy and Hold: " + str(roc.buy_and_hold_return()))
roc.display()
