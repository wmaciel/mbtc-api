# -*- coding: utf-8 -*-
import common
import urllib
import httplib
import json

mbTradeAPIKey = ''
mbTradeAPICode = ''
PIN = ''


def sendRequest(apiKey, apiCode, pin, params):
    """ Send POST request with the given parameters and return response.

    Arguments:
    apiKey -- private key given by the website
    apiCode -- private code given by the website
    pin -- the PIN number used in your account
    params -- dict with the parameters needed by the API method called

    """
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
    """Return the current balances of the account."""
    method = 'getInfo'
    tonce = common.getTonce()
    params = {'method': method, 'tonce': tonce}
    params = urllib.urlencode(params)
    signature = common.createSignature(apiCode, method, pin, tonce)
    header = common.createHeader(apiKey, signature)
    conn = httplib.HTTPSConnection("www.mercadobitcoin.com.br")
    conn.request("POST", "/tapi/", params, header)
    response = conn.getresponse()
    return json.load(response)


def getOrderList(apiKey, apiCode, pin, coin, orderType=None, status=None,
                 fromId=None, endId=None, since=None, end=None):
    """Return all the orders created that match the given filters."""
    method = 'OrderList'
    tonce = common.getTonce()
    params = {'method': method, 'tonce': tonce}

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

    params = urllib.urlencode(params)
    signature = common.createSignature(apiCode, method, pin, tonce)
    header = common.createHeader(apiKey, signature)
    conn = httplib.HTTPSConnection("www.mercadobitcoin.com.br")
    conn.request("POST", "/tapi/", params, header)
    response = conn.getresponse()
    return json.load(response)


def setOrder(apiKey, apiCode, pin, coin, orderType, amount, price):
    """Create a buy or sell order."""
    method = 'Trade'
    tonce = common.getTonce()
    params = {
      'method': method,
      'tonce': tonce,
      'volume': str(amount),
      'price': str(price)
      }

    if coin in common.mbCoins:
        params['pair'] = coin + "_brl"

    if orderType is not None and orderType in common.orderTypes:
        params['type'] = orderType

    params = urllib.urlencode(params)
    signature = common.createSignature(apiCode, method, pin, tonce)
    header = common.createHeader(apiKey, signature)
    conn = httplib.HTTPSConnection("www.mercadobitcoin.com.br")
    conn.request("POST", "/tapi/", params, header)
    response = conn.getresponse()
    return json.load(response)


def cancelOrder(apiKey, apiCode, pin, coin, orderId):
    """Cancel an order."""
    method = 'CancelOrder'
    tonce = common.getTonce()
    params = {
      'method': method,
      'tonce': tonce,
      'order_id': str(orderId),
      }

    if coin in common.mbCoins:
        params['pair'] = coin + "_brl"

    params = urllib.urlencode(params)
    signature = common.createSignature(apiCode, method, pin, tonce)
    header = common.createHeader(apiKey, signature)
    conn = httplib.HTTPSConnection("www.mercadobitcoin.com.br")
    conn.request("POST", "/tapi/", params, header)
    response = conn.getresponse()
    return json.load(response)
