# -*- coding: utf-8 *-*
import httplib
import json
import common


def getTicker(coin, connection=None):
    """
    Returns a unicode dict of numbers in the following arrangement:
    {
      "ticker": {
        "high": Highest traded price (BRL) today,
        "low": Lowest traded price (BRL) today,
        "vol": Amount of coins (LTC or BTC) traded today,
        "last": Price (BRL) of the last transaction,
        "buy": Current highest price (BRL) offered by people buying,
        "sell": Current lowest price (BRL) offered by poeple selling,
        "date": timestamp of the last ticker update
      }
    }
    """
    headers = {"Content-type": "application/x-www-form-urlencoded"}

    if connection is None:
        connection = httplib.HTTPSConnection(common.mbDomain)

    address = "/api/ticker/"
    if coin == 'ltc':
        address = address[:-1] + "_litecoin" + address[-1:]

    connection.request("GET", address, "", headers)
    response = connection.getresponse()
    output = json.load(response)
    return common.convert(output)


def getOrderBook(coin, connection=None):
    """
    Returns a unicode dict of lists of lists in the following arrangement
    {
      "asks": list of the selling offers available.
      "bids": list of the buying offers available.
    }
    Where each offer is a list of two elements [price per unit, amount]
    """
    headers = {"Content-type": "application/x-www-form-urlencoded"}

    if connection is None:
        connection = httplib.HTTPSConnection(common.mbDomain)

    address = "/api/orderbook/"
    if coin == 'ltc':
        address = address[:-1] + "_litecoin" + address[-1:]

    connection.request("GET", address, "", headers)
    response = connection.getresponse()
    output = json.load(response)
    return common.convert(output)


def getTrades(coin, timeBegin=None, timeEnd=None, connection=None):
    """
    Returns a unicode list of dicts in the following arrangement
    [
      {
        "date": Timestamp of the transaction,
        "price": Price (BRL) per unit of coin (LTC or BTC),
        "amount": Amount of coin (LTC or BTC),
        "tid": Transaction ID,
        "type": 'buy' or 'sell'
      }
     ]
    """
    headers = {"Content-type": "application/x-www-form-urlencoded"}

    if connection is None:
        connection = httplib.HTTPSConnection(common.mbDomain)

    address = "/api/trades/"
    if coin == 'ltc':
        address = address[:-1] + "_litecoin" + address[-1:]

    if timeBegin is not None:
        address = address[:-1] + str(timeBegin) + address[-1:]
        if timeEnd is not None:
            address = address[:-1] + str(timeEnd) + address[-1:]

    connection.request("GET", address, "", headers)
    response = connection.getresponse()
    output = json.load(response)
    return common.convert(output)

print(str(getTicker('btc')))
