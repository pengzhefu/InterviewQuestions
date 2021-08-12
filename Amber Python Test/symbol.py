# 可以在此基础上进行任意的设计和修改
from trade_basic import TradeBase


class Symbol(TradeBase):
    def __init__(self, name, exchange_name, group_name, quantity_limit, quantity_interval, delta_limit, delta_interval):
        super(Symbol, self).__init__()
        self.name = name
        self.exchange_name = exchange_name
        self.group_name = group_name
        self.quantity_limit = quantity_limit
        self.quantity_interval = quantity_interval
        self.delta_limit = delta_limit
        self.delta_interval = delta_interval
        # 表示symbol最近是否自己触发过quantity告警, 默认False
        self.__inner_alert_quantity = False
        # 表示symbol最近是否自己触发过delta告警, 默认False
        self.__inner_alert_delta = False

    def symbol_alert(self):
        quantity_val = sum([item[1] for item in self.quantity_record])
        delta_val = sum([item[1] for item in self.delta_record])
        # 更新自己是否调用过
        if quantity_val >= self.quantity_limit:
            self.__inner_alert_quantity = True
        if abs(delta_val) >= self.delta_limit:
            self.__inner_alert_delta = True
        return self.inner_alert_quantity, self.inner_alert_delta

    @property
    def inner_alert_delta(self):
        return self.__inner_alert_delta

    @inner_alert_delta.setter
    def inner_alert_delta(self, value):
        if isinstance(value, bool):
            self.__inner_alert_delta = value
        else:
            raise TypeError("To set inner alert, type should be Boolean")

    @property
    def inner_alert_quantity(self):
        return self.__inner_alert_quantity

    @inner_alert_quantity.setter
    def inner_alert_quantity(self, value):
        if isinstance(value, bool):
            self.__inner_alert_quantity = value
        else:
            raise TypeError("To set inner alert, type should be Boolean")
