# -*- coding: utf-8 -*-
import common
import urllib
import httplib
import json


def sendRequest(authentication, params):
    """ Send POST request with the given parameters and return response.

    Arguments:
    apiKey -- private key given by the website
    apiCode -- private code given by the website
    pin -- the PIN number used in your account
    params -- dict with the parameters needed by the API method called

    """
    apiKey = authentication.key
    apiCode = authentication.code
    pin = authentication.pin

    params['tonce'] = common.getTonce()
    signature = common.createSignature(
        apiCode,
        params['method'],
        pin,
        params['tonce']
    )
    params = urllib.urlencode(params)
    header = common.createHeader(apiKey, signature)
    conn = httplib.HTTPSConnection(common.mbDomain)
    conn.request("POST", "/tapi/", params, header)
    response = conn.getresponse()
    response = json.load(response)
    try:
        data = common.parseResponse(response)
    except common.ResponseException, e:
        print str(e)
        data = None

    return data


def getAccountInfo(authentication):
    """Return the current balances of the account."""
    params = {
        'method': 'getInfo',
        'tonce': common.getTonce()
        }

    table = sendRequest(authentication, params)
    return common.AccountInfo(table)


def getOrderList(authentication, coin, orderType=None, status=None,
                 fromId=None, endId=None, since=None, end=None):
    """Return all the orders created that match the given filters."""
    params = {
        'method': 'OrderList',
        'tonce': common.getTonce()
        }

    if coin in common.mbCoins:
        params['pair'] = coin + "_brl"

    if orderType is not None and orderType in common.orderTypes:
        params['type'] = orderType

    if status is not None and status in common.orderStatuses:
        params['status'] = status

    if fromId is not None:
        params['from_id'] = str(fromId)

    if endId is not None:
        params['end_id'] = str(endId)

    if since is not None:
        params['since'] = str(since)

    if end is not None:
        params['end'] = str(end)

    orderList = []
    table = sendRequest(authentication, params)
    for orderId, data in table:
        orderList.append(common.Order(orderId, data))

    return orderList


def setOrder(authentication, coin, orderType, amount, price):
    """Create a buy or sell order."""
    params = {
      'method': 'Trade',
      'tonce': common.getTonce(),
      'volume': str(amount),
      'price': str(price)
      }

    if coin in common.mbCoins:
        params['pair'] = coin + "_brl"

    if orderType is not None and orderType in common.orderTypes:
        params['type'] = orderType

    table = common.sendRequest(authentication, params)
    orderId = table.keys()[0]
    return common.Order(orderId, table[orderId])


def cancelOrder(authentication, coin, orderId):
    """Cancel an order."""
    params = {
      'method': 'CancelOrder',
      'tonce': common.getTonce(),
      'order_id': str(orderId),
      }

    if coin in common.mbCoins:
        params['pair'] = coin + "_brl"

    table = common.sendRequest(authentication, params)
    orderId = table.keys()[0]
    return common.Order(orderId, table[orderId])
