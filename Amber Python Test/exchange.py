# 可以在此基础上进行任意的设计和修改
from trade_basic import TradeBase


class Exchange(TradeBase):
    def __init__(self, name, quantity_limit, quantity_interval, delta_limit, delta_interval):
        super(Exchange, self).__init__()
        self.name = name
        self.quantity_limit = quantity_limit
        self.quantity_interval = quantity_interval
        self.delta_limit = delta_limit
        self.delta_interval = delta_interval
