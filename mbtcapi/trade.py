# -*- coding: utf-8 -*-
import common
import urllib
import httplib
import json


def sendRequest(apiKey, apiCode, pin, params):
    params['tonce'] = common.getTonce()
    params = urllib.urlencode(params)
    signature = common.createSignature(
        apiCode,
        params['method'],
        pin,
        params['tonce']
    )
    header = common.createHeader(apiKey, signature)
    conn = httplib.HTTPSConnection(common.mbDomain)
    conn.request("POST", "/tapi/", params, header)
    response = conn.getresponse()
    return json.load(response)


def getAccountInfo(apiKey, apiCode, pin):
    params = {
        'method': 'getInfo',
        'tonce': common.getTonce()
        }
    return sendRequest(apiKey, apiCode, pin, params)



def getOrderList(apiKey, apiCode, pin, coin, orderType=None, status=None,
                 fromId=None, endId=None, since=None, end=None):
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

    return sendRequest(apiKey, apiCode, pin, params)


def setOrder(apiKey, apiCode, pin, coin, orderType, amount, price):
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

    return common.sendRequest(apiKey, apiCode, pin, params)


def cancelOrder(apiKey, apiCode, pin, coin, orderId):
    params = {
      'method': 'CancelOrder',
      'tonce': common.getTonce(),
      'order_id': str(orderId),
      }

    if coin in common.mbCoins:
        params['pair'] = coin + "_brl"

    return common.sendRequest(apiKey, apiCode, pin, params)
