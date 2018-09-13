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

    w = QWidget()  # 模拟第三方应用
    palette = QPalette()
    palette.setColor(w.backgroundRole(), QColor(0, 0, 0))
    w.setPalette(palette)
    w_layout = QHBoxLayout()
    w_layout.addWidget(QPushButton(str(1)))
    w.setLayout(w_layout)
    w.showFullScreen()
    sub = QWindow.fromWinId(w.winId())
    sub.setFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.FramelessWindowHint | Qt.WA_TranslucentBackground)

    m = QWidget()  # 承载第三方应用窗口的控件
    m_palette = QPalette()
    m_palette.setColor(w.backgroundRole(), QColor(51, 141, 230))
    m.setPalette(m_palette)

    embed = QWidget.createWindowContainer(sub, parent=m)
    m_layout = QHBoxLayout()
    m_layout.setContentsMargins(0, 0, 0, 0)
    m_layout.setSpacing(0)
    m_layout.addWidget(embed)
    m.setLayout(m_layout)
    m.move(QApplication.desktop().availableGeometry().center() - m.rect().center())

    main_window = QMainWindow()  # 主窗口1
    main_window.setWindowTitle('QMainWindow1')
    main_window.setCentralWidget(m)
    main_window.resize(200, 200)
    # main_window.move(QApplication.desktop().availableGeometry().center() - main_window.rect().center())
    main_window.show()

    class SecondWindow(QMainWindow):
        def resizeEvent(self, event):
            main_window.resize(event.size().width(), event.size().height() - 80)

    second_window = SecondWindow()
    second_window.setWindowTitle('QMainWindow2')
    second_window.resize(800, 600)
    second_window.move(QApplication.desktop().availableGeometry().center() - second_window.rect().center())
    second_window.show()

    main_window.setParent(second_window)
    main_window.show()
    main_window.move(0, 80)
    main_window.resize(second_window.width(), second_window.height() - 80)

    sys.exit(app.exec_())
