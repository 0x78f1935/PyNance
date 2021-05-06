from pynance.core.exceptions import PyNanceException


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
        self.client.logger.info(f'Weight: Weight: {data.info["weight"]} / 1200')
        return data
    
    # def create(self, 
    #     symbol:str=None, 
    #     quantity:float=None,
    #     order_type:str="",
    #     buy:bool=True, 
    #     time_in_force:str="GTC",
    #     reduce_only:bool=False,
    #     price:str="",
    #     newClientOrderId:str="",
    #     stopPrice:str="",
    #     workingType:str="",
    #     closePosition:str="",
    #     positionSide:str="",
    #     callbackRate:str="",
    #     activationPrice:str="",
    #     newOrderRespType:str="",
    # ):
    #     """This method is able to create different kind of buy/sell order

    #     Args:
    #         symbol (str, required): [Target symbol].
    #         quantity (float, required): [Total quantity].
    #         order_type (str, required): [Market type to place order in].
    #             ['LIMIT', 'MARKET', 'STOP', 'STOP_MARKET', 'TAKE_PROFIT', 'TAKE_PROFIT_MARKET', 'TRAILING_STOP_MARKET']
    #         buy (bool, optional): [Indicates to place a buy order or a sell order]. Defaults to True.
    #         time_in_force (str, optional): [Order behavious]. Defaults to "GTC".
    #             GTC - Good Till Cancel
    #             IOC - Immediate or Cancel
    #             FOK - Fill or Kill
    #             GTX - Good Till Crossing (Post Only)
    #         reduce_only (boolean, optional): [ "true" or "false". default "false". Cannot be sent in Hedge Mode; cannot be sent with closePosition=true]. Defaults to False.
    #         price (str, optional): [description]. Defaults to "".
    #         newClientOrderId (str, optional): [description]. Defaults to "".
    #         stopPrice (str, optional): [description]. Defaults to "".
    #         workingType (str, optional): [description]. Defaults to "".
    #         closePosition (str, optional): [description]. Defaults to "".
    #         positionSide (str, optional): [description]. Defaults to "".
    #         callbackRate (str, optional): [description]. Defaults to "".
    #         activationPrice (str, optional): [description]. Defaults to "".
    #         newOrderRespType (str, optional): [description]. Defaults to "".

    #         Type	Additional mandatory parameters
    #         LIMIT	timeInForce, quantity, price
    #         MARKET	quantity
    #         STOP/TAKE_PROFIT	quantity, price, stopPrice
    #         STOP_MARKET/TAKE_PROFIT_MARKET	stopPrice
    #         TRAILING_STOP_MARKET	callbackRate
    #     """
    #     if symbol is None or quantity is None: raise PyNanceException("Asset and quantity are required")
    #     if order_type.upper() not in ['LIMIT', 'MARKET', 'STOP', 'STOP_MARKET', 'TAKE_PROFIT', 'TAKE_PROFIT_MARKET', 'TRAILING_STOP_MARKET']:
    #         raise PyNanceException("order_type has to be one of the following: ['LIMIT', 'MARKET', 'STOP', 'STOP_MARKET', 'TAKE_PROFIT', 'TAKE_PROFIT_MARKET', 'TRAILING_STOP_MARKET']")
        
        
    #     endpoint = "https://fapi.binance.com/fapi/v1/openOrders"
    #     data = self.client._post(
    #         endpoint,
    #         True,
    #         data={
    #             'symbol': symbol,
    #             'quantity': quantity
    #         }
    #     )
    #     self.client.logger.info(f'Weight: Weight: {data.info["weight"]} / 1200')
    #     return data