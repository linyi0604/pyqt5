import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QPushButton, QFileDialog, QDialog, QComboBox
from PyQt5.QtCore import pyqtSignal
import sqlite3
import datetime
from threading import Thread
import time
from base64 import encodebytes, decodebytes
import os


# 数据库连接类
class Connector(object):
    def __init__(self):
        self.conn = sqlite3.connect("./db/connect.db")

    def execute(self, sql):
        try:
            c = self.conn.cursor()
            cursor = c.execute(sql)
            self.conn.commit()
            self.conn.close()
            return cursor
        except Exception as e:
            print(e)

    def delete(self, name):
        self.execute("delete from messages where user_from='%s'" % name)

    def insert_msg(self, user_from, user_to, msg):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        encryption = "123456"
        c = self.conn.cursor()
        sql0 = "select max(id) from messages "
        cursor = c.execute(sql0)
        res, = cursor.fetchone()
        if res is None:
            nid = 1
        else:
            nid = int(res) + 1
        sql = "insert into messages (id, user_from, user_to, detail, time, checked, encryption) values (%d, '%s', '%s', '%s', '%s', '%d', %s)" % (nid, user_from, user_to, msg, now, 0, encryption)
        conn = Connector()
        conn.execute(sql)

    def select_unread_message(self, name, signal):
        sql = "select user_from ,detail, id from messages where checked=0 and user_to='%s'" % name
        c = self.conn.cursor()
        cursor = c.execute(sql)
        for row in cursor:
            user_from = row[0]
            detail = row[1]
            nid = row[2]
            text = detail
            signal.emit(text)
            c = self.conn.cursor()
            c.execute("update messages set checked=1 where id=%s"%nid)
            self.conn.commit()


# 聊天窗口
class MyWindow(QWidget):
    # 信号槽
    _signal = pyqtSignal(str)

    def __init__(self, username, x=30):
        super(MyWindow, self).__init__()
        self.username = username
        self.x = x
        self.fileReciever = None
        self.reader = None
        self.fileSender = None
        self.msg_sender = None
        self.writer = None
        self.listener = None
        self.isClosed = False
        self.listener = Thread(target=self.listen, args=(self.username, self._signal), kwargs={})
        self.initUI()

    # 初始化发来消息面板
    def initReader(self):
        self.reader = QTextEdit(self)
        self.reader.move(5, 5)
        self.reader.resize(590, 340)
        self.reader.setReadOnly(True)

    # 初始化写消息面板
    def initWriter(self):
            self.writer = QTextEdit(self)
            self.writer.move(5, 350)
            self.writer.resize(490, 145)

    # 初始化 发送消息 发送文件 接收文件按钮组
    def initButtons(self):
        self.fileSender = QPushButton("发文件", self)
        self.fileSender.move(500, 350)
        self.fileSender.clicked.connect(self.sendFile)

        self.fileReciever = QPushButton("收文件", self)
        self.fileReciever.move(500, 400)
        self.fileReciever.clicked.connect(self.recieveFile)

        self.msg_sender = QPushButton("发送", self)
        self.msg_sender.move(500, 450)
        self.msg_sender.clicked.connect(self.sendMsg)

    # 画出界面
    def initUI(self):
        # 显示消息的文本框
        self.initReader()
        # 发送消息文本框
        self.initWriter()
        # 发送消息 接收文件 发送文件 按钮组
        self.initButtons()

        self.move(self.x, 30)
        self.resize(600, 500)
        self.setWindowTitle(self.username)
        self.show()
        # 开启线程获取消息状态 实时更新消息
        self._signal.connect(self.updateReader)
        self.listener.start()

    # 页面关闭的时候触发
    def closeEvent(self, QCloseEvent):
        self.isClosed = True
        conn = Connector()
        # conn.delete(self.username)

    # 监听别人发来信息
    def listen(self, name, signal):
        while True:
            time.sleep(1)
            if self.isClosed is True:
                break
            conn = Connector()
            conn.select_unread_message(name, signal)

    # 更新发来消息面板
    def updateReader(self, text):
        te = self.reader.toPlainText()
        text = decodebytes(text.encode()).decode()

        if self.username == "A":
            text = "B说：" + text
        else:
            text = "A说：" + text
        if te == "":
            te = text
        else:
            te += "\n\n" + text
        self.reader.setText(te)

    # 发送消息
    def sendMsg(self):
        msg = self.writer.toPlainText().strip()
        if msg:
            text = self.reader.toPlainText()
            if text == "":
                text += "我说:" + msg
            else:
                text += "\n\n我说:" + msg

            self.reader.setText(text)
            self.writer.setText("")

            if self.username == "A":
                to = "B"
            else:
                to = "A"
            conn = Connector()
            msg = encodebytes(msg.encode()).decode()
            conn.insert_msg(self.username, to, msg)

    # 发送文件
    def sendFile(self):
        fname = QFileDialog.getOpenFileName(self, '选择要发送的文件:', '/')
        path = fname[0]
        file_name = path.split("/")[-1]
        if path == "":
            return

        self.saveEncryptionFile(path, file_name)

    # 将文件加密后保存在系统里
    def saveEncryptionFile(self, path, file_name):
        fr = open(path, "rb")
        part = fr.read()
        # 对文件内容进行加密
        part = encodebytes(part)
        fw = open("./files/" + file_name, "wb")
        fw.write(part)
        fw.close()
        fr.close()

    # 接收发来文件
    def recieveFile(self):
        qc = ChooseFileDialog(self)


