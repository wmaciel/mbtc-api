# -*- coding: utf-8 *-*
import httplib
import json
import common


def getTicker(coin):
    """ Return the ticker information of the current state of the exchange.

    The ticker contains a summary of the current state of the exchange for a
    given coin.
    This information is given  as a dict in the following arrangement:
    {
      "ticker": {
        "high": Highest traded price (BRL) today,
        "low": Lowest traded price (BRL) today,
        "vol": Amount of coins (LTC or BTC) traded today,
        "last": Price (BRL) of the last transaction,
        "buy": Current highest price (BRL) offered by people buying,
        "sell": Current lowest price (BRL) offered by people selling,
        "date": timestamp of the last ticker update
      }
    }

    Arguments:
    coin -- "btc" or "ltc", defines which coin the info is about

    """
    headers = {"Content-type": "application/x-www-form-urlencoded"}

    connection = httplib.HTTPSConnection(common.mbDomain)

    address = "/api/ticker/"
    if coin == 'ltc':
        address = address[:-1] + "_litecoin" + address[-1:]

    connection.request("GET", address, "", headers)
    response = connection.getresponse()
    output = json.load(response)
    return common.convert(output)


def getOrderBook(coin):
    """Return the active orders for the given coin

    The orders are given as a dict of lists of lists in the following
    arrangement
    {
      "asks": list of the selling offers available.
      "bids": list of the buying offers available.
    }
    Where each offer is a list of two elements [price per unit, amount]

    Arguments:
    coin -- "btc" or "ltc", defines which coin the info is about

    """
    headers = {"Content-type": "application/x-www-form-urlencoded"}

    connection = httplib.HTTPSConnection(common.mbDomain)

    address = "/api/orderbook/"
    if coin == 'ltc':
        address = address[:-1] + "_litecoin" + address[-1:]

    connection.request("GET", address, "", headers)
    response = connection.getresponse()
    output = json.load(response)
    return common.convert(output)


def getTrades(coin, timeBegin=None, timeEnd=None):
    """ Return the history of trades of a given coin in a period of time

    The history of the transactions is given as a list of dicts in the
    following arrangement:
    [
      {
        "date": Timestamp of the transaction,
        "price": Price (BRL) per unit of coin (LTC or BTC),
        "amount": Amount of coin (LTC or BTC),
        "tid": Transaction ID,
        "type": 'buy' or 'sell'
      }
    ]

    Arguments:
    coin -- "btc" or "ltc", defines which coin the info is about
    timeBegin -- (optional) Timestamp of the beginning of the wanted history
    timeEnd -- (optional) Timestamp of the end of the wanted history

    """
    headers = {"Content-type": "application/x-www-form-urlencoded"}

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
