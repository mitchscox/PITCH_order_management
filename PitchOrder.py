# Pitch order object definition
%s
class PitchOrder:
    def __init__(self):
        self.timestamp = None
        self.order_id = None
        self.shares = 0
        self.message_type = None
        self.side_indicator = None
        self.symbol = None

    @property
    def side_indicator(self):
        return self.side_indicator

    @side_indicator.setter
    def side_indicator(self, value):
        self.side_indicator = value

    @property
    def symbol(self):
        return self.symbol

    @symbol.setter
    def symbol(self, value):
        self.symbol = value

    @property
    def message_type(self):
        return self.message_type

    @message_type.setter
    def message_type(self, value):
        self.message_type = value

    @property
    def timestamp(self):
        return self.timestamp

    @timestamp.setter
    def timestamp(self, value):
        self.timestamp = value

    @property
    def order_id(self):
        return self.order_id

    @order_id.setter
    def order_id(self, value):
        self.order_id = value

    @property
    def shares(self):
        return self.shares

    @shares.setter
    def shares(self, value):
        self.shares = value
