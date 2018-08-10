import os
import sys
import subprocess
import threading
import win32gui
import time
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

Qt

report_process_id = 0


def get_handle_id():
    # report_window_title = '快鱼POS系统'
    # report_window_class = 'WindowsForms10.Window.8.app.0.141b42a_r9_ad1'

    report_window_title = '计算器'
    report_window_class = 'ApplicationFrameWindow'
    hwnd = win32gui.FindWindow(report_window_class, report_window_title)
    if hwnd == 0:
        start = time.time()
        while hwnd == 0:
            time.sleep(0.01)
            hwnd = win32gui.FindWindow(report_window_class, report_window_title)
            end = time.time()
            if hwnd != 0 or end - start > 5:
                return hwnd
    else:
        return hwnd


def launch_report():
    global report_process_id
    exe_path = "C:\\Windows\\system32\\calc.exe"
    # exe_path = "D:\\report demo\\FastFish.Client.Pos.Win.exe debug -n:3203401 -p:1234 -b:false -m:false"
    report_process = subprocess.Popen(exe_path)
    report_process_id = report_process.pid


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

    # t = threading.Thread(target=launch_report)
    # t.start()
    # t.join()

    # report_window = QWindow.fromWinId(get_handle_id())
    # window = Report(report_window)
    # window.createWindowContainer(report_window, window)

    w = QWidget()
    w.resize(300, 300)
    palette = QPalette()
    palette.setColor(w.backgroundRole(), QColor(0, 0, 0))
    w.setPalette(palette)
    sub = QWindow.fromWinId(w.winId())

    m = QMainWindow()
    m.createWindowContainer(sub, parent=m, flags=Qt.FramelessWindowHint)
    m.resize(500, 500)
    m.move(QApplication.desktop().availableGeometry().center() - m.rect().center())
    m.show()

    sys.exit(app.exec_())
