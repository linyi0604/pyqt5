import sys
from PyQt5.QtWidgets import QApplication, QWidget

if __name__ == '__main__':
    # 灭一个pyqt5程序必须创建一个应用程序对象 sys.argv 是一个参数列表
    app = QApplication(sys.argv)
    # QWidget部件是pyqt5所有用户界面对象的基类
    w = QWidget()
    # 设置窗口大小
    w.resize(250, 150)
    # 移动窗口位置到屏幕的就位置
    w.move(50, 50)
    # 设置窗口的标题
    w.setWindowTitle("Simple")
    # 显示
    w.show()

    # 系统退出的时候 程序也退出
    # exec_() 方法是一个python关键词
    sys.exit(app.exec_())