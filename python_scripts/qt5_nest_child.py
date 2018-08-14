import os
import sys
import subprocess
import threading
import win32gui
import time
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class Report(QMainWindow):
    def __init__(self, child_window):
        super(Report, self).__init__()
        self.report_window = child_window
        # self.createWindowContainer(self.report_window, self)
        self.resize(1200, 800)
        self.move(QApplication.desktop().availableGeometry().center() - self.rect().center())
        self.setWindowTitle('报表内嵌机制测试')
        self.show()

    def closeEvent(self, event):
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = QWidget()
    palette = QPalette()
    palette.setColor(w.backgroundRole(), QColor(0, 0, 0))
    w.setPalette(palette)
    w_layout = QHBoxLayout()
    w_layout.addWidget(QPushButton(str(1)))
    w.setLayout(w_layout)
    w.setWindowTitle('this is w')
    w.showFullScreen()
    sub = QWindow.fromWinId(w.winId())
    sub.setFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.FramelessWindowHint | Qt.WA_TranslucentBackground)

    print('w handle = ', int(w.winId()))
    print('sub handle =', int(sub.winId()))

    m = QWidget()
    m_palette = QPalette()
    m_palette.setColor(w.backgroundRole(), QColor(51, 141, 230))
    m.setPalette(m_palette)
    m.createWindowContainer(sub, parent=m)

    embed = QWidget.createWindowContainer(sub, parent=m)
    print('embed handle = ', int(embed.winId()))
    m_layout = QHBoxLayout()
    m_layout.setContentsMargins(0, 0, 0, 0)
    m_layout.setSpacing(0)
    m_layout.addWidget(embed)
    m.setLayout(m_layout)

    m.resize(1200, 800)

    m.setWindowTitle('this is m')
    m.move(QApplication.desktop().availableGeometry().center() - m.rect().center())
    m.show()

    sys.exit(app.exec_())
