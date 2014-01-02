# -*- coding: utf-8 -*-

import time
import hmac
import hashlib

mbDomain = "www.mercadobitcoin.com.br"

mbCoins = ["btc", "ltc"]

orderStatuses = ['active', 'canceled', 'completed']

orderTypes = ["buy", "sell"]


def convert(input):
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


def getTonce():
    return str(int(time.time()))


def createSignature(apiCode, method, pin, tonce):
    H = hmac.new(apiCode, digestmod=hashlib.sha512)
    H.update(method + ':' + pin + ':' + tonce)
    signature = H.hexdigest()
    return signature


def createHeader(apiKey, signature):
    return {
        "headers-type": "application/x-www-form-urlencoded",
        "Key": apiKey,
        "Sign": signature
        }


def parseResponse(response):
    response = convert(response)
    if response['success'] == 0:
        return response['error']
    else:
        return response['return']


class Operation:

    def __init__(self, table):
        self.buildFromTable(table)

    def buildFromTable(self, operationId, table):
        self.id = operationId
        self.volume = table['volume']
        self.price = table['price']
        self.rate = table['rate']
        self.created = table['created']


class Order:

    def __init__(self, table):
        self.buildFromTable(table)

    def buildFromTable(self, table):
        self.id = list(table.keys())[0]
        data = table[self.id]
        self.status = data['status']
        self.created = data['created']
        self.price = data['price']
        self.volume = data['colume']
        self.pair = data['pair']
        self.type = data['type']

        #Creates list of operations
        opTable = data['operations']
        self.operations = []
        for opID, opData in list(opTable.items()):
            self.operations.append(Operation(opID, opData))


class AccountInfo:

    def __init__(self, table):
        self.buildFromTable(self, table)

    def buildFromTable(self, table):
        self.btc = table['funds']['btc']
        self.ltc = table['funds']['ltc']
        self.brl = table['funds']['brl']
        self.time = table['server_time']
        self.numOrders = table['open_orders']