from abc import ABC


class TFMA(ABC):

    def signals(self):
        ...

    def strategy_return(self):
        ...
