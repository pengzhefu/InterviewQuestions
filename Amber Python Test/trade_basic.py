#!/usr/bin/evn python
# -*- coding: utf-8 -*-


class TradeBase:
    def __init__(self):
        self.name = "base class"
        self.quantity_interval = 20
        self.delta_interval = 20
        self.quantity_limit = 0
        self.delta_limit = 0
        # 存放最新quantity_interval的交易的quantity记录
        self.quantity_record = []
        # 存放最新delta_interval内的交易的delta记录
        self.delta_record = []

    def trade_update(self, trade):
        """
        根据trade更新symbol的交易记录
        :param trade: 交易回报, 以dict形式表示
        :return:
        """
        # 更新quantity_record
        self.quantity_record = list(
            filter(lambda x: x[0] >= (trade["time"] - self.quantity_interval),
                   self.quantity_record)
        )
        self.quantity_record.append(
            (trade["time"],
             trade["quantity"]
             )
        )
        # 更新delta_record
        self.delta_record = list(
            filter(lambda x: x[0] >= (trade["time"] - self.delta_interval),
                   self.delta_record)
        )
        self.delta_record.append((trade["time"],
                                  (trade["price"] if trade["side"].startswith("B") else -trade["price"]) * (
                                  trade['quantity'])))

    def eg_alarm(self, symbol_list=None):
        """
        针对group和exchange进行是否产生告警的判断
        :param symbol_list: 和group或者exchange相关的symbol列表
        :return: 四元组: 是否产生quantity告警, 是否产生delta告警, quantity告警的symbol列表, delta告警的symbol列表
        """
        # 判断是否产生告警
        quantity_val = sum([item[1] for item in self.quantity_record])
        delta_val = sum([item[1] for item in self.delta_record])
        quantity_alert = False
        delta_alert = False
        symbol_alert_quantity_list = list()
        symbol_alert_delta_list = list()
        if quantity_val >= self.quantity_limit:
            quantity_alert = True
        if abs(delta_val) >= self.delta_limit:
            delta_alert = True
        if symbol_list:
            for symbol in symbol_list:
                if quantity_alert:
                    if not symbol.inner_alert_quantity:
                        symbol_alert_quantity_list.append(symbol)
                        # 设为已调用过
                        symbol.inner_alert_quantity = True
                if delta_alert:
                    if not symbol.inner_alert_delta:
                        symbol_alert_delta_list.append(symbol)
                        # 设为已调用过
                        symbol.inner_alert_delta = True
        return quantity_alert, delta_alert, symbol_alert_quantity_list, symbol_alert_delta_list
