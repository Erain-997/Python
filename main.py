# coding:utf-8

import sys

from PyQt5 import QtWidgets

from src.scence import erain_life


def main():
    app = QtWidgets.QApplication(sys.argv)
    erain_life()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
