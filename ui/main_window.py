from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout
from trading.websocket_client import PriceSocket
from trading.order_manager import OrderManager
from trading.krw_worker import RateWorker

class MainWindow(QWidget):
    def __init__(self, client):
        super().__init__()
        self.usdt_krw = 0
        self.rate_worker = RateWorker()
        self.rate_worker.rate_updated.connect(self.update_rate)
        self.rate_worker.start()

        self.client = client
        self.order_manager = OrderManager(self.client)

        #setting table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Symbol", "Amount", "Entry", "PNL_USDT", "PNL_KRW", "Action"])

        self.refresh_button = QPushButton("Postion refresh")
        self.refresh_button.clicked.connect(self.load_positions)

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(self.refresh_button)
        self.setLayout(layout)
        
        self.sockets = []
        self.load_positions()

    def load_positions(self):
        raw_positions = self.order_manager.get_positions()
        self.positions = {}
        self.row_map = {}

        self.table.setRowCount(len(raw_positions))

        for i, p in enumerate(raw_positions):
            symbol = p['symbol']
            amount = float(p['amount'])
            
            #positive -> long position  negative -> short
            side = "LONG" if amount > 0 else "SHORT"

            self.positions[symbol] = p
            self.row_map[symbol] = i

            self.table.setItem(i, 0, QTableWidgetItem(symbol))
            self.table.setItem(i, 1, QTableWidgetItem(str(amount)))
            self.table.setItem(i, 2, QTableWidgetItem(str(p['entryPrice'])))
            self.table.setItem(i, 3, QTableWidgetItem(str(p['unRealizedProfit'])))
            self.table.setItem(i, 4, QTableWidgetItem("0 WON"))

            #add button final col
            close_btn = QPushButton("close")
            close_btn.setStyleSheet("background-color: #ff4d4d; color: white; font-weight: bold;")
            
            #postion close event 
            close_btn.clicked.connect(lambda checked, s=symbol, d=side: self.close_position_request(s, d))
            
            self.table.setCellWidget(i, 5, close_btn)
        
        self.reset_sockets()


    def close_position_request(self, symbol, side):
        print(f"\n[청산 요청] {symbol} | 포지션: {side}")
        
        if side == "LONG":
            order_side = "SELL"
        else:
            order_side = "BUY"

        result = self.order_manager._close_position(symbol, order_side)
        if result:
            self.load_positions()

    def update_price(self, symbol, price):
        if symbol not in self.positions:
            return

        p = self.positions[symbol]
        row = self.row_map[symbol]

        entry = float(p['entryPrice'])
        amount = float(p['amount'])

        pnl_USDT = (price - entry) * amount
        pnl_KRW = pnl_USDT * self.usdt_krw

        self.table.setItem(row, 3, QTableWidgetItem(f"{pnl_USDT:.2f} USDT"))
        self.table.setItem(row, 4, QTableWidgetItem(f"{pnl_KRW:.0f} WON"))

    def reset_sockets(self):
        for s in self.sockets:
            s.stop()
        self.sockets = []
        for symbol in self.positions.keys():
            socket = PriceSocket(symbol.lower(), self.update_price)
            socket.start()
            self.sockets.append(socket)
    
    def update_rate(self, rate):
        self.usdt_krw = rate