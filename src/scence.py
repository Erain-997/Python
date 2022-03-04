# author:Erain
# date: 2021/10/5

from UI.scene_main import MainScene
from UI.scene_picture import PictureScene


def erain_life():
    main = MainScene()
    main.show()  # 初始化主界面
    # 初始化各个界面
    pic = PictureScene()
    # 页面跳转
    main.init_main.clicked.connect(lambda: {main.close(), pic.show()})
    pic.button_poem.clicked.connect(lambda: {pic.close(), main.show()})
    pic.init_main.clicked.connect(lambda: {main.close(), pic.show()})
