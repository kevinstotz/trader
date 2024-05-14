from matplotlib import pyplot as plt
import pandas as pd
from src.algos.data_miner import DataMiner, Units
from src.algos.trend_following.trend_following_moving_average import TFMA


class SimpleMovingAverage(TFMA):

    def __init__(self, data: pd.DataFrame, long: int = 50, short: int = 20) -> None:
        self.data: pd.DataFrame = data
        self.long_window: int = long
        self.short_window: int = short
        self.sell_signals: pd.DataFrame = pd.DataFrame()
        self.buy_signals: pd.DataFrame = pd.DataFrame()

    def display(self) -> None:
        plt.figure(figsize=(12, 6))

        plt.plot(self.data.index, self.data['SMA_LONG'], label='SMA ' + str(self.long_window) + ' Strategy')
        plt.plot(self.data.index, self.data['SMA_SHORT'], label='SMA ' + str(self.short_window) + ' Strategy')
        plt.plot(self.data.index, self.data['close'], label='close')

        plt.scatter(self.buy_signals.index, self.buy_signals['signal'], label='Buy Signal', marker="^")
        plt.scatter(self.sell_signals.index, self.sell_signals['signal'], label='Sell Signal', marker="*")

        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.title('BTC Simple Moving Averages (' + str(self.short_window) + ', ' + str(self.long_window) + ')')
        plt.legend(['SMA_LONG', 'SMA_SHORT', 'close'], loc='upper right')
        plt.show()

    def calculate(self) -> None:
        self.data['SMA_LONG'] = self.data['close'].rolling(window=self.long_window, min_periods=1, center=False).mean()
        self.data['SMA_SHORT'] = self.data['close'].rolling(window=self.short_window, min_periods=1,
                                                            center=False).mean()
        self.buy_signals['signal'] = (self.data['close']).where(((self.data['SMA_SHORT'] > self.data['SMA_LONG']) &
                                                                 (self.data['SMA_SHORT'].shift(1) < self.data[
                                                                     'SMA_LONG'].shift(1))))
        self.sell_signals['signal'] = (self.data['close']).where(((self.data['SMA_SHORT'] < self.data['SMA_LONG']) &
                                                                  (self.data['SMA_SHORT'].shift(1) > self.data[
                                                                      'SMA_LONG'].shift(1))))

        self.sell_signals = self.sell_signals.dropna()
        self.buy_signals = self.buy_signals.dropna()

    def strategy_return(self):

        buy = self.buy_signals
        buy['position'] = 1
        sell = self.sell_signals
        sell['position'] = -1
        merged = pd.concat([buy, sell]).sort_index()
        balance = 1
        buy = 0
        open_position = False
        for row in merged.values:
            if row[1] == 1:
                buy = row[0]
                open_position = True
            if row[1] == -1 and open_position:
                balance = balance + row[0] - buy
                buy = 0
                open_position = False
        return (balance - 1) / 1

    def hold_return(self):
        return (self.data['close'].take([-1]).iloc[0] - self.data['close'].take([0]).iloc[0]) / \
            self.data['close'].take([0]).iloc[0]

    def signal(self):
        previous_long = self.data['SMA_LONG'].take([-2]).iloc[0]
        previous_short = self.data['SMA_SHORT'].take([-2]).iloc[0]
        current_long = self.data['SMA_LONG'].take([-1]).iloc[0]
        current_short = self.data['SMA_SHORT'].take([-1]).iloc[0]

        if (previous_short > previous_long) and (current_short < current_long):
            return -1
        if (previous_short < previous_long) and (current_short > current_long):
            return 1
        return 0

    def tabulate(self, size=10) -> str:
        return self.data.head(size).to_string()


dm = DataMiner(units=Units.DAY, period=200)
d = dm.get_data()
sma = SimpleMovingAverage(data=d)
sma.calculate()
print(sma.tabulate(size=300))
print(sma.signal())
print(sma.strategy_return())
print(sma.hold_return())
sma.display()
