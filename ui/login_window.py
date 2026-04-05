from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from trading.binance_client import check_client
from ui.main_window import MainWindow

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.api_key = QLineEdit()
        self.api_key.setPlaceholderText("API Key")

        self.secret = QLineEdit()
        self.secret.setPlaceholderText("Secret Key")
        self.secret.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.submit_keys)

        api_layout = QHBoxLayout()
        api_layout.addWidget(QLabel("API Key"))
        api_layout.addWidget(self.api_key)

        secret_layout = QHBoxLayout()
        secret_layout.addWidget(QLabel("Secret"))
        secret_layout.addWidget(self.secret)

        main_layout = QVBoxLayout()
        main_layout.addLayout(api_layout)
        main_layout.addLayout(secret_layout)
        main_layout.addWidget(self.login_button)

        self.setLayout(main_layout)

    def submit_keys(self):
        api = self.api_key.text()
        secret = self.secret.text()
        success, msg, client = check_client(api, secret)
        if success:
            QMessageBox.information(self, "성공", msg)

            self.main_window = MainWindow(client)
            self.main_window.show()

            self.close()

        else:
            QMessageBox.warning(self, "실패", msg)