from test_case import *


# 可以在此基础上进行任意的设计和修改
class TradeMonitor:
    def __init__(self):
        pass

    @staticmethod
    def find_symbol(trade):
        """
        根据trade找到相应的symbol
        :param trade:
        :return:
        """
        name = trade["name"]
        for symbol in Global_Data["symbols"]:
            if symbol.name == name:
                return symbol

    @staticmethod
    def find_trade(symbol):
        """
        根据symbol找到相应的group & exhcange
        :param symbol:
        :return:
        """
        group = symbol.group_name
        exchange = symbol.exchange_name
        for target_group in Global_Data["groups"]:
            if target_group.name == group:
                for target_exchange in Global_Data["exchanges"]:
                    if target_exchange.name == exchange:
                        return target_group, target_exchange

    def on_trade(self, trade):
        """
        发生交易, 并根据监控产生告警
        :param trade: 交易回报, 以dict形式表示
        :return:
        """
        # print(trade)
        # 根据trade, 找到对应的Symbol
        target_symbol = self.find_symbol(trade)
        # 根据symbol, 找到对应的Group和Exchange
        target_group, target_exchange = self.find_trade(target_symbol)
        # 初始化在每次交易后都要对symbol进行重新设定的列表
        symbol_reset = []
        # 对symbol进行监控
        # 先进行更新
        target_symbol.trade_update(trade)
        # 再进行判断是否产生告警
        alert_symbol = target_symbol.symbol_alert()
        if alert_symbol[0]:
            self.alarm(trade["time"], target_symbol.name)
        if alert_symbol[1]:
            self.alarm(trade["time"], target_symbol.name, atype='delta')
        symbol_reset += [target_symbol]
        # 对Group进行监控
        # 先进行更新
        target_group.trade_update(trade)
        # 进行判断是否产生告警
        alert_group = target_group.eg_alarm(
            [item for item in Global_Data["symbols"] if item.group_name == target_group.name])
        if alert_group[0]:
            # 如果针对group, quantity需要产生告警
            # 首先产生group的告警
            self.alarm(trade["time"], target_group.name)
            # 针对group的相关symbol告警
            for single_symbol in alert_group[2]:
                self.alarm(trade["time"], single_symbol.name)
        if alert_group[1]:
            # 如果针对group, delta需要产生告警
            # 首先产生group的告警
            self.alarm(trade["time"], target_group.name, atype='delta')
            # 针对group的相关symbol告警
            for single_symbol in alert_group[3]:
                self.alarm(trade["time"], single_symbol.name, atype='delta')
        symbol_reset += alert_group[2]
        symbol_reset += alert_group[3]
        # 对Exchange进行监控
        # 先进行更新
        target_exchange.trade_update(trade)
        alert_exchange = target_exchange.eg_alarm(
            [item for item in Global_Data["symbols"] if item.exchange_name == target_exchange.name])
        if alert_exchange[0]:
            # 如果针对exchange, quantity需要产生告警
            # 首先产生exchange的告警
            self.alarm(trade["time"], target_exchange.name)
            # 针对exchange的相关symbol告警
            for single_symbol in alert_exchange[2]:
                self.alarm(trade["time"], single_symbol.name)
        if alert_exchange[1]:
            # 如果针对exchange, delta需要产生告警
            # 首先产生exchange的告警
            self.alarm(trade["time"], target_exchange.name, atype='delta')
            # 针对exchange的相关symbol告警
            for single_symbol in alert_exchange[3]:
                self.alarm(trade["time"], single_symbol.name, atype='delta')
        symbol_reset += alert_exchange[2]
        symbol_reset += alert_exchange[3]
        # 这一轮交易更新完之后, 需要将symbol的inner_alert重新设回
        for item in symbol_reset:
            item.inner_alert_quantity = False
            item.inner_alert_delta = False

    @staticmethod
    def alarm(atime, name, atype='quantity'):
        alarm_msg = '累计成交量报警'
        if atype == 'delta':
            alarm_msg = '累计Delta报警'
        print(atime, name, alarm_msg)


if __name__ == "__main__":
    monitor = TradeMonitor()

    load_param_data1()
    load_trade_data1(monitor)

    load_param_data2()
    load_trade_data2(monitor)
