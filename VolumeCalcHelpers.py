import io
from collections import defaultdict, OrderedDict
#import PitchOrder
#from PitchOrder import PitchOrder
import logging

class volumeCalcHelpers:
    open_orders = {}  # track OPEN ORDERS by ORDER ID
    volumes = defaultdict(int)  # track EXECUTED VOLUME by SYMBOL


    # Configure the logger
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Use the logger

    @staticmethod
    def read_pitch_file(path):
        with io.open(path, 'r') as reader:  # open PITCH file
            for order_line in reader:
                logging.debug("Simulated order raw: %s", order_line)
                message_type = order_line[9] # get Message Type
                logging.debug("Message type letter: %s", message_type)
                match message_type:
                    case 'A':
                        logging.debug("Add Order")
                        add_order = volumeCalcHelpers.parse_add_or_trade_order(order_line)
                    case 'P':  # check for TRADE ORDERS
                        logging.debug("Trade Order")
                        trade_message = volumeCalcHelpers.parse_add_or_trade_order(order_line)
                        volumeCalcHelpers.update_volume_map(trade_message)  # update executed VOLUME of SYMBOL
                    case 'E':
                        logging.debug("Execution Order")
                    case 'X':
                        logging.debug("Canceled Order")
                        order = volumeCalcHelpers.parse_execute_or_cancel_order(order_line)
                    case _ :
                        logging.debug("Warning: unrecognized message type %s", message_type )

        return volumeCalcHelpers.get_top_volumes()

    @staticmethod
    def parse_add_or_trade_order(order_line):
        order = pitchOrder()
        order.timestamp = order_line[:8]
        order.message_type = order_line[9]
        order.order_id = order_line[10:22]
        order.side_indicator = order_line[23]
        #order.shares = int(order_line[24:30])
        order.shares = order_line[23:29].lstrip("0")
        #order.symbol = order_line[:order_line.find(' ')]
        order.symbol = order_line[29:35]
        logging.debug("Order Shares: %s" , order.shares)
        logging.debug("Order Symbol: %s", order.symbol)

        return order

    @staticmethod
    def parse_execute_or_cancel_order(order_line):
        order = pitchOrder()
        order.timestamp = order_line[:8]
        order.message_type = order_line[9]
        order.order_id = order_line[10:22]
        order.shares = int(order_line[23:29])

        return order

    @staticmethod
    def update_volume_map(update_volume):
        if update_volume.symbol in volumeCalcHelpers.volumes:
            volumeCalcHelpers.volumes[update_volume.symbol] += update_volume.shares
        else:
            volumeCalcHelpers.volumes[update_volume.symbol] = update_volume.shares

    @staticmethod
    def update_open_order_map(order, executed):
        if order.order_id in volumeCalcHelpers.open_orders and volumeCalcHelpers.open_orders[order.order_id].shares >= order.shares:
            if executed:  # order was EXECUTED instead of CANCELLED
                update_volume = pitchOrder()
                update_volume.symbol = volumeCalcHelpers.open_orders[order.order_id].symbol
                volumeCalcHelpers.update_volume_map(update_order)
                remaining_shares = volumeCalcHelpers.open_orders[order.order_id].shares - order.shares
            if remaining_shares > 0:
                volumeCalcHelpers.open_orders[order.order_id].shares = remaining_shares
            else:
                del volumeCalcHelpers.open_orders[order.order_id]
        else:  # order was CANCELLED
            del volumeCalcHelpers.open_orders[order.order_id]

    @staticmethod
    def get_top_volumes():
        top_volumes = OrderedDict(sorted(volumeCalcHelpers.volumes.items(), key=lambda x: x[1], reverse=True))
        if len(top_volumes) > 10:
            top_volumes = list(top_volumes.items())[:10]
        #logging.debug(top_volumes)
        return top_volumes

class pitchOrder:
    def __init__(self):
        self.timestamp = None
        self.message_type = None
        self.order_id = None
        self.shares = 0
        self.symbol = None

if __name__ == "__main__":
    VCH = volumeCalcHelpers()
    VCH.read_pitch_file('pitch_example_data')

