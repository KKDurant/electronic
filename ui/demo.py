from PySide6.QtWidgets import QMainWindow, QApplication, QWidget, QMessageBox

from ui.Login import Ui_LoginUi
from ui.Regist import Ui_RegistUi

class RegistWindow(QWidget):
    def __init__(self, loginWindow):
        super(RegistWindow, self).__init__()
        self.parent = loginWindow
        self.regist_ui = Ui_RegistUi()
        self.regist_ui.setupUi(self)
        self.regist_ui.reset.clicked.connect(self.reset)
        self.regist_ui.regist.clicked.connect(self.registInfo)

    def reset(self):
        self.regist_ui.username.setText("")
        self.regist_ui.password.setText("")

    def registInfo(self):
        username = self.regist_ui.username.text()
        password = self.regist_ui.password.text()
        QMessageBox.information(self, '注册', '注册成功：' + username + '/' + password + '点击确定跳转登录')
        self.close()
        self.parent.show()

class LoginWindow(QWidget):
    def __init__(self):
        super(LoginWindow, self).__init__()
        self.login_ui = Ui_LoginUi()
        self.login_ui.setupUi(self)
        self.login_ui.regist.clicked.connect(self.regist_info)
        self.show()

    def login_to_init(self):
        pass

    def regist_info(self):
        self.regist_window = RegistWindow(self)
        self.hide()
        self.regist_window.show()

if __name__ == '__main__':
    app = QApplication()
    window = LoginWindow()
    app.exec()