import io
from collections import defaultdict, OrderedDict
import PitchOrder
from PitchOrder import PitchOrder


class volumeCalcHelpers:
    open_orders = {}  # track OPEN ORDERS by ORDER ID
    volumes = defaultdict(int)  # track EXECUTED VOLUME by SYMBOL

    @staticmethod
    def read_pitch_file(path):
        with io.open(path, 'r') as reader:  # open PITCH file
            for order_line in reader:
                print(order_line)
                message_type = order_line[9]  # get Message Type
                if message_type == 'P':  # check for TRADE ORDERS
                    trade_message = volumeCalcHelpers.parse_add_or_trade_order(order_line)
                    volumeCalcHelpers.update_volume_map(trade_message)  # update executed VOLUME of SYMBOL
                elif message_type == 'E' or message_type == 'X':
                    order = volumeCalcHelpers.parse_execute_or_cancel_order(order_line)
                if message_type == 'E':  # order was EXECUTED
                    volumeCalcHelpers.update_open_order_map(order, True)  # update open order map with new executed order
                else:  # order was CANCELLED
                    volumeCalcHelpers.update_open_order_map(order, False)  # update open order map with cancelled order

        return volumeCalcHelpers.get_top_volumes()

    @staticmethod
    def parse_add_or_trade_order(order_line):
        order = PitchOrder()
        order.timestamp = order_line[:8]
        order.message_type = order_line[9]
        order.order_id = order_line[10:22]
        order.side_indicator = order_line[23]
        order.shares = int(order_line[24:30])
        order.symbol = order_line[:order_line.find(' ')]
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
        print(top_volumes)
        return top_volumes

if __name__ == "__main__":
    VCH = volumeCalcHelpers()
    VCH.read_pitch_file('pitch_example_data')

