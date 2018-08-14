import sys
from PyQt5.QtWidgets import *
from ctypes.wintypes import *
import win32api
import win32con
import win32gui

hwnd = 0


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.init_layout()

    def init_layout(self):
        w_layout = QHBoxLayout()

        h_layout = QHBoxLayout()
        h_layout.addWidget(QPushButton(str(1)))
        h_layout.addWidget(QPushButton(str(2)))

        v_layout = QVBoxLayout()
        v_layout.addWidget(QPushButton(str(3)))
        v_layout.addWidget(QPushButton(str(4)))

        g_layout = QGridLayout()
        g_layout.addWidget(QPushButton(str(5)), 0, 0)
        g_layout.addWidget(QPushButton(str(6)), 0, 1)
        g_layout.addWidget(QPushButton(str(7)), 1, 0)
        g_layout.addWidget(QPushButton(str(8)), 1, 1)

        f_layout = QFormLayout()
        f_layout.addWidget(QPushButton(str(9)))
        f_layout.addWidget(QPushButton(str(10)))
        f_layout.addWidget(QPushButton(str(11)))
        f_layout.addWidget(QPushButton(str(12)))

        hwg = QWidget()
        vwg = QWidget()
        gwg = QWidget()
        fwg = QWidget()

        hwg.setLayout(h_layout)
        vwg.setLayout(v_layout)
        gwg.setLayout(g_layout)
        fwg.setLayout(f_layout)

        w_layout.addWidget(hwg)
        w_layout.addWidget(vwg)
        w_layout.addWidget(gwg)
        w_layout.addWidget(fwg)

        self.setLayout(w_layout)

    def nativeEvent(self, event_type, message):
        #  SendMessage(new IntPtr(StartupCommands.Hwnd), 0x9527, this.Handle, IntPtr.Zero);
        msg = ctypes.wintypes.MSG.from_address(message.__int__())
        # print(event_type, type(event_type))
        print('window hwnd = ', hwnd)
        # print('hwnd = ', msg.hWnd)
        print("message: ", msg.message)
        # print("pt: ", msg.pt)
        # print("time: ", msg.time)
        print("wParam: ", msg.wParam, type(msg.wParam))
        print("lParam: ", msg.lParam, type(msg.lParam))
        print('------------------------------------')
        return QWidget.nativeEvent(self, event_type, message)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = MainWindow()
    m.move(QApplication.desktop().availableGeometry().center() - m.rect().center())
    m.show()
    hwnd = int(m.winId())
    print('==============================', hwnd, '==============================')

    sys.exit(app.exec_())
