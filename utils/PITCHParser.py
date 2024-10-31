
import pandas as pd


class PITCHMessageParser:
    def __init__(self):
        self.message_type_names = {
            'E': 'Executed Order',
            'A': 'Add Order',
            'P': 'Trade Order',
            'X': 'Cancelled Order'
        }

    def parse_message(self, message):
        session_letter = message[0]
        message_type = message[9]
        timestamp = message[1:8]
        order_id = message[10:22].strip()
        side = message[22]
        quantity = message[23:29].strip()
        stock_symbol = message[29:32].strip()
        price = message[32:42]
        display = message[42] if len(message) > 42 else None

        return {
            'Session Letter': session_letter,
            'Message Type': message_type,
            'Message Type Name': self.message_type_names.get(message_type, 'No message name'),
            'Timestamp': timestamp,
            'Order ID': order_id,
            'Side': side,
            'Quantity': quantity,
            'Stock Symbol': stock_symbol,
            'Price': price,
            'Display': display
        }

    def process_file(self, file_path):
        with open(file_path, 'r') as file:
            messages = [line.strip() for line in file.readlines()]
        parsed_messages = [self.parse_message(msg) for msg in messages]
        df = pd.DataFrame(parsed_messages)
        print(df)
        df.to_csv('parsed_messages.csv', index=False)
        print("Parsed messages saved to 'parsed_messages.csv'.")

    def group_file(self, parsed_file_path):
        output_file_path = 'grouped.csv'
        df = pd.read_csv(parsed_file_path)
        grouped_data = df.groupby('Stock Symbol')['Quantity'].sum().reset_index()
        grouped_data.to_csv(output_file_path, index=False)
        print("Grouped messages saved to 'grouped.csv'")

if __name__ == "__main__":
    parser = PITCHMessageParser()
    parser.process_file('../pitch_example_data')
    parser.group_file('parsed_messages.csv')
