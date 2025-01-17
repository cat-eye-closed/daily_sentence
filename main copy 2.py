from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication, QPushButton, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QPoint, QPointF
from PyQt5.QtGui import QPainter, QColor, QRadialGradient,QFont,QTextDocument

import random

import import_text_copy, import_love, import_date, search


#读取句子文本文件
textdic = import_text_copy.read_file_to_dict('sentence.md')
#句子总数
SENTENCE_NUM = len(textdic)
#随机生成句子序号的序列
sentence_sequence = list(range(1, SENTENCE_NUM+1))
random.shuffle(sentence_sequence)
#句子序号序列的下标
sen_serial_num = 0
#读取收藏序列
love_list = import_love.read_love_from_file('love.md')
#love_list用于主界面遍历，通过love_list_copy进行操作
love_list_copy = love_list.copy()
#love_list_copy用于收藏夹界面的遍历，通过love_list_copy_copy进行操作
love_list_copy_copy = love_list.copy()
love_serial_num = 0
#找到的句子序号序列
searched_list = []


class QSSLoader:
    def __init__(self):
        pass

    @staticmethod
    def read_qss_file(qss_file_name):
        with open(qss_file_name, 'r',  encoding='UTF-8') as file:
            return file.read()

class HoverLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMouseTracking(True)  # 启用鼠标跟踪
        self.x = 0.0
        self.y = 0.0

        # Set the styles
        self.setStyleSheet("""
            color: #1b2d45;
            font-family: '微软雅黑';
            font-size: 35px;
            font-weight: bold;
            qproperty-alignment: AlignCenter;
            border: 10px solid #CCCCCC;
            border-radius: 25px;
            padding: 5px;
            margin: 10px;
            outline: paleturquoise;
        """)
        self.setAlignment(Qt.AlignCenter)

    def enterEvent(self, event):
        super().enterEvent(event)

    def leaveEvent(self, event):
        super().leaveEvent(event)

    def mouseMoveEvent(self, event):
        self.x = float(event.x())
        self.y = float(event.y())
        self.update()  # 通知QWidget需要重绘
        super().mouseMoveEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        center = QPointF(self.x, self.y)
        gradient = QRadialGradient(center, 300)
        gradient.setColorAt(0, QColor(70, 130, 180, 255))  # 光晕的颜色
        gradient.setColorAt(1, QColor(235, 243, 248, 255))  # 背景颜色
        painter.fillRect(self.rect(), gradient)

        font = QFont()
        font.setFamily('微软雅黑')
        font.setBold(True)
        font.setPixelSize(35)
        painter.setFont(font)
        painter.setPen(QColor(27, 45, 69))  # Set text color
        painter.drawText(self.rect(), Qt.AlignCenter, self.text())  # Draw text

        painter = QPainter(self)

        # 创建 QTextDocument 作为临时的富文本渲染器
        doc = QTextDocument()

        # 使用 CSS 设置文本样式
        css = """
        p {
            color: #1b2d45;
            font-family: '微软雅黑';
            font-size: 35px;
            font-weight: bold;
            text-align: center;
            border: 10px solid #CCCCCC;
            border-radius: 25px;
            padding: 5px;
            margin: 10px;
            outline: paleturquoise;
        }
        """
        doc.setDefaultStyleSheet(css)
        doc.setHtml("<p>Hello<br/>World</p>")

        # 使用 QPainter 绘制 QTextDocument
        doc.drawContents(painter)

#主界面UI
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


        #左上角日期设置
        self.date = QtWidgets.QLabel(self.centralwidget)
        self.date.setGeometry(QtCore.QRect(int(self.width*0.08), int(self.height*0.08), int(self.width*0.18), int(self.width*0.18)))
        self.date.setText('<p>{}</p></br><p>{}</p>'.format(import_date.month, import_date.day))
        self.date.setObjectName("date")
        self.date.setAlignment(QtCore.Qt.AlignCenter)


        #左侧中间change按钮
        self.change = QtWidgets.QPushButton(self.centralwidget)
        self.change.setGeometry(QtCore.QRect(int(self.width*0.1), int(self.height*0.4), int(self.width*0.14), int(self.height*0.13)))
        self.change.setObjectName("change")
        self.change.clicked.connect(self.search)
        addShadowEffect2(self.change)


        self.hover_label = HoverLabel(self.centralwidget)
        self.hover_label.setObjectName("hover_label")
        self.hover_label.setStyleSheet("border-radius: 25px;padding: 5px;margin: 10px;outline: paleturquoise;")
        self.hover_label.setGeometry(QtCore.QRect(int(self.width*0.33), int(self.height*0.08), int(self.width*0.6), int(self.height*0.6)))

        #文本框设置
        self.label = HoverLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(int(self.width*0.33), int(self.height*0.08), int(self.width*0.6), int(self.height*0.6)))
        self.label.setObjectName("label")
        self.label.setStyleSheet("background-color: transparent")
        addShadowEffect1(self.label)
        self.label.setMouseTracking(True)


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
            self.retranslateUi(MainWindow)
        else:
            self.star.setIcon(star2)
            self.retranslateFavorite(MainWindow)
        self.star.setIconSize(QtCore.QSize(int(self.width*0.18), int(self.width*0.18)))
        self.star.setObjectName("star")
        self.star.setStyleSheet('border: 2px solid #CCCCCC;border-radius: 180px;padding: 5px;margin: 10px;') 
        self.star.setCheckable(True)
        self.star.setAutoExclusive(True)
        self.star.clicked.connect(self.clickStar)
        addShadowEffect2(self.star)


        #右侧下方中间收藏按钮
        self.love_button = QtWidgets.QPushButton(self.centralwidget)
        self.love_button.setGeometry(QtCore.QRect(int(self.width*0.585), int(self.height*0.73), int(self.width*0.09), int(self.width*0.09)))
        self.love_button.setText("")
        loved_button = QtGui.QIcon()
        loved_button.addPixmap(QtGui.QPixmap("pictures/loved.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        unloved_button = QtGui.QIcon()
        unloved_button.addPixmap(QtGui.QPixmap("pictures/unloved.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        
        if sentence_sequence[sen_serial_num] in love_list_copy:
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

        #右侧下方左边last按钮
        self.last_button = QtWidgets.QPushButton(self.centralwidget)
        self.last_button.setGeometry(QtCore.QRect(int(self.width*0.37), int(self.height*0.73), int(self.width*0.09), int(self.width*0.09)))
        last = QtGui.QIcon()
        last.addPixmap(QtGui.QPixmap("pictures/last.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.last_button.setIcon(last)
        self.last_button.setIconSize(QtCore.QSize(int(self.width*0.085), int(self.width*0.085)))
        self.last_button.setObjectName("last_button")
        self.last_button.setStyleSheet('border: 2px solid #CCCCCC;border-radius: 80px;padding: 5px;margin: 10px;')
        self.last_button.clicked.connect(self.last_sequence)
        addShadowEffect3(self.last_button)

        #右侧下方右边next按钮
        self.next_button = QtWidgets.QPushButton(self.centralwidget)
        self.next_button.setGeometry(QtCore.QRect(int(self.width*0.8), int(self.height*0.73), int(self.width*0.09), int(self.width*0.09)))
        next = QtGui.QIcon()
        next.addPixmap(QtGui.QPixmap("pictures/next.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.next_button.setIcon(next)
        self.next_button.setIconSize(QtCore.QSize(int(self.width*0.085), int(self.width*0.085)))
        self.next_button.setObjectName("next_button")
        self.next_button.setStyleSheet('border: 2px solid #CCCCCC;border-radius: 80px;padding: 5px;margin: 10px;')
        self.next_button.clicked.connect(self.next_sequence)
        addShadowEffect3(self.next_button)


        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    #星星收藏夹按钮对应切换主页面和收藏夹页面
    def clickStar(self):
        def addShadowEffect3(widget):
            shadowEffect = QGraphicsDropShadowEffect()
            shadowEffect.setBlurRadius(50)  # 设置模糊半径
            shadowEffect.setColor(QtGui.QColor(0, 0, 0, 80))  # 设置阴影颜色
            shadowEffect.setOffset(10, 10)  # 设置阴影偏移量
            widget.setGraphicsEffect(shadowEffect)

        global sen_serial_num, love_list, love_serial_num, love_list_copy, love_list_copy_copy, sentence_sequence
        self.star.isChecked = not self.star.isChecked
        star1 = QtGui.QIcon()
        star1.addPixmap(QtGui.QPixmap("pictures/star.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        star2 = QtGui.QIcon()
        star2.addPixmap(QtGui.QPixmap("pictures/star2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        if self.star.isChecked:
            self.star.setIcon(star1)
            self.star.setIconSize(QtCore.QSize(int(self.width*0.18), int(self.width*0.18)))
            self.retranslateUi(MainWindow)
            love_list_copy = love_list_copy_copy.copy()
            love_list = love_list_copy_copy.copy()
            if sentence_sequence[sen_serial_num] in love_list_copy:
                self.love_button.setIcon(QtGui.QIcon("pictures/loved.png"))
                self.love_button.setIconSize(QtCore.QSize(int(self.width*0.085), int(self.width*0.085)))
                self.love_button.isChecked = True
            else:
                self.love_button.setIcon(QtGui.QIcon("pictures/unloved.png"))
                self.love_button.setIconSize(QtCore.QSize(int(self.width*0.085), int(self.width*0.085)))
                self.love_button.isChecked = False
        else:
            self.star.setIcon(star2)
            self.star.setIconSize(QtCore.QSize(int(self.width*0.18), int(self.width*0.18)))
            self.retranslateFavorite(MainWindow)
            love_list_copy_copy = love_list_copy.copy()
            love_list = love_list_copy.copy()
            love_serial_num = 0
            self.love_button.setIcon(QtGui.QIcon("pictures/loved.png"))
            self.love_button.setIconSize(QtCore.QSize(int(self.width*0.085), int(self.width*0.085)))
            self.love_button.isChecked = True          
        loved_botton = QtGui.QIcon()
        loved_botton.addPixmap(QtGui.QPixmap("pictures/loved.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        unloved_button = QtGui.QIcon()
        unloved_button.addPixmap(QtGui.QPixmap("pictures/unloved.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        addShadowEffect3(self.love_button)


    #收藏按钮的变化并修改收藏序列
    def clickLove(self):
        global sen_serial_num, love_list, love_serial_num, love_list_copy, love_list_copy_copy, sentence_sequence
        self.love_button.isChecked = not self.love_button.isChecked
        loved_botton = QtGui.QIcon()
        loved_botton.addPixmap(QtGui.QPixmap("pictures/loved.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        unloved_button = QtGui.QIcon()
        unloved_button.addPixmap(QtGui.QPixmap("pictures/unloved.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        if self.star.isChecked:
            if self.love_button.isChecked:
                self.love_button.setIcon(loved_botton)
                self.love_button.setIconSize(QtCore.QSize(int(self.width*0.085), int(self.width*0.085)))
                love_list_copy.append(sentence_sequence[sen_serial_num])
            else:
                self.love_button.setIcon(unloved_button)
                self.love_button.setIconSize(QtCore.QSize(int(self.width*0.085), int(self.width*0.085)))
                love_list_copy.remove(sentence_sequence[sen_serial_num])
        else:
            if self.love_button.isChecked:
                self.love_button.setIcon(loved_botton)
                self.love_button.setIconSize(QtCore.QSize(int(self.width*0.085), int(self.width*0.085)))
                love_list_copy_copy.append(love_list_copy[love_serial_num])
            else:
                self.love_button.setIcon(unloved_button)
                self.love_button.setIconSize(QtCore.QSize(int(self.width*0.085), int(self.width*0.085)))
                love_list_copy_copy.remove(love_list_copy[love_serial_num])
    
    #last按钮按下后显示上一句
    def last_sequence(self):
        global sen_serial_num, love_list, love_serial_num, love_list_copy
        if self.star.isChecked:
            sen_serial_num -= 1
            if sen_serial_num < 0:
                sen_serial_num = len(sentence_sequence) - 1
            self.label.setText('{}'.format(textdic[sentence_sequence[sen_serial_num]]))
            if sentence_sequence[sen_serial_num] in love_list_copy:
                self.love_button.setIcon(QtGui.QIcon("pictures/loved.png"))
                self.love_button.setIconSize(QtCore.QSize(int(self.width*0.085), int(self.width*0.085)))
                self.love_button.isChecked = True
            else:
                self.love_button.setIcon(QtGui.QIcon("pictures/unloved.png"))
                self.love_button.setIconSize(QtCore.QSize(int(self.width*0.085), int(self.width*0.085)))
                self.love_button.isChecked = False
        else:
            love_serial_num -= 1
            if love_serial_num < 0:
                love_serial_num = len(love_list) - 1
            self.label.setText('{}'.format(textdic[love_list_copy[love_serial_num]]))
            if love_list[love_serial_num] in love_list_copy_copy:
                self.love_button.setIcon(QtGui.QIcon("pictures/loved.png"))
                self.love_button.setIconSize(QtCore.QSize(int(self.width*0.085), int(self.width*0.085)))
                self.love_button.isChecked = True
            else:
                self.love_button.setIcon(QtGui.QIcon("pictures/unloved.png"))
                self.love_button.setIconSize(QtCore.QSize(int(self.width*0.085), int(self.width*0.085)))
                self.love_button.isChecked = False

    #next按钮按下后显示下一句
    def next_sequence(self):
        global sen_serial_num, love_list, love_serial_num, love_list_copy
        if self.star.isChecked:
            sen_serial_num += 1
            if sen_serial_num >= len(sentence_sequence):
                sen_serial_num = 0
            self.label.setText('{}'.format(textdic[sentence_sequence[sen_serial_num]]))
            if sentence_sequence[sen_serial_num] in love_list_copy:
                self.love_button.setIcon(QtGui.QIcon("pictures/loved.png"))
                self.love_button.setIconSize(QtCore.QSize(int(self.width*0.085), int(self.width*0.085)))
                self.love_button.isChecked = True
            else:
                self.love_button.setIcon(QtGui.QIcon("pictures/unloved.png"))
                self.love_button.setIconSize(QtCore.QSize(int(self.width*0.085), int(self.width*0.085)))
                self.love_button.isChecked = False
        else:
            love_serial_num += 1
            if love_serial_num >= len(love_list):
                love_serial_num = 0
            self.label.setText('{}'.format(textdic[love_list_copy[love_serial_num]]))
            if love_list[love_serial_num] in love_list_copy_copy:
                self.love_button.setIcon(QtGui.QIcon("pictures/loved.png"))
                self.love_button.setIconSize(QtCore.QSize(int(self.width*0.085), int(self.width*0.085)))
                self.love_button.isChecked = True
            else:
                self.love_button.setIcon(QtGui.QIcon("pictures/unloved.png"))
                self.love_button.setIconSize(QtCore.QSize(int(self.width*0.085), int(self.width*0.085)))
                self.love_button.isChecked = False

    #搜索函数
    def search(self):
        global searched_list, sen_serial_num
        search.search(textdic, '爱', searched_list)
        if searched_list:
            sen_serial_num = searched_list[0] - 1
            self.label.setText('{}'.format(textdic[searched_list[0]]))
        else:
            self.label.setText('未找到')
    

    #主界面的设置
    def retranslateUi(self, MainWindow):
        global textdic, sen_serial_num,sentence_sequence
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Daily Sentence"))
        MainWindow.setWindowIcon(QtGui.QIcon('pictures/star.png'))
        self.change.setText(_translate("MainWindow", "主界面"))
        self.label.setText(_translate("MainWindow", '{}'.format(textdic[sentence_sequence[sen_serial_num]])))

    def retranslateFavorite(self, MainWindow):
        global textdic, sen_serial_num, love_list, love_serial_num
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Daily Sentence"))
        MainWindow.setWindowIcon(QtGui.QIcon('pictures/star2.png'))
        self.change.setText(_translate("MainWindow", "收藏夹"))
        self.label.setText(_translate("MainWindow", '{}'.format(textdic[love_list_copy[love_serial_num]])))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    style_file = './style.qss'
    style_sheet = QSSLoader.read_qss_file(style_file)
    MainWindow.setStyleSheet(style_sheet)
    MainWindow.show()
    app.exec_()
    love_list = set(love_list_copy).intersection(set(love_list_copy_copy))
    import_love.write_love_to_file(love_list, 'love.md')
    print('love_list:', love_list)
    sys.exit()