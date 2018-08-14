import os
import sys
import subprocess
import threading
import win32gui
import time
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

report_process_id = 0


def get_handle_id():
    report_window_title = None
    # report_window_title = 'NESTED_F4_REPORT_WINDOW'
    # report_window_title = 'FF POS系统 - [常用报表]'
    report_window_class = 'WindowsForms10.Window.8.app.0.1ca0192_r9_ad1'

    # report_window_title = '计算器'
    # report_window_class = 'ApplicationFrameWindow'
    hwnd = win32gui.FindWindow(report_window_class, report_window_title)
    print('get_handle_id hwnd = ', hwnd)
    if hwnd == 0:
        start = time.time()
        while hwnd == 0:
            time.sleep(0.5)
            hwnd = win32gui.FindWindow(report_window_class, report_window_title)
            print('get_handle_id while hwnd = ', hwnd)
            end = time.time()
            if hwnd != 0 or end - start > 10:
                # print('handle = ', hwnd)
                # print('title = ', win32gui.GetWindowText(hwnd))
                # print('class = ', win32gui.GetClassName(hwnd))
                return hwnd
    else:
        return hwnd


def launch_report():
    global report_process_id
    # exe_path = "C:\\Windows\\system32\\calc.exe"
    exe_path = "D:\\report demo\\FastFish.Client.Pos.Win.exe debug -n:3203401 -p:1234 -b:true -m:false -pid:" + str(
        os.getpid()) + ' -t:NESTED_F4_REPORT_WINDOW'
    print('exe_path = ', exe_path)
    report_process = subprocess.Popen(exe_path)
    report_process_id = report_process.pid


class Report(QWidget):
    def __init__(self, child_window):
        super(Report, self).__init__()
        self.report_window = child_window
        embed = self.createWindowContainer(self.report_window, self)
        window_layout = QHBoxLayout()
        window_layout.setContentsMargins(0, 0, 0, 0)
        window_layout.addWidget(embed)

        self.setLayout(window_layout)

    def closeEvent(self, event):
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    t = threading.Thread(target=launch_report)
    t.start()
    t.join()

    nest_window = True

    if nest_window:
        hwnd = get_handle_id()
        print('main thread hwnd = ', hwnd)
        report_window = QWindow.fromWinId(get_handle_id())
        report_window.showFullScreen()
        print('report_window = ', int(report_window.winId()))
        window = Report(report_window)
        window.resize(1500, 900)
        window.setWindowTitle('The title of main window')
        window.move(QApplication.desktop().availableGeometry().center() - window.rect().center())
        window.show()

    sys.exit(app.exec_())
