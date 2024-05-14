import pandas as pd
from matplotlib import pyplot as plt

from src.algos.data_miner import DataMiner, Units
from src.algos.trend_following.trend_following_moving_average import TFMA


class MovingAverageConvergenceDivergence(TFMA):

    def __init__(self, data: pd.DataFrame, long: int = 26, short: int = 12) -> None:
        self.data: pd.DataFrame = data
        self.long_window: int = long
        self.short_window: int = short
        self.sell_signals: pd.DataFrame = pd.DataFrame()
        self.buy_signals: pd.DataFrame = pd.DataFrame()

    def calculate(self) -> None:
        self.data['EMA_LONG'] = self.data['close'].ewm(span=self.short_window, adjust=False).mean()
        self.data['EMA_SHORT'] = self.data['close'].ewm(span=self.long_window, adjust=False).mean()
        # Calculate the 9-period EMA of MACD (Signal Line)
        self.data['MACD'] = self.data['EMA_SHORT'] - self.data['EMA_LONG']
        self.data['Signal_Line'] = self.data['MACD'].ewm(span=9, adjust=False).mean()

        self.buy_signals['signal'] = (self.data['close']).where(((self.data['MACD'] < self.data['Signal_Line']) &
                                                                 (self.data['MACD'].shift(1) > self.data[
                                                                     'Signal_Line'].shift(1))))
        self.sell_signals['signal'] = (self.data['close']).where(((self.data['MACD'] > self.data['Signal_Line']) &
                                                                 (self.data['MACD'].shift(1) < self.data[
                                                                     'Signal_Line'].shift(1))))

    def hold_return(self):
        return (self.data['close'].take([-1]).iloc[0] - self.data['close'].take([0]).iloc[0]) / \
            self.data['close'].take([0]).iloc[0]

    def tabulate(self, size=10) -> str:
        return self.data.head(size).to_string()

    def signal(self):
        previous_macd = self.data['MACD'].take([-2]).iloc[0]
        previous_signal_line = self.data['Signal_Line'].take([-2]).iloc[0]
        current_macd = self.data['MACD'].take([-1]).iloc[0]
        current_signal_line = self.data['Signal_Line'].take([-1]).iloc[0]

        if (previous_macd > previous_signal_line) and (current_macd < current_signal_line):
            return -1
        if (previous_macd < previous_signal_line) and (current_macd > current_signal_line):
            return 1
        return 0

    def strategy_return(self):
        return -1

    def display(self) -> None:
        plt.figure(figsize=(12, 8))

        plt.plot(self.data.index, self.data['EMA_LONG'], label='EMA ' + str(self.long_window))
        plt.plot(self.data.index, self.data['EMA_SHORT'], label='EMA ' + str(self.short_window))
        plt.plot(self.data.index, self.data['MACD'], label='MACD')
        plt.plot(self.data.index, self.data['Signal_Line'], label='Signal Line')
        plt.plot(self.data.index, self.data['close'], label='close')

        plt.scatter(self.buy_signals.index, self.buy_signals['signal'], label='Buy Signal', marker="^")
        plt.scatter(self.sell_signals.index, self.sell_signals['signal'], label='Sell Signal', marker="*")

        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.title('Moving Average Convergence Divergence (MACD) (' + str(self.short_window) + ', ' + str(self.long_window) + ')')
        plt.legend(['EMA_LONG', 'EMA_SHORT', 'MACD', 'Signal_Line', 'close'], loc='upper right')
        plt.show()


dm = DataMiner(units=Units.DAY, period=200)
d = dm.get_data()
macd = MovingAverageConvergenceDivergence(data=d)
macd.calculate()
print(macd.tabulate(size=300))
print(macd.signal())
print(macd.strategy_return())
print(macd.hold_return())
macd.display()
