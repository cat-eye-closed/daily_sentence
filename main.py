from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication, QPushButton, QGraphicsDropShadowEffect
from PyQt5.QtGui import QFont

import random

import import_text, import_love


#读取句子文本文件
textdic = import_text.read_file_to_dict('sentence.md')
SENTENCE_NUM = len(textdic)
sen_serial_num = random.randint(1, SENTENCE_NUM)
#读取收藏序列
love_list = import_love.read_love_from_file('love.md')


class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "自适应屏幕大小UI"

        #获取显示器分辨率
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.screenheight = self.screenRect.height()
        self.screenwidth = self.screenRect.width()

        print("Screen height {}".format(self.screenheight))
        print("Screen width {}".format(self.screenwidth))

        self.height = int(self.screenheight * 0.7)
        self.width = int(self.screenwidth * 0.7)

        self.resize(self.width,self.height)
        self.wid = QWidget(self)
        self.setCentralWidget(self.wid)
        self.setWindowTitle(self.title)
        self.setupUi(MainWindow)


    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(self.width, self.height)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet('background-color: #FFFFFF;')

        #阴影效果
        def addShadowEffect1(widget):
            shadowEffect = QGraphicsDropShadowEffect()
            shadowEffect.setBlurRadius(80)  # 设置模糊半径
            shadowEffect.setColor(QtGui.QColor(0, 0, 0, 80))  # 设置阴影颜色
            shadowEffect.setOffset(20, 20)  # 设置阴影偏移量
            widget.setGraphicsEffect(shadowEffect)
        def addShadowEffect2(widget):
            shadowEffect = QGraphicsDropShadowEffect()
            shadowEffect.setBlurRadius(80)  # 设置模糊半径
            shadowEffect.setColor(QtGui.QColor(0, 0, 0, 80))  # 设置阴影颜色
            shadowEffect.setOffset(15, 15)  # 设置阴影偏移量
            widget.setGraphicsEffect(shadowEffect)
        def addShadowEffect3(widget):
            shadowEffect = QGraphicsDropShadowEffect()
            shadowEffect.setBlurRadius(50)  # 设置模糊半径
            shadowEffect.setColor(QtGui.QColor(0, 0, 0, 80))  # 设置阴影颜色
            shadowEffect.setOffset(10, 10)  # 设置阴影偏移量
            widget.setGraphicsEffect(shadowEffect)


        #字体设置
        font1 = QFont()
        font1.setFamily('微软雅黑')
        font1.setBold(True)
        font1.setPixelSize(int(self.width*0.018))


        #左上角日期设置
        self.date = QtWidgets.QLabel(self.centralwidget)
        self.date.setGeometry(QtCore.QRect(int(self.width*0.08), int(self.height*0.08), int(self.width*0.18), int(self.width*0.18)))
        self.date.setText("Date")
        self.date.setObjectName("date")
        self.date.setAlignment(QtCore.Qt.AlignCenter)
        self.date.setStyleSheet('border: 3px solid #000000;')


        #左侧中间change按钮
        self.change_but = QtWidgets.QPushButton(self.centralwidget)
        self.change_but.setGeometry(QtCore.QRect(int(self.width*0.1), int(self.height*0.43), int(self.width*0.14), int(self.height*0.13)))
        self.change_but.setFont(font1)
        self.change_but.setObjectName("change_but")
        self.change_but.clicked.connect(self.change_sequence)
        addShadowEffect2(self.change_but)


        #文本框设置
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(int(self.width/3), int(self.height/12), int(self.width/1.7), int(self.height/1.7)))
        self.label.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))

        self.label.setFont(font1)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label.setStyleSheet('background-color:rgb(235, 243, 248); border: 10px solid #CCCCCC;border-radius: 15px;padding: 5px;margin: 10px;')
        addShadowEffect1(self.label)


        #左下角收藏夹按钮
        self.star = QtWidgets.QPushButton(self.centralwidget)
        self.star.setGeometry(QtCore.QRect(int(self.width*0.075), int(self.height*0.6), int(self.width*0.19), int(self.width*0.19)))
        self.star.setText("")
        star1 = QtGui.QIcon()
        star1.addPixmap(QtGui.QPixmap("pictures/star.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        star2 = QtGui.QIcon()
        star2.addPixmap(QtGui.QPixmap("pictures/star2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.star.setChecked(False)
        if self.star.isChecked:
            self.star.setIcon(star1)
        else:
            self.star.setIcon(star2)
        self.star.setIconSize(QtCore.QSize(int(self.width*0.18), int(self.width*0.18)))
        self.star.setObjectName("star")
        self.star.setStyleSheet('border: 2px solid #CCCCCC;border-radius: 180px;padding: 5px;margin: 10px;') 
        self.star.setCheckable(True)
        self.star.setAutoExclusive(True)
        self.star.clicked.connect(self.clickStar)
        addShadowEffect2(self.star)


        #右侧下方收藏按钮
        self.love_button = QtWidgets.QPushButton(self.centralwidget)
        self.love_button.setGeometry(QtCore.QRect(int(self.width*0.4), int(self.height*0.7), int(self.width*0.09), int(self.width*0.09)))
        self.love_button.setText("")
        loved_button = QtGui.QIcon()
        loved_button.addPixmap(QtGui.QPixmap("d:\\cat_eye\\daily_sentence\\pictures/loved.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        unloved_button = QtGui.QIcon()
        unloved_button.addPixmap(QtGui.QPixmap("d:\\cat_eye\\daily_sentence\\pictures/unloved.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        
        if sen_serial_num in love_list:
            self.love_button.setIcon(loved_button)
            self.love_button.isChecked = True
        else:
            self.love_button.setIcon(unloved_button)
            self.love_button.isChecked = False
        addShadowEffect3(self.love_button)
        self.love_button.setIconSize(QtCore.QSize(int(self.width*0.085), int(self.width*0.085)))
        self.love_button.setObjectName("love_button")
        self.love_button.setStyleSheet('border: 2px solid #CCCCCC;border-radius: 80px;padding: 5px;margin: 10px;') 
        self.love_button.setCheckable(True)
        self.love_button.setAutoExclusive(True)
        self.love_button.clicked.connect(self.clickLove)


        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    #星星按钮的变化
    def clickStar(self):
        self.star.isChecked = not self.star.isChecked
        star1 = QtGui.QIcon()
        star1.addPixmap(QtGui.QPixmap("pictures/star.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        star2 = QtGui.QIcon()
        star2.addPixmap(QtGui.QPixmap("pictures/star2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        if self.star.isChecked:
            self.star.setIcon(star1)
            self.star.setIconSize(QtCore.QSize(int(self.width*0.18), int(self.width*0.18)))
        else:
            self.star.setIcon(star2)
            self.star.setIconSize(QtCore.QSize(int(self.width*0.18), int(self.width*0.18)))


    #收藏按钮的变化并修改收藏序列
    def clickLove(self):
        global sen_serial_num
        self.love_button.isChecked = not self.love_button.isChecked
        loved_botton = QtGui.QIcon()
        loved_botton.addPixmap(QtGui.QPixmap("pictures/loved.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        unloved_button = QtGui.QIcon()
        unloved_button.addPixmap(QtGui.QPixmap("pictures/unloved.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        if self.love_button.isChecked:
            self.love_button.setIcon(loved_botton)
            self.love_button.setIconSize(QtCore.QSize(int(self.width*0.085), int(self.width*0.085)))
            love_list.append(sen_serial_num)
        else:
            self.love_button.setIcon(unloved_button)
            self.love_button.setIconSize(QtCore.QSize(int(self.width*0.085), int(self.width*0.085)))
            love_list.remove(sen_serial_num)


    #change按钮按下后随机
    def change_sequence(self):
        global sen_serial_num
        sen_serial_num = random.randint(1, SENTENCE_NUM)
        self.label.setText('<p style="line-height:60px;">{}</p>'.format(textdic[sen_serial_num]))
        if sen_serial_num in love_list:
            self.love_button.setIcon(QtGui.QIcon("pictures/loved.png"))
            self.love_button.setIconSize(QtCore.QSize(int(self.width*0.085), int(self.width*0.085)))
            self.love_button.isChecked = True
        else:
            self.love_button.setIcon(QtGui.QIcon("pictures/unloved.png"))
            self.love_button.setIconSize(QtCore.QSize(int(self.width*0.085), int(self.width*0.085)))
            self.love_button.isChecked = False
    

    #主界面的设置
    def retranslateUi(self, MainWindow):
        global textdic, sen_serial_num
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Daily Sentence"))
        MainWindow.setWindowIcon(QtGui.QIcon('pictures/star2.png'))
        self.change_but.setText(_translate("MainWindow", "切换句子"))
        self.label.setText(_translate("MainWindow", '<p style="line-height:60px;">{}</p>'.format(textdic[sen_serial_num])))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.exec_()
    love_list.sort()
    import_love.write_love_to_file(love_list, 'love.md')
    print('love_list:', love_list)
    sys.exit()