from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QSlider
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QPushButton, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QPoint, QPointF, QPropertyAnimation, pyqtProperty, QUrl
from PyQt5.QtGui import QPainter, QColor, QRadialGradient,QFont
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist

import random, time, math, os

import import_text, import_love, import_date, search


#读取句子文本文件
textdic = import_text.read_file_to_dict('sentence.md')
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
search_serial_num = 0
#悬停光晕半径
hover_radius = random.randint(250, 500)
#判定是否搜索
is_searched = False


class QSSLoader:
    def __init__(self):
        pass

    @staticmethod
    def read_qss_file(qss_file_name):
        with open(qss_file_name, 'r',  encoding='UTF-8') as file:
            return file.read()
        
def get_color():
    t = time.time()  # Get current time

    # Compute color components
    hue = int(t * 10) % 360
    saturation = 100 + int(math.sin(t) * 50)  # Range between 200 and 250
    value = 200 + int(math.sin(t) * 50)  # Range between 200 and 250

    return QColor.fromHsv(hue, saturation, value)

#设置检测鼠标悬停的label子类
class HoverLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super(HoverLabel, self).__init__(*args, **kwargs)
        self.setMouseTracking(True) # Enable mouse tracking
        self.mousePosition = QPointF(0, 0)
        self.animation = QPropertyAnimation(self, b'mousePosition', self)
        self.animation.setDuration(1000)  # Animation duration in milliseconds        

    def enterEvent(self, event):
        global hover_radius
        super().enterEvent(event)
        hover_radius = random.randint(200, 500)

    def leaveEvent(self, event):
        super().leaveEvent(event)

    @pyqtProperty(QPointF)
    def mousePosition(self):
        return self._mousePosition

    @mousePosition.setter
    def mousePosition(self, value):
        self._mousePosition = value
        self.update()
    
    def mouseMoveEvent(self, event):
        endValue = QPointF(event.pos().x(), event.pos().y())
        self.animation.setStartValue(self.mousePosition)
        self.animation.setEndValue(endValue)
        self.animation.start()

    def paintEvent(self,event):
        painter = QPainter(self)
        gradient = QRadialGradient(self.mousePosition, hover_radius)
        gradient.setColorAt(0, get_color())  # 光晕的颜色
        gradient.setColorAt(1, QColor(235, 243, 248, 0))  # 背景颜色
        painter.fillRect(self.rect(), gradient)


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
        self.date.setGeometry(QtCore.QRect(int(self.width*0.08), int(self.height*0.02), int(self.width*0.18), int(self.width*0.18)))
        self.date.setText('<p>{}</p></br><p>{}</p>'.format(import_date.month, import_date.day))
        self.date.setObjectName("date")
        self.date.setAlignment(QtCore.Qt.AlignCenter)


        #左侧中间搜索框
        global search_str
        self.search_box = QtWidgets.QLineEdit(self.centralwidget)
        self.search_box.setGeometry(QtCore.QRect(int(self.width*0.37), int(self.height*0.018), int(self.width*0.45), int(self.height*0.1)))
        self.search_box.setObjectName("search")
        self.search_box.returnPressed.connect(self.search)
        search_str = self.search_box.text()
        addShadowEffect2(self.search_box)

        #左侧中间搜索确认按钮
        self.search_confirm_button = QtWidgets.QPushButton(self.centralwidget)
        self.search_confirm_button.setGeometry(QtCore.QRect(int(self.width*0.83), int(self.height*0.018), int(self.height*0.1), int(self.height*0.1)))
        self.search_confirm_button.setObjectName("confirm")
        self.search_confirm_button.clicked.connect(self.search_confirm)
        addShadowEffect2(self.search_confirm_button)

        #文本框设置
        self.label = QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(int(self.width*0.33), int(self.height*0.13), int(self.width*0.6), int(self.height*0.61)))
        self.label.setObjectName("label")
        self.label.setStyleSheet("background-color: transparent")
        addShadowEffect1(self.label)
        self.label.setMouseTracking(True)

        #文本框的悬停效果
        self.hover_label = HoverLabel(self.centralwidget)
        self.hover_label.setObjectName("hover_label")
        self.hover_label.setGeometry(QtCore.QRect(int(self.width*0.335), int(self.height*0.1385), int(self.width*0.59), int(self.height*0.59)))


        #左下角收藏夹按钮
        self.star = QtWidgets.QPushButton(self.centralwidget)
        self.star.setGeometry(QtCore.QRect(int(self.width*0.075), int(self.height*0.63), int(self.width*0.19), int(self.width*0.19)))
        self.star.setText("")
        star1 = QtGui.QIcon()
        star1.addPixmap(QtGui.QPixmap("resources/pictures/star.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        star2 = QtGui.QIcon()
        star2.addPixmap(QtGui.QPixmap("resources/pictures/star2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

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
        self.love_button.setGeometry(QtCore.QRect(int(self.width*0.585), int(self.height*0.78), int(self.width*0.09), int(self.width*0.09)))
        self.love_button.setText("")
        loved_button = QtGui.QIcon()
        loved_button.addPixmap(QtGui.QPixmap("resources/pictures/loved.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        unloved_button = QtGui.QIcon()
        unloved_button.addPixmap(QtGui.QPixmap("resources/pictures/unloved.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        
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
        if is_searched and searched_list == []:
            self.love_button.setIcon(unloved_button)
            self.love_button.isChecked = False            
        else:
            self.love_button.clicked.connect(self.clickLove)

        #右侧下方左边last按钮
        self.last_button = QtWidgets.QPushButton(self.centralwidget)
        self.last_button.setGeometry(QtCore.QRect(int(self.width*0.37), int(self.height*0.78), int(self.width*0.09), int(self.width*0.09)))
        last = QtGui.QIcon()
        last.addPixmap(QtGui.QPixmap("resources/pictures/last.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.last_button.setIcon(last)
        self.last_button.setIconSize(QtCore.QSize(int(self.width*0.085), int(self.width*0.085)))
        self.last_button.setObjectName("last_button")
        self.last_button.setStyleSheet('border: 2px solid #CCCCCC;border-radius: 80px;padding: 5px;margin: 10px;')
        self.last_button.clicked.connect(self.last_sequence)
        addShadowEffect3(self.last_button)

        #右侧下方右边next按钮
        self.next_button = QtWidgets.QPushButton(self.centralwidget)
        self.next_button.setGeometry(QtCore.QRect(int(self.width*0.8), int(self.height*0.78), int(self.width*0.09), int(self.width*0.09)))
        next = QtGui.QIcon()
        next.addPixmap(QtGui.QPixmap("resources/pictures/next.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.next_button.setIcon(next)
        self.next_button.setIconSize(QtCore.QSize(int(self.width*0.085), int(self.width*0.085)))
        self.next_button.setObjectName("next_button")
        self.next_button.setStyleSheet('border: 2px solid #CCCCCC;border-radius: 80px;padding: 5px;margin: 10px;')
        self.next_button.clicked.connect(self.next_sequence)
        addShadowEffect3(self.next_button)

        #音乐播放   

        class MusicPlayer(QWidget):
            def __init__(self, songs):
                super().__init__()
                self.songs = songs  # 保存音乐路径列表
                self.playlist = QMediaPlaylist()
                self.player = QMediaPlayer()
                self.player.setVolume(50)
                self.playlist.setPlaybackMode(QMediaPlaylist.Random)

                random.shuffle(self.songs)
                for song in self.songs:
                    self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(song)))

                random_index = random.randint(0, len(self.songs) - 1)
                self.playlist.setCurrentIndex(random_index)

                self.player.setPlaylist(self.playlist)


            def get_current_music_name(self):
                # 获取当前播放的音乐的路径
                current_music_path = self.songs[self.playlist.currentIndex()]
                # 获取音乐文件的名称，去掉扩展名
                music_name, _ = os.path.splitext(os.path.basename(current_music_path))
                return music_name

        music_dir = 'resources/music'
        songs = [os.path.join(music_dir, f) for f in os.listdir(music_dir) if f.endswith('.mp3')]
        self.mediaPlayer = MusicPlayer(songs)
        self.mediaPlayer.player.stateChanged.connect(self.next_music_normal)

        #音乐播放按钮
        self.music_button = QtWidgets.QPushButton(self.centralwidget)
        self.music_button.setGeometry(QtCore.QRect(int(self.width*0.145), int(self.height*0.45), int(self.width*0.05), int(self.width*0.05)))
        self.music_button.setObjectName("music_button")
        music = QtGui.QIcon()
        music.addPixmap(QtGui.QPixmap("resources/pictures/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.music_button.setIcon(music)
        self.music_button.setIconSize(QtCore.QSize(int(self.width*0.045), int(self.width*0.045)))
        self.music_button.setStyleSheet('border: 2px solid #CCCCCC;border-radius: 40px;padding: 5px;margin: 10px;')
        self.music_button.isChecked = False
        self.music_button.setCheckable(True)
        self.music_button.clicked.connect(self.music_button_click)
        addShadowEffect2(self.music_button)

        #音乐上一首
        self.last_music_button = QtWidgets.QPushButton(self.centralwidget)
        self.last_music_button.setGeometry(QtCore.QRect(int(self.width*0.07), int(self.height*0.45), int(self.width*0.05), int(self.width*0.05)))
        self.last_music_button.setObjectName("last_music_button")
        last_music = QtGui.QIcon()
        last_music.addPixmap(QtGui.QPixmap("resources/pictures/last.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.last_music_button.setIcon(last_music)
        self.last_music_button.setIconSize(QtCore.QSize(int(self.width*0.045), int(self.width*0.045)))
        self.last_music_button.setStyleSheet('border: 2px solid #CCCCCC;border-radius: 40px;padding: 5px;margin: 10px;')
        self.last_music_button.clicked.connect(self.last_music)
        addShadowEffect2(self.last_music_button)

        #音乐下一首
        self.next_music_button = QtWidgets.QPushButton(self.centralwidget)
        self.next_music_button.setGeometry(QtCore.QRect(int(self.width*0.22), int(self.height*0.45), int(self.width*0.05), int(self.width*0.05)))
        self.next_music_button.setObjectName("next_music_button")
        next_music = QtGui.QIcon()
        next_music.addPixmap(QtGui.QPixmap("resources/pictures/next.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.next_music_button.setIcon(next_music)
        self.next_music_button.setIconSize(QtCore.QSize(int(self.width*0.045), int(self.width*0.045)))
        self.next_music_button.setStyleSheet('border: 2px solid #CCCCCC;border-radius: 40px;padding: 5px;margin: 10px;')
        self.next_music_button.clicked.connect(self.next_music)
        addShadowEffect2(self.next_music_button)

        #显示当前音乐名称
        self.music_name = QtWidgets.QLabel(self.centralwidget)
        self.music_name.setGeometry(QtCore.QRect(int(self.width*0.02), int(self.height*0.35), int(self.width*0.3), int(self.height*0.08)))
        self.music_name.setObjectName("music_name")
        self.music_name.setAlignment(QtCore.Qt.AlignCenter)
        self.music_name.setText(self.mediaPlayer.get_current_music_name())
        self.music_name.setStyleSheet('background-color: transparent')
        addShadowEffect2(self.music_name)


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

        global sen_serial_num, love_list, love_serial_num, love_list_copy, love_list_copy_copy, sentence_sequence, is_searched, searched_list, search_serial_num
        self.star.isChecked = not self.star.isChecked
        is_searched = False
        star1 = QtGui.QIcon()
        star1.addPixmap(QtGui.QPixmap("resources/pictures/star.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        star2 = QtGui.QIcon()
        star2.addPixmap(QtGui.QPixmap("resources/pictures/star2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        if self.star.isChecked:
            self.star.setIcon(star1)
            self.star.setIconSize(QtCore.QSize(int(self.width*0.18), int(self.width*0.18)))
            self.retranslateUi(MainWindow)
            love_list_copy = love_list_copy_copy.copy()
            love_list = love_list_copy_copy.copy()
            if sentence_sequence[sen_serial_num] in love_list_copy:
                self.love_button.setIcon(QtGui.QIcon("resources/pictures/loved.png"))
                self.love_button.setIconSize(QtCore.QSize(int(self.width*0.085), int(self.width*0.085)))
                self.love_button.isChecked = True
            else:
                self.love_button.setIcon(QtGui.QIcon("resources/pictures/unloved.png"))
                self.love_button.setIconSize(QtCore.QSize(int(self.width*0.085), int(self.width*0.085)))
                self.love_button.isChecked = False
        else:
            self.star.setIcon(star2)
            self.star.setIconSize(QtCore.QSize(int(self.width*0.18), int(self.width*0.18)))
            if love_list_copy:
                self.retranslateFavorite(MainWindow)
            else:
                self.label.setText('<p style="line-height:60px;">还没有收藏的句子呢，</br>去逛逛吧</p>')
            love_list_copy_copy = love_list_copy.copy()
            love_list = love_list_copy.copy()
            love_serial_num = 0
            self.love_button.setIcon(QtGui.QIcon("resources/pictures/loved.png"))
            self.love_button.setIconSize(QtCore.QSize(int(self.width*0.085), int(self.width*0.085)))
            self.love_button.isChecked = True          
        loved_botton = QtGui.QIcon()
        loved_botton.addPixmap(QtGui.QPixmap("resources/pictures/loved.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        unloved_button = QtGui.QIcon()
        unloved_button.addPixmap(QtGui.QPixmap("resources/pictures/unloved.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        addShadowEffect3(self.love_button)

    #收藏按钮的变化并修改收藏序列
    def clickLove(self):
        global sen_serial_num, love_list, love_serial_num, love_list_copy, love_list_copy_copy, sentence_sequence
        self.love_button.isChecked = not self.love_button.isChecked
        loved_botton = QtGui.QIcon()
        loved_botton.addPixmap(QtGui.QPixmap("resources/pictures/loved.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        unloved_button = QtGui.QIcon()
        unloved_button.addPixmap(QtGui.QPixmap("resources/pictures/unloved.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        if is_searched:
            if searched_list:
                if self.love_button.isChecked:
                    if searched_list[search_serial_num] not in love_list_copy_copy:
                        self.love_button.setIcon(loved_botton)
                        self.love_button.setIconSize(QtCore.QSize(int(self.width*0.085), int(self.width*0.085)))
                        love_list_copy_copy.append(searched_list[search_serial_num])
                        love_list_copy.append(searched_list[search_serial_num])
                else:
                    if searched_list[search_serial_num] in love_list_copy_copy:
                        self.love_button.setIcon(unloved_button)
                        self.love_button.setIconSize(QtCore.QSize(int(self.width*0.085), int(self.width*0.085)))
                        love_list_copy_copy.remove(searched_list[search_serial_num])
                        love_list_copy.remove(searched_list[search_serial_num])

        elif self.star.isChecked:
            if self.love_button.isChecked:
                self.love_button.setIcon(loved_botton)
                self.love_button.setIconSize(QtCore.QSize(int(self.width*0.085), int(self.width*0.085)))
                love_list_copy.append(sentence_sequence[sen_serial_num])
            else:
                self.love_button.setIcon(unloved_button)
                self.love_button.setIconSize(QtCore.QSize(int(self.width*0.085), int(self.width*0.085)))
                love_list_copy.remove(sentence_sequence[sen_serial_num])
        else:
            if love_list_copy:
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
        global sen_serial_num, love_list, love_serial_num, love_list_copy, love_list_copy_copy, sentence_sequence, search_serial_num
        if is_searched:
            if searched_list:
                search_serial_num -= 1
                if search_serial_num < 0:
                    search_serial_num = len(searched_list) - 1
                self.label.setText('<p style="line-height:60px;">{}</p>'.format(textdic[searched_list[search_serial_num]]))
                if searched_list[search_serial_num] in love_list_copy_copy:
                    self.love_button.setIcon(QtGui.QIcon("resources/pictures/loved.png"))
                    self.love_button.setIconSize(QtCore.QSize(int(self.width*0.085), int(self.width*0.085)))
                    self.love_button.isChecked = True
                else:
                    self.love_button.setIcon(QtGui.QIcon("resources/pictures/unloved.png"))
                    self.love_button.setIconSize(QtCore.QSize(int(self.width*0.085), int(self.width*0.085)))
                    self.love_button.isChecked = False
        elif self.star.isChecked:
            sen_serial_num -= 1
            if sen_serial_num < 0:
                sen_serial_num = len(sentence_sequence) - 1
            self.label.setText('<p style="line-height:60px;">{}</p>'.format(textdic[sentence_sequence[sen_serial_num]]))
            if sentence_sequence[sen_serial_num] in love_list_copy:
                self.love_button.setIcon(QtGui.QIcon("resources/pictures/loved.png"))
                self.love_button.setIconSize(QtCore.QSize(int(self.width*0.085), int(self.width*0.085)))
                self.love_button.isChecked = True
            else:
                self.love_button.setIcon(QtGui.QIcon("resources/pictures/unloved.png"))
                self.love_button.setIconSize(QtCore.QSize(int(self.width*0.085), int(self.width*0.085)))
                self.love_button.isChecked = False
        else:
            if love_list_copy:
                love_serial_num -= 1
                if love_serial_num < 0:
                    love_serial_num = len(love_list) - 1
                self.label.setText('<p style="line-height:60px;">{}</p>'.format(textdic[love_list_copy[love_serial_num]]))
                if love_list[love_serial_num] in love_list_copy_copy:
                    self.love_button.setIcon(QtGui.QIcon("resources/pictures/loved.png"))
                    self.love_button.setIconSize(QtCore.QSize(int(self.width*0.085), int(self.width*0.085)))
                    self.love_button.isChecked = True
                else:
                    self.love_button.setIcon(QtGui.QIcon("resources/pictures/unloved.png"))
                    self.love_button.setIconSize(QtCore.QSize(int(self.width*0.085), int(self.width*0.085)))
                    self.love_button.isChecked = False

    #next按钮按下后显示下一句
    def next_sequence(self):
        global sen_serial_num, love_list, love_serial_num, love_list_copy, love_list_copy_copy, sentence_sequence, search_serial_num
        if is_searched:
            if searched_list:
                search_serial_num += 1
                if search_serial_num >= len(searched_list):
                    search_serial_num = 0
                self.label.setText('<p style="line-height:60px;">{}</p>'.format(textdic[searched_list[search_serial_num]]))
                if searched_list[search_serial_num] in love_list_copy_copy:
                    self.love_button.setIcon(QtGui.QIcon("resources/pictures/loved.png"))
                    self.love_button.setIconSize(QtCore.QSize(int(self.width*0.085), int(self.width*0.085)))
                    self.love_button.isChecked = True
                else:
                    self.love_button.setIcon(QtGui.QIcon("resources/pictures/unloved.png"))
                    self.love_button.setIconSize(QtCore.QSize(int(self.width*0.085), int(self.width*0.085)))
                    self.love_button.isChecked = False

        elif self.star.isChecked:
            sen_serial_num += 1
            if sen_serial_num >= len(sentence_sequence):
                sen_serial_num = 0
            self.label.setText('<p style="line-height:60px;">{}</p>'.format(textdic[sentence_sequence[sen_serial_num]]))
            if sentence_sequence[sen_serial_num] in love_list_copy:
                self.love_button.setIcon(QtGui.QIcon("resources/pictures/loved.png"))
                self.love_button.setIconSize(QtCore.QSize(int(self.width*0.085), int(self.width*0.085)))
                self.love_button.isChecked = True
            else:
                self.love_button.setIcon(QtGui.QIcon("resources/pictures/unloved.png"))
                self.love_button.setIconSize(QtCore.QSize(int(self.width*0.085), int(self.width*0.085)))
                self.love_button.isChecked = False
        else:
            if love_list_copy:
                love_serial_num += 1
                if love_serial_num >= len(love_list):
                    love_serial_num = 0
                self.label.setText('<p style="line-height:60px;">{}</p>'.format(textdic[love_list_copy[love_serial_num]]))
                if love_list[love_serial_num] in love_list_copy_copy:
                    self.love_button.setIcon(QtGui.QIcon("resources/pictures/loved.png"))
                    self.love_button.setIconSize(QtCore.QSize(int(self.width*0.085), int(self.width*0.085)))
                    self.love_button.isChecked = True
                else:
                    self.love_button.setIcon(QtGui.QIcon("resources/pictures/unloved.png"))
                    self.love_button.setIconSize(QtCore.QSize(int(self.width*0.085), int(self.width*0.085)))
                    self.love_button.isChecked = False

    #搜索框槽函数
    def search(self):
        global searched_list, sen_serial_num, search_str, is_searched, sentence_sequence,search_serial_num
        search_serial_num = 0
        is_searched = True
        search_str = self.search_box.text()
        print('search_str:', search_str)
        searched_list = search.search(textdic, search_str, searched_list)
        print('searched_list:', searched_list)
        if searched_list:
            self.label.setText('<p style="line-height:60px;">{}</p>'.format(textdic[searched_list[0]]))
            if searched_list[search_serial_num] in love_list_copy_copy:
                self.love_button.setIcon(QtGui.QIcon("resources/pictures/loved.png"))
                self.love_button.setIconSize(QtCore.QSize(int(self.width*0.085), int(self.width*0.085)))
                self.love_button.isChecked = True
            else:
                self.love_button.setIcon(QtGui.QIcon("resources/pictures/unloved.png"))
                self.love_button.setIconSize(QtCore.QSize(int(self.width*0.085), int(self.width*0.085)))
                self.love_button.isChecked = False
        else:
            self.label.setText('<p style="line-height:60px;">没搜到耶，要不换个词试试看？</p>')

    #搜索确认按钮槽函数
    def search_confirm(self):
        self.search()

    #音乐播放按钮槽函数
    def music_button_click(self):
        self.music_button.isChecked = not self.music_button.isChecked
        if self.music_button.isChecked:
            self.mediaPlayer.player.pause()
            self.music_button.setIcon(QtGui.QIcon("resources/pictures/start.png"))
            self.music_button.setIconSize(QtCore.QSize(int(self.width*0.045), int(self.width*0.045)))
        else:
            self.mediaPlayer.player.play()
            self.music_button.setIcon(QtGui.QIcon("resources/pictures/pause.png"))
            self.music_button.setIconSize(QtCore.QSize(int(self.width*0.045), int(self.width*0.045)))

    #音乐上一首按钮槽函数
    def last_music(self):
        self.mediaPlayer.playlist.previous()
        self.music_name.setText(self.mediaPlayer.get_current_music_name())

    #音乐下一首按钮槽函数
    def next_music(self):
        self.mediaPlayer.playlist.next()
        self.music_name.setText(self.mediaPlayer.get_current_music_name())
        print('current music:', self.mediaPlayer.get_current_music_name())

    def next_music_normal(self):
        if self.mediaPlayer.player.state() == QMediaPlayer.StoppedState:
            self.mediaPlayer.playlist.next()
            self.mediaPlayer.player.play()
            self.music_name.setText(self.mediaPlayer.get_current_music_name())


    #主界面的设置
    def retranslateUi(self, MainWindow):
        global textdic, sen_serial_num,sentence_sequence
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Daily Sentence"))
        MainWindow.setWindowIcon(QtGui.QIcon('resources/pictures/star.png'))
        self.search_confirm_button.setText(_translate("MainWindow", "✓"))
        self.label.setText(_translate("MainWindow", '<p style="line-height:60px;">{}</p>'.format(textdic[sentence_sequence[sen_serial_num]])))

    def retranslateFavorite(self, MainWindow):
        global textdic, sen_serial_num, love_list, love_serial_num
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Daily Sentence"))
        MainWindow.setWindowIcon(QtGui.QIcon('resources/pictures/star2.png'))
        self.search_confirm_button.setText(_translate("MainWindow", "✓"))
        self.label.setText(_translate("MainWindow", '<p style="line-height:60px;">{}</p>'.format(textdic[love_list_copy[love_serial_num]])))

    def retranslateSearch(self, MainWindow):
        global textdic, sen_serial_num, searched_list
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Daily Sentence"))
        MainWindow.setWindowIcon(QtGui.QIcon('resources/pictures/star2.png'))
        self.search_confirm_button.setText(_translate("MainWindow", "✓"))
        if searched_list:
            self.label.setText(_translate("MainWindow", '<p style="line-height:60px;">{}</p>'.format(textdic[searched_list[0]])))
        else:
            self.label.setText(_translate("MainWindow", '<p style="line-height:60px;">未找到</p>'))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.mediaPlayer.player.play()
    style_file = './style.qss'
    style_sheet = QSSLoader.read_qss_file(style_file)
    MainWindow.setStyleSheet(style_sheet)
    MainWindow.show()
    app.exec_()
    if ui.star.isChecked:
        love_list = set(love_list_copy)|set(love_list_copy_copy)
    else:
        love_list = set(love_list_copy).intersection(set(love_list_copy_copy))

    import_love.write_love_to_file(love_list, 'love.md')
    print('love_list:', love_list)
    sys.exit()