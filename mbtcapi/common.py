# -*- coding: utf-8 -*-
import time
import hmac
import hashlib

mbDomain = "www.mercadobitcoin.com.br"

mbCoins = ["btc", "ltc"]

orderStatuses = ['active', 'canceled', 'completed']

orderTypes = ["buy", "sell"]


class ResponseError(StandardError):
    pass


def convert(input):
    """Convert unicode strings into utf-8 inside lists and dicts

    This function was created by stack overflow user Mark Amery
    (http://stackoverflow.com/users/1709587/mark-amery) and published on the
    thread http://goo.gl/sNy4xP

    """
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


def getTonce():
    """Return a tonce to be used in the signature for authentication

    More information about tonces in
    https://en.bitcoin.it/wiki/MtGox/API/HTTP#tonce_and_nonce

    """
    return str(int(time.time()))


def createSignature(apiCode, method, pin, tonce):
    """Generate the required authentication signature to be placed on header"""
    H = hmac.new(apiCode, digestmod=hashlib.sha512)
    H.update(method + ':' + pin + ':' + tonce)
    signature = H.hexdigest()
    return signature


def createHeader(apiKey, signature):
    """Generate the header to be placed on the POST request"""
    return {
        "headers-type": "application/x-www-form-urlencoded",
        "Key": apiKey,
        "Sign": signature
        }


def parseResponse(response):
    """Parse the response dict removing unwanted information."""
    response = convert(response)
    if response['success'] == 0:
        raise ResponseError(response['error'])
    else:
        return response['return']


class Operation:

    """Define an operation.

    An Operation is the actual transaction of coins. It is created when an
    order is fully or partially executed. Therefore, operations are final and
    cannot be canceled or reversed.

    Attributes:
    id -- Identificatin number
    volume -- Amount of coin moved
    price -- Price (BRL) per unit of coin
    rate -- Fee (%) charged
    created -- Timestamp from when the operation occured

    """

    def __init__(self, table):
        """Constructor"""
        self.buildFromTable(table)

    def buildFromTable(self, operationId, table):
        """Read table and fetch the necessary infrmation"""
        self.id = operationId
        self.volume = table['volume']
        self.price = table['price']
        self.rate = table['rate']
        self.created = table['created']


class Order:

    """Define an order.

    An order is an offer of either buying or selling coins. The creation of an
    order does not mean the immediate execution of the transaction.

    Attributes:
    id -- Identification number
    status -- 'active', 'canceled' or 'completed'
    created -- Timestamp from when the order was created
    price -- Price (BRL) per unit of coin
    volume -- Amount of coin
    pair -- Type of coin, may be 'btc_brl' or 'ltc_brl'
    type -- Type or order, may be 'sell' or 'buy'
    operations -- List of executed operations

    """

    def __init__(self, table):
        """Constructor"""
        self.buildFromTable(table)

    def buildFromTable(self, table):
        """Read table and fetch the necessary infrmation."""
        self.id = list(table.keys())[0]
        data = table[self.id]
        self.status = data['status']
        self.created = data['created']
        self.price = data['price']
        self.volume = data['colume']
        self.pair = data['pair']
        self.type = data['type']

        #Create list of operations
        opTable = data['operations']
        self.operations = []
        for opID, opData in list(opTable.items()):
            self.operations.append(Operation(opID, opData))


class AccountInfo:

    """Define the state of an account.

    The state of the account if given by it's balances in all three supported
    currencies i.e. brl, btc and ltc as well as the number of orders not yet
    fully executed.

    Attributes:
    btc -- Bitcoin balance
    ltc -- Litecoin balance
    brl -- Brazillian Real balance
    numOrders -- Number of open orders
    time -- Timestamp of the moment this information was fetched

    """

    def __init__(self, table):
        """Constructor"""
        self.buildFromTable(table)

    def buildFromTable(self, table):
        """Read table and fetch the necessary infrmation."""
        self.btc = table['funds']['btc']
        self.ltc = table['funds']['ltc']
        self.brl = table['funds']['brl']
        self.time = table['server_time']
        self.numOrders = table['open_orders']