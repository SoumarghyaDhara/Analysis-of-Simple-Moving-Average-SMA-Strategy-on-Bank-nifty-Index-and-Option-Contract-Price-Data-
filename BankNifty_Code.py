from google.colab import drive
drive.mount('/content/drive'

import pandas as pd

class BankNiftyStrategy:
    def __init__(self, index_data_path, option_data_path):
        self.index_data = pd.read_csv('/content/drive/MyDrive/Nifty/banknifty_data.csv')
        self.option_data = pd.read_csv('/content/drive/MyDrive/Nifty/option_contract_data.csv')
        self.trades = []
        self.active_trade = None
        self.profit_threshold = 28
        self.loss_threshold = -20

    def execute_strategy(self):
        for index, row in self.index_data.iterrows():
            if self.active_trade:
                self.update_active_trade(row)
            else:
                if self.check_current_situation(row):
                    self.execute_trade(row)

    def check_current_situation(self, column):
        return column['<close>'] > column['SMA_value'] or column['SMA_value'] < column['<close>']

    def execute_trade(self, row):
        trade = Trade(row)
        self.active_trade = trade
        self.trades.append(trade)

    def update_active_trade(self, row):
        self.active_trade.update(row)

        # Enforce exact profit and loss thresholds
        if self.active_trade.profit >= 28:
            self.active_trade.exit_trade()
            self.active_trade = None
        elif self.active_trade.profit <= -20:
            self.active_trade.exit_trade()
            self.active_trade = None

    def save_trades_to_csv(self, filename):
        trade_records = []
        for trade in self.trades:
            trade_records.append(trade.get_trade_record())
        df = pd.DataFrame(trade_records)
        df.to_csv(filename, index=False)

class Trade:
    def __init__(self, entry_row):
        self.entry_time = entry_row['<time>']
        self.entry_price = entry_row['SMA_value']
        self.current_price = self.entry_price
        self.profit = 0

    def update(self, row):
        self.current_price = row['SMA_value']
        self.profit = self.current_price - self.entry_price

    def exit_trade(self):
        self.exit_time = self.entry_time
        self.exit_price = self.current_price

    def get_trade_record(self):
        return {
            'Entry Time': self.entry_time,
            'Entry Price': self.entry_price,
            'Exit Time': self.exit_time if hasattr(self, 'exit_time') else None,
            'Exit Price': self.exit_price if hasattr(self, 'exit_price') else None,
            'Profit': self.profit
        }

if __name__ == "__main__":
    strategy = BankNiftyStrategy('/content/drive/MyDrive/Nifty/v3bank_nifty_index_data.csv', '/content/drive/MyDrive/Nifty/v3bank_nifty_option_data.csv')
    strategy.execute_strategy()
    strategy.save_trades_to_csv('/content/drive/MyDrive/Nifty/v3trades.csv')