# 选择下载文件的Dialog
class ChooseFileDialog(QDialog):
    def __init__(self, s):
        super(ChooseFileDialog, self).__init__(s)
        self.combo = None
        self.parent = s
        self.initUI()
        self.setWindowTitle("选择要接收的文件")

    def initUI(self):
        combo = QComboBox(self)
        self.combo = combo
        file_list = os.listdir("./files")
        if not file_list:
            combo.addItem("尚未上传文件！")
        else:
            for f in file_list:
                combo.addItem(f)
        combo.move(0, 0)
        combo.resize(400, 30)

        btn = QPushButton("下载", self)
        btn.move(150, 50)
        btn.clicked.connect(self.chooseFile)

        self.setGeometry(300, 300, 400, 100)
        self.setWindowTitle('QComboBox')
        self.show()

    # 选择要下载的文件面板
    def chooseFile(self):
        file_name = self.combo.currentText()
        if file_name == "尚未上传文件！":
            self.close()
            return

        self.close()
        file_path = "./files/" + file_name
        path = QFileDialog.getExistingDirectory()
        if path == "":
            return
        else:
            path += "/"
        self.saveUnEncryptionFile(file_path, path + file_name)

    # 将文件解密后保存用户要下载的地方
    def saveUnEncryptionFile(self, in_path, out_path):
        print(in_path)
        print(out_path)
        fr = open(in_path, "rb")
        part = fr.read()
        # 对文件内容进行解密
        part = decodebytes(part)
        fw = open(out_path, "wb")
        fw.write(part)
        fw.close()
        fr.close()


# 初始化文件夹
def init_dirs():
    if not os.path.exists("./files/"):
        os.makedirs("./files/")
    if not os.path.exists("./db/"):
        os.makedirs("./db/")


# 初始化数据库
def init_db():
    sql0 = "drop table messages "
    conn = Connector()
    conn.execute(sql0)
    sql = '''
    create table messages(
      id int primary key DEFAULT 0,
      user_from text not null,
      user_to text not null,
      detail text not null,
      time text not NULL,
      checked int not NULL,
      encryption text
    );
    '''
    conn = Connector()
    conn.execute(sql)


# 初始化文件
def init_files():
    path = "./files/"
    file_list = os.listdir(path)
    for f in file_list:
        os.remove(path + f)


if __name__ == '__main__':
    try:
        init_dirs()     # 初始化文件夹
        init_db()   # 初始化数据库
        init_files() # 初始化文件目录
        # 开启二人聊天窗口
        app = QApplication(sys.argv)
        user1 = MyWindow("A")
        user2 = MyWindow("B", 900)
        sys.exit(app.exec_())
    except Exception as e:
        print(e)
