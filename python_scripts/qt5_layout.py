import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from ctypes.wintypes import *
import win32api
import win32con
import win32gui

hwnd = 0


class Dialog(QDialog):
    def __init__(self, params={
        'description': 'Description Info',
        'leftButtonText': 'Left Button',
        'rightButtonText': 'Right Button',
        'leftButtonAction': 'close',
        'rightButtonAction': 'cancel'
    }):
        super(Dialog, self).__init__()
        self.m_drag = False
        self.m_DragPosition = 0
        self.params = params
        self.init()
        self.init_style()
        self.exec_()

    def init(self):
        action = {
            'close': self.self_close,
            'cancel': self.close
        }
        self.resize(600, 200)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowModality(Qt.ApplicationModal)

        v_layout = QVBoxLayout()

        h_layout_top = QHBoxLayout()
        h_layout_top.setContentsMargins(0, 0, 0, 0)
        h_layout_top.setSpacing(0)

        h_layout_bottom = QHBoxLayout()

        dialog_description = QLabel()
        dialog_description.setText(self.params['description'])
        dialog_description.setAlignment(Qt.AlignCenter)
        h_layout_top.addWidget(dialog_description)

        left_button = QPushButton(self.params['leftButtonText'])
        left_button.clicked.connect(action[self.params['leftButtonAction']])
        right_button = QPushButton(self.params['rightButtonText'])
        right_button.clicked.connect(action[self.params['rightButtonAction']])

        h_layout_bottom.addStretch(1)
        h_layout_bottom.addWidget(left_button)
        h_layout_bottom.addStretch(1)
        h_layout_bottom.addWidget(right_button)
        h_layout_bottom.addStretch(1)

        top_widget = QWidget()
        top_widget.setProperty('name', 'top_widget')

        bottom_widget = QWidget()
        bottom_widget.setProperty('name', 'bottom_widget')

        top_widget.setLayout(h_layout_top)
        bottom_widget.setLayout(h_layout_bottom)

        v_layout.addWidget(top_widget, 1)
        v_layout.addWidget(bottom_widget, 2)
        v_layout.setSpacing(0)
        v_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(v_layout)

    def init_style(self):
        style = """
          QWidget [name="top_widget"] {
            background-color: green;
          }
          QWidget [name="bottom_widget"] {
            background-color: #000;
          }
          QPushButton {
            background-color: red;
             color: #fff;
             font-family: Microsoft YaHei;
             text-align: center;
             border-radius: 5px;
             width: 120px;
             height: 50px;
          }
          QLabel {
             background-color: blue;
             color: #fff;
             font-family: Microsoft YaHei;
             text-align: center;
             font-size: 25px;
           }
        """
        self.setStyleSheet(style)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.m_drag and event.buttons() and Qt.LeftButton:
            self.move(event.globalPos() - self.m_DragPosition)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.m_drag = False

    def self_close(self):
        self.close()


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.init_layout()

    @staticmethod
    def show_dialog():
        Dialog()

    def init_layout(self):
        w_layout = QHBoxLayout()

        h_layout = QHBoxLayout()
        btn1 = QPushButton(str(1))
        btn1.clicked.connect(self.show_dialog)
        h_layout.addWidget(btn1)
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
        # print('window hwnd = ', hwnd)
        # print('hwnd = ', msg.hWnd)
        # print("message: ", msg.message)
        # print("pt: ", msg.pt)
        # print("time: ", msg.time)
        # print("wParam: ", msg.wParam, type(msg.wParam))
        # print("lParam: ", msg.lParam, type(msg.lParam))
        # print('------------------------------------')
        return QWidget.nativeEvent(self, event_type, message)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = MainWindow()
    m.move(QApplication.desktop().availableGeometry().center() - m.rect().center())
    m.setWindowTitle('this is a title')
    m.show()
    m.show_dialog()

    # m1 = MainWindow()
    # m1.move(QApplication.desktop().availableGeometry().center() - m1.rect().center())
    # m1.show()

    hwnd = int(m.winId())
    print('==============================', hwnd, '==============================')

    sys.exit(app.exec_())
