import sys
from PyQt5.QtWidgets import QWidget, QToolTip, QPushButton, QApplication
from PyQt5.QtGui import QFont

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 这种静态方法设置显示提示文字 使用10px 滑体字
        QToolTip.setFont(QFont("SansSerif", 10))
        # 创建一个提示语 可以使用丰富的文本格式
        self.setToolTip("这是一个 <b>QWidget</b> widget")
        # 创建一个PushButton 为他设置一个ToolTip
        btn = QPushButton("Button", self)
        btn.setToolTip("这是一个 <b>QPushButton</b> widget")
        # 设置按钮显示的默认尺寸
        btn.resize(btn.sizeHint())
        # 窗口位置
        btn.move(50, 50)

        self.setGeometry(100, 100, 300, 300)
        self.setWindowTitle("Tooltips")
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWindow()
    sys.exit(app.exec_())