import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication)


class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        okButton = QPushButton("OK")
        cancelButton = QPushButton("Cancel")

        # 水平布局
        hbox = QHBoxLayout()
        # 添加一个滑动因子 会把内容向右挤
        hbox.addStretch(1)
        # 添加两个按钮
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)

        # 垂直布局
        vbox = QVBoxLayout()
        # 添加一个滑动因子 把内容向下挤
        vbox.addStretch(1)
        # 添加水平布局
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Buttons')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())