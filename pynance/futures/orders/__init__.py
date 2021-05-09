from pynance.core.exceptions import PyNanceException
import time


class Orders(object):
    """Based on https://binance-docs.github.io/apidocs/futures/en/#new-order-trade

    Args:
        client: PyNance Client
    """
    def __init__(self, client):
        self.client = client

    def open(self, symbol=None):
        """Retrieves a collection of all open orders

        Warning
        If symbol is None the weight is 40

        Example
            client.orders.open() # or
            client.orders.open('LTCBTC')
        """
        endpoint = "https://fapi.binance.com/fapi/v1/openOrders"
        if symbol is None: _filter = {}
        else: _filter = {'symbol': symbol}
        data = self.client._get(endpoint, True, data=_filter)
        self.client.logger.info(f'Weight: {data.info["weight"]}')
        return data
    
    def create(self, 
        symbol:str=None, 
        market_type:str=None, 
        side:str=None,
        quantity:float=None,
        position:str=None, 
        timeInForce:str=None,
        reduceOnly:bool=False,
        price:float=0,
        stopPrice:float=None,
        closePosition:bool= False,
        activationPrice:float=None,
        callbackRate:float=None,
        workingType:str =None,
        priceProtect:bool = False,
        newOrderRespType:bool = False
    ):
        """Creates an open order in Binance Futures

        Args:
            symbol (str, required): [Target symbol].
            market_type (str, required): [Market Type, one of the following: ['LIMIT', 'MARKET', 'STOP', 'STOP_MARKET', 'TAKE_PROFIT', 'TAKE_PROFIT_MARKET', 'TRAILING_STOP_MARKET']]
            side (str, required): [BUY, SELL].
            quantity (float, optional): [Cannot be sent with closePosition=true(Close-All)]
            position (str, optional): [Default BOTH for One-way Mode ; LONG or SHORT for Hedge Mode. It must be sent in Hedge Mode.]. Defaults to BOTH.
            timeInForce (str, optional): [
                GTC - Good Till Cancel
                IOC - Immediate or Cancel
                FOK - Fill or Kill
                GTX - Good Till Crossing (Post Only)
            ]. Defaults to GTC.
            reduceOnly (bool, optional): ["true" or "false". default "false". Cannot be sent in Hedge Mode; cannot be sent with closePosition=true]. Defaults to False.
            price (float, optional): [Target price]. Defaults to 0.
            stopPrice (float, optional): [Used with STOP/STOP_MARKET or TAKE_PROFIT/TAKE_PROFIT_MARKET orders.]
            closePosition (bool, optional): [true, false；Close-All，used with STOP_MARKET or TAKE_PROFIT_MARKET.]. Defaults to False.
            activationPrice (float, optional): [Used with TRAILING_STOP_MARKET orders, default as the latest price(supporting different workingType)]
            callbackRate (float, optional): [Used with TRAILING_STOP_MARKET orders, min 0.1, max 5 where 1 for 1%]
            workingType (str, optional): [stopPrice triggered by: "MARK_PRICE", "CONTRACT_PRICE". Default "CONTRACT_PRICE"]
            priceProtect (bool, optional): ["TRUE" or "FALSE", default "FALSE". Used with STOP/STOP_MARKET or TAKE_PROFIT/TAKE_PROFIT_MARKET orders.]. Defaults to False.
            newOrderRespType (bool, optional): [False == "ACK", True == "RESULT", default "ACK"]. Defaults to False.

        Returns:
            [Response Object]: [PyNance response object]
        """
        endpoint = "https://fapi.binance.com/fapi/v1/order"
        if symbol is None: raise PyNanceException("Symbol is required")

        if market_type is None: raise PyNanceException("Market Type is required")
        if market_type.upper() not in ['LIMIT', 'MARKET', 'STOP', 'STOP_MARKET', 'TAKE_PROFIT', 'TAKE_PROFIT_MARKET', 'TRAILING_STOP_MARKET']:
            raise PyNanceException("Market type has to be one of the following: ['LIMIT', 'MARKET', 'STOP', 'STOP_MARKET', 'TAKE_PROFIT', 'TAKE_PROFIT_MARKET', 'TRAILING_STOP_MARKET']")

        if side is None: raise PyNanceException("Side is required")
        if side is not None and side.upper() not in ['BUY', 'SELL']: raise PyNanceException("SIDE has to be either BUY or SELL.")

        _filter = {'symbol': symbol, 'type': market_type.upper(), 'side': side.upper()}

        if position is not None and position.upper() not in ['BOTH', 'LONG', 'SHORT']: raise PyNanceException("Default BOTH for One-way Mode ; LONG or SHORT for Hedge Mode. It must be sent in Hedge Mode.")
        if position is not None: _filter['positionSide'] = position.upper()

        if timeInForce is not None and timeInForce.upper() not in ['GTC', 'IOC', 'FOK', 'GTX']: raise PyNanceException("timeInForce needs to be one of the following: ['GTC', 'IOC', 'FOK', 'GTX']")
        if timeInForce is not None: _filter['timeInForce'] = timeInForce.upper()

        if not closePosition and quantity is not None: _filter['quantity'] = float(quantity)
        elif closePosition: _filter['closePosition'] = closePosition

        if reduceOnly: _filter['reduceOnly'] = reduceOnly
        
        if market_type in ['STOP', 'STOP_MARKET', 'TAKE_PROFIT', 'TAKE_PROFIT_MARKET'] and stopPrice is None:
            raise PyNanceException("stopPrice is required when using the following markets: ['STOP', 'STOP_MARKET', 'TAKE_PROFIT', 'TAKE_PROFIT_MARKET']")
        if stopPrice is not None: _filter['stopPrice'] = float(stopPrice)

        if activationPrice is not None: _filter['activationPrice'] = float(activationPrice)

        if market_type in ['TRAILING_STOP_MARKET'] and callbackRate is None:
            raise PyNanceException("callbackRate is required when using the following markets: ['TRAILING_STOP_MARKET']. Min 0.1 max 5 where 1 == 1%")
        if market_type in ['TRAILING_STOP_MARKET'] and callbackRate is not None and callbackRate >= 0.01 and callbackRate <= 5: _filter['callbackRate'] = float(callbackRate)
        elif market_type in ['TRAILING_STOP_MARKET'] and callbackRate is None: raise PyNanceException('callbackRate has to be between 0.01 and 5')
        
        if workingType is not None and workingType.upper() not in ['MARK_PRICE', 'CONTRACT_PRICE']: raise PyNanceException("stopPrice triggered by: 'MARK_PRICE', 'CONTRACT_PRICE'. Default 'CONTRACT_PRICE'")
        if workingType is not None and workingType != "CONTRACT_PRICE": _filter['workingType'] = workingType.upper()

        if market_type in ['STOP', 'STOP_MARKET', 'TAKE_PROFIT', 'TAKE_PROFIT_MARKET'] and priceProtect:
            _filter['priceProtect'] = "TRUE"

        if newOrderRespType: _filter['newOrderRespType'] = "RESULT"

        data = self.client._post(endpoint=endpoint, signed=True, force_params=False, data=_filter)
        self.client.logger.info(f'Weight: {data.info["weight"]}')
        return data
