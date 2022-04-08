import pyautogui, time, os

# print(os.path.split(os.path.realpath(__file__))[0]+ "\\giao.png")

pyautogui.doubleClick(30, 20, button='left')  # 点图标,写死为屏幕左上角第一个图标坐标

time.sleep(2)
giaooo = pyautogui.locateOnScreen(os.path.split(os.path.realpath(__file__))[0] + "\\giao.png")
pyautogui.click(x=giaooo[0] + 30, y=giaooo[1] + 20, button='left')
