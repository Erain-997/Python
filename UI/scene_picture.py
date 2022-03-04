# author:Erain
# date: 2021/10/4

import qtawesome
from PyQt5 import QtCore, QtGui, QtWidgets

class PictureScene(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # 主窗口
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.right_layout = QtWidgets.QGridLayout()  # 创建右侧部件的网格布局层
        self.right_widget = QtWidgets.QWidget()  # 创建右侧部件
        self.left_layout = QtWidgets.QGridLayout()  # 创建左侧部件的网格布局层
        self.left_widget = QtWidgets.QWidget()  # 创建左侧部件

        self.left_close = QtWidgets.QPushButton("")  #
        self.init_main = QtWidgets.QPushButton("")  # 返回主界面按钮
        self.left_mini = QtWidgets.QPushButton("")  # 最小化按

        # list
        self.button_home = QtWidgets.QPushButton("主界面")
        self.button_home.setObjectName('left_label')
        self.label_life = QtWidgets.QPushButton("人生计划")
        self.label_life.setObjectName('left_label')
        self.button_picture = QtWidgets.QPushButton(qtawesome.icon('fa.sellsy', color='white'), "画")
        self.button_picture.setObjectName('list_button')
        self.button_poem = QtWidgets.QPushButton(qtawesome.icon('fa.film', color='white'), "诗")
        self.button_poem.setObjectName('list_button')
        self.button_music = QtWidgets.QPushButton(qtawesome.icon('fa.music', color='white'), "乐")
        self.button_music.setObjectName('list_button')
        self.label_live = QtWidgets.QPushButton("在人间")
        self.label_live.setObjectName('left_label')
        self.button_child = QtWidgets.QPushButton(qtawesome.icon('fa.child', color='white'), "童年")
        self.button_child.setObjectName('list_button')
        self.button_youth = QtWidgets.QPushButton(qtawesome.icon('fa.star', color='white'), "青春")
        self.button_youth.setObjectName('list_button')
        self.button_upper = QtWidgets.QPushButton(qtawesome.icon('fa.comment', color='white'), "立")
        self.button_upper.setObjectName('list_button')
        self.button_her = QtWidgets.QPushButton(qtawesome.icon('fa.heart', color='white'), "她")
        self.button_her.setObjectName('list_button')
        self.label_learn = QtWidgets.QPushButton("活着")
        self.label_learn.setObjectName('left_label')
        self.button_forward = QtWidgets.QPushButton(qtawesome.icon('fa.forward', color='white'), "向前")
        self.button_forward.setObjectName('list_button')
        self.button_stop = QtWidgets.QPushButton(qtawesome.icon('fa.stop', color='white'), "停下")
        self.button_stop.setObjectName('list_button')

        # right
        self.right_bar_widget = QtWidgets.QWidget()  # 右侧顶部搜索框部件
        self.right_bar_layout = QtWidgets.QGridLayout()  # 右侧顶部搜索框网格布局
        self.right_bar_widget.setLayout(self.right_bar_layout)
        self.search_icon = QtWidgets.QLabel(chr(0xf002) + ' ' + '搜索  ')
        self.search_icon.setFont(qtawesome.font('fa', 16))
        self.right_bar_widget_search_input = QtWidgets.QLineEdit()
        self.right_bar_widget_search_input.setPlaceholderText("检索，反思，沉沦...")

        self.right_recommend_label = QtWidgets.QLabel("那年今日")
        self.right_recommend_label.setObjectName('right_lable')
        self.right_recommend_widget = QtWidgets.QWidget()  # 推荐封面部件
        self.right_recommend_layout = QtWidgets.QGridLayout()  # 推荐封面网格布局
        self.right_recommend_widget.setLayout(self.right_recommend_layout)
        self.right_newsong_lable = QtWidgets.QLabel("你看")
        self.right_playlist_lable = QtWidgets.QLabel("你听")

        # recommend
        self.recommend_button_1 = QtWidgets.QToolButton()
        self.recommend_button_2 = QtWidgets.QToolButton()
        self.recommend_button_3 = QtWidgets.QToolButton()
        self.recommend_button_4 = QtWidgets.QToolButton()
        self.recommend_button_5 = QtWidgets.QToolButton()

        # 你看
        self.right_newsong_widget = QtWidgets.QWidget()
        self.right_newsong_layout = QtWidgets.QGridLayout()
        self.newsong_button_1 = QtWidgets.QPushButton("夜机      陈慧娴      永远的朋友      03::29")
        self.newsong_button_2 = QtWidgets.QPushButton("夜机      陈慧娴      永远的朋友      03::29")
        self.newsong_button_3 = QtWidgets.QPushButton("夜机      陈慧娴      永远的朋友      03::29")
        self.newsong_button_4 = QtWidgets.QPushButton("夜机      陈慧娴      永远的朋友      03::29")
        self.newsong_button_5 = QtWidgets.QPushButton("夜机      陈慧娴      永远的朋友      03::29")
        self.newsong_button_6 = QtWidgets.QPushButton("夜机      陈慧娴      永远的朋友      03::29")

        # playlist
        self.right_playlist_widget = QtWidgets.QWidget()  # 播放歌单部件
        self.right_playlist_layout = QtWidgets.QGridLayout()  # 播放歌单网格布局
        self.playlist_button_1 = QtWidgets.QToolButton()
        self.playlist_button_2 = QtWidgets.QToolButton()
        self.playlist_button_3 = QtWidgets.QToolButton()
        self.playlist_button_4 = QtWidgets.QToolButton()

        # console
        self.right_process_bar = QtWidgets.QProgressBar()  # 播放进度部件
        self.right_playconsole_widget = QtWidgets.QWidget()  # 播放控制部件
        self.right_playconsole_layout = QtWidgets.QGridLayout()  # 播放控制部件网格布局层
        self.console_button_1 = QtWidgets.QPushButton(qtawesome.icon('fa.backward', color='#F76677'), "")
        self.console_button_2 = QtWidgets.QPushButton(qtawesome.icon('fa.forward', color='#F76677'), "")

        self.main_scene()
        self.main_left_scene()
        self.main_right_scene()
        self.init_ui()

    def main_scene(self):
        self.setFixedSize(960, 700)
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局
        self.setCentralWidget(self.main_widget)  # 设置窗口主部件

    def main_left_scene(self):
        self.left_widget.setObjectName('left_widget')
        self.left_widget.setLayout(self.left_layout)  # 设置左侧部件布局为网格
        self.main_layout.addWidget(self.left_widget, 0, 0, 12, 2)  # 左侧部件在第0行第0列，占8行3列
        self.left_layout.addWidget(self.left_mini, 0, 0, 1, 1)
        self.left_layout.addWidget(self.left_close, 0, 2, 1, 1)
        self.left_layout.addWidget(self.init_main, 0, 1, 1, 1)
        self.left_layout.addWidget(self.label_life, 1, 0, 1, 3)
        self.left_layout.addWidget(self.button_picture, 2, 0, 1, 3)
        self.left_layout.addWidget(self.button_poem, 3, 0, 1, 3)
        self.left_layout.addWidget(self.button_music, 4, 0, 1, 3)
        self.left_layout.addWidget(self.label_live, 5, 0, 1, 3)
        self.left_layout.addWidget(self.button_child, 6, 0, 1, 3)
        self.left_layout.addWidget(self.button_youth, 7, 0, 1, 3)
        self.left_layout.addWidget(self.button_upper, 8, 0, 1, 3)
        self.left_layout.addWidget(self.label_learn, 10, 0, 1, 3)
        self.left_layout.addWidget(self.button_forward, 11, 0, 1, 3)
        self.left_layout.addWidget(self.button_stop, 12, 0, 1, 3)
        self.left_layout.addWidget(self.button_her, 9, 0, 1, 3)

    def main_right_scene(self):
        self.right_widget.setObjectName('right_widget')
        self.right_widget.setLayout(self.right_layout)  # 设置右侧部件布局为网格
        self.main_layout.addWidget(self.right_widget, 0, 2, 12, 10)  # 右侧部件在第0行第3列，占8行9列
        self.right_bar_layout.addWidget(self.search_icon, 0, 0, 1, 1)
        self.right_bar_layout.addWidget(self.right_bar_widget_search_input, 0, 1, 1, 8)
        self.right_layout.addWidget(self.right_bar_widget, 0, 0, 1, 9)

    def init_ui(self):
        self.recommend_button_1.setText("今天")  # 设置按钮文本
        self.recommend_button_1.setIcon(QtGui.QIcon('repository/pic/r1.jpg'))  # 设置按钮图标
        self.recommend_button_1.setIconSize(QtCore.QSize(100, 100))  # 设置图标大小
        self.recommend_button_1.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)  # 设置按钮形式为上图下文

        self.recommend_button_2.setText("昨天")
        self.recommend_button_2.setIcon(QtGui.QIcon('repository/pic/r1.jpg'))
        self.recommend_button_2.setIconSize(QtCore.QSize(100, 100))
        self.recommend_button_2.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_3.setText("明天")
        self.recommend_button_3.setIcon(QtGui.QIcon('repository/pic/r1.jpg'))
        self.recommend_button_3.setIconSize(QtCore.QSize(100, 100))
        self.recommend_button_3.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_4.setText("那年")
        self.recommend_button_4.setIcon(QtGui.QIcon('repository/pic/r1.jpg'))
        self.recommend_button_4.setIconSize(QtCore.QSize(100, 100))
        self.recommend_button_4.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_5.setText("某天")
        self.recommend_button_5.setIcon(QtGui.QIcon('repository/pic/r1.jpg'))
        self.recommend_button_5.setIconSize(QtCore.QSize(100, 100))
        self.recommend_button_5.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.right_recommend_layout.addWidget(self.recommend_button_1, 0, 0)
        self.right_recommend_layout.addWidget(self.recommend_button_2, 0, 1)
        self.right_recommend_layout.addWidget(self.recommend_button_3, 0, 2)
        self.right_recommend_layout.addWidget(self.recommend_button_4, 0, 3)
        self.right_recommend_layout.addWidget(self.recommend_button_5, 0, 4)

        self.right_layout.addWidget(self.right_recommend_label, 1, 0, 1, 9)
        self.right_layout.addWidget(self.right_recommend_widget, 2, 0, 2, 9)
        self.right_newsong_lable.setObjectName('right_lable')
        self.right_playlist_lable.setObjectName('right_lable')
        self.right_newsong_widget.setLayout(self.right_newsong_layout)
        self.right_newsong_layout.addWidget(self.newsong_button_1, 0, 1, )
        self.right_newsong_layout.addWidget(self.newsong_button_2, 1, 1, )
        self.right_newsong_layout.addWidget(self.newsong_button_3, 2, 1, )
        self.right_newsong_layout.addWidget(self.newsong_button_4, 3, 1, )
        self.right_newsong_layout.addWidget(self.newsong_button_5, 4, 1, )
        self.right_newsong_layout.addWidget(self.newsong_button_6, 5, 1, )
        self.right_playlist_widget.setLayout(self.right_playlist_layout)



        self.right_playlist_layout.addWidget(self.playlist_button_1, 0, 0)
        self.right_playlist_layout.addWidget(self.playlist_button_2, 0, 1)
        self.right_playlist_layout.addWidget(self.playlist_button_3, 1, 0)
        self.right_playlist_layout.addWidget(self.playlist_button_4, 1, 1)

        self.right_layout.addWidget(self.right_newsong_lable, 4, 0, 1, 5)
        self.right_layout.addWidget(self.right_playlist_lable, 4, 5, 1, 4)
        self.right_layout.addWidget(self.right_newsong_widget, 5, 0, 1, 5)
        self.right_layout.addWidget(self.right_playlist_widget, 5, 5, 1, 4)

        self.right_process_bar.setValue(49)
        self.right_process_bar.setFixedHeight(3)  # 设置进度条高度
        self.right_process_bar.setTextVisible(False)  # 不显示进度条文字
        self.right_playconsole_widget.setLayout(self.right_playconsole_layout)

        self.right_playconsole_layout.addWidget(self.console_button_1, 0, 0)
        self.right_playconsole_layout.addWidget(self.console_button_2, 0, 2)
        self.right_playconsole_layout.setAlignment(QtCore.Qt.AlignCenter)  # 设置布局内部件居中显示
        self.right_layout.addWidget(self.right_process_bar, 9, 0, 1, 9)
        self.right_layout.addWidget(self.right_playconsole_widget, 10, 0, 1, 9)

        ##################################################################################################
        # 使用QSS和部件属性美化窗口部件
        #
        self.left_close.setFixedSize(15, 15)  # 设置关闭按钮的大小
        self.init_main.setFixedSize(15, 15)  # 设置按钮大小
        self.left_mini.setFixedSize(15, 15)  # 设置最小化按钮大小
        # 通过setStyleSheet()方法，设置按钮部件的QSS样式
        # 左侧按钮默认为淡绿色，鼠标悬浮时为深绿色；
        # 中间按钮默认为淡黄色，鼠标悬浮时为深黄色；
        # 右侧按钮默认为浅红色，鼠标悬浮时为红色。
        self.left_close.setStyleSheet(
            '''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')
        self.init_main.setStyleSheet(
            '''QPushButton{background:#F7D674;border-radius:5px;}QPushButton:hover{background:yellow;}''')
        self.left_mini.setStyleSheet(
            '''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')
        # 左侧菜单美化
        self.left_widget.setStyleSheet('''
            QPushButton{border:none;color:white;}
            QPushButton#left_label{
                border:none;
                border-bottom:1px solid white;
                font-size:18px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
            QPushButton#left_button:hover{border-left:4px solid red;font-weight:700;}#去掉按钮的边框
        ''')
        # 边框圆角处理
        self.right_bar_widget_search_input.setStyleSheet(
            '''QLineEdit{
                    border:1px solid gray;
                    width:300px;
                    border-radius:10px;
                    padding:2px 4px;
            }''')

        self.right_widget.setStyleSheet('''
            QWidget#right_widget{
                color:#232C51;
                background:white;
                border-top:1px solid darkGray;
                border-bottom:1px solid darkGray;
                border-right:1px solid darkGray;
                border-top-right-radius:10px;
                border-bottom-right-radius:10px;
            }
            QLabel#right_lable{
                border:none;
                font-size:16px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
        ''')

        self.right_recommend_widget.setStyleSheet(
            '''
                QToolButton{border:none;}
                QToolButton:hover{border-bottom:2px solid #F76677;}
            ''')
        self.right_playlist_widget.setStyleSheet(
            '''
                QToolButton{border:none;}
                QToolButton:hover{border-bottom:2px solid #F76677;}
            ''')

        self.right_newsong_widget.setStyleSheet('''
            QPushButton{
                border:none;
                color:gray;
                font-size:12px;
                height:40px;
                padding-left:5px;
                padding-right:10px;
                text-align:left;
            }
            QPushButton:hover{
                color:black;
                border:1px solid #F3F3F5;
                border-radius:10px;
                background:LightGray;
            }
        ''')

        self.right_process_bar.setStyleSheet('''
            QProgressBar::chunk {
                background-color: #F76677;
            }
        ''')

        self.right_playconsole_widget.setStyleSheet('''
            QPushButton{
                border:none;
            }
        ''')

        self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明

        # self.right_newsong_widget.setStyleSheet('''
        # QWidget#left_widget{
        #     background: gray;
        #     border - top: 1pxsolidwhite;
        #     border - bottom: 1pxsolidwhite;
        #     border - left: 1pxsolidwhite;
        #     border - top - left - radius: 10px;
        #     border - bottom - left - radius: 10px;}
        #     ''')

        self.main_layout.setSpacing(0)  # 去缝
