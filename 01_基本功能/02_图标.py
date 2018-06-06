import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon

class MyWindow(QWidget):

    def __init__(self):
        super().__init__()
        # 绘制界面交给InitUI方法
        self.initUI()

    def initUI(self):
        # 设置窗口位置和大小
        self.setGeometry(100, 100, 500, 500)
        # 设置窗口标题
        self.setWindowTitle("MyWindow")
        # 设置图标
        self.setWindowIcon(QIcon("../img/icon.png"))

        # 显示窗口
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MyWindow()
    sys.exit(app.exec_())