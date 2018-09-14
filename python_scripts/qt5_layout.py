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
        'topBgColor': '#2a5596',
        'topFontSize': 24,
        'buttonBgColor': '#2a5596',
        'middleFontColor': '#2a5596',
        'middleFontSize': 16,
        'title': 'Dialog Title',
        'description': 'Description Info',
        'dialogWidth': 360,
        'dialogHeight': 201,
        'leftButtonText': 'Left Button',
        'rightButtonText': 'Right Button',
        'leftButtonAction': 'close',
        'rightButtonAction': 'cancel',
        'buttonWidth': 110,
        'buttonHeight': 34,
        'buttonFontSize': 16,
        'borderRadius': 6,
        'blurRadius': 20
    }):
        super(Dialog, self).__init__()
        self.pixel_ratio = 1.25
        self.m_drag = False
        self.m_DragPosition = 0
        self.params = params
        self.init()
        self.init_style()
        # self.show()
        # q = QEventLoop()
        # q.exec_()
        self.exec_()

    def init(self):
        action = {
            'close': self.self_close,
            'cancel': self.close
        }
        width = self.params['dialogWidth'] * self.pixel_ratio + self.params['blurRadius'] * 2 * self.pixel_ratio
        height = self.params['dialogHeight'] * self.pixel_ratio + self.params['blurRadius'] * 2 * self.pixel_ratio
        self.resize(width, height)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowModality(Qt.ApplicationModal)
        shadow_effect = QGraphicsDropShadowEffect(self)
        shadow_effect.setColor(Qt.gray)
        shadow_effect.setBlurRadius(self.params['blurRadius'])
        shadow_effect.setOffset(0, 0)
        self.setGraphicsEffect(shadow_effect)
        self.setContentsMargins(self.params['blurRadius'] * self.pixel_ratio,
                                self.params['blurRadius'] * self.pixel_ratio,
                                self.params['blurRadius'] * self.pixel_ratio,
                                self.params['blurRadius'] * self.pixel_ratio)

        v_layout = QVBoxLayout()

        h_layout_top = QHBoxLayout()
        h_layout_top.setContentsMargins(0, 0, 0, 0)
        h_layout_top.setSpacing(0)

        h_layout_middle = QHBoxLayout()
        h_layout_middle.setContentsMargins(0, 0, 0, 0)
        h_layout_middle.setSpacing(0)

        h_layout_bottom = QHBoxLayout()

        dialog_title = QLabel()
        dialog_title.setText(self.params['title'])
        dialog_title.setAlignment(Qt.AlignCenter)
        dialog_title.setObjectName('dialog_title')
        h_layout_top.addWidget(dialog_title)

        dialog_description = QLabel()
        dialog_description.setText(self.params['description'])
        dialog_description.setAlignment(Qt.AlignCenter)
        dialog_description.setObjectName('dialog_description')
        h_layout_middle.addWidget(dialog_description)

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

        middle_widget = QWidget()
        middle_widget.setProperty('name', 'middle_widget')

        bottom_widget = QWidget()
        bottom_widget.setProperty('name', 'bottom_widget')

        top_widget.setLayout(h_layout_top)
        middle_widget.setLayout(h_layout_middle)
        bottom_widget.setLayout(h_layout_bottom)

        v_layout.addWidget(top_widget, 50)
        v_layout.addWidget(middle_widget, 101)
        v_layout.addWidget(bottom_widget, 50)
        v_layout.setSpacing(0)
        v_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(v_layout)

    def init_style(self):
        style = """
          QWidget [name="top_widget"] {
            background-color: [topBgColor];
            border-top-left-radius: [borderRadius];
            border-top-right-radius:[borderRadius];
          }
          QWidget [name="middle_widget"] {
            background-color: [middleBgColor];
          }
          QWidget [name="bottom_widget"] {
            border-top: 1px solid #dcdcdc;
            background-color: [bottomBgColor];
            border-bottom-left-radius:[borderRadius];
            border-bottom-right-radius:[borderRadius];
          }
          QPushButton {
            background-color: [buttonBgColor];
            color: #fff;
            font-family: Microsoft YaHei;
            text-align: center;
            border-radius: 5px;
            width: [buttonWidth];
            height: [buttonHeight];
            font-size: [buttonFontSize];
          }
          QLabel {
            font-family: Microsoft YaHei;
            text-align: center;
          }
          #dialog_title {
            color: #fff;
            font-size: [topFontSize];
          }
          #dialog_description{
            color: [middleFontColor];
            font-size: [middleFontSize]
          }
        """
        style = style.replace('[borderRadius]', str(self.params['borderRadius'] * self.pixel_ratio) + 'px')
        style = style.replace('[topBgColor]', self.params['topBgColor'])
        style = style.replace('[middleBgColor]', '#fff')
        style = style.replace('[bottomBgColor]', '#fff')
        style = style.replace('[buttonWidth]', str(self.params['buttonWidth'] * self.pixel_ratio) + 'px')
        style = style.replace('[buttonHeight]', str(self.params['buttonHeight'] * self.pixel_ratio) + 'px')
        style = style.replace('[buttonBgColor]', self.params['buttonBgColor'])
        style = style.replace('[middleFontColor]', self.params['middleFontColor'])
        style = style.replace('[middleFontSize]', str(int(self.params['middleFontSize'] * self.pixel_ratio)) + 'px')
        style = style.replace('[topFontSize]', str(int(self.params['topFontSize'] * self.pixel_ratio)) + 'px')
        style = style.replace('[buttonFontSize]', str(int(self.params['buttonFontSize'] * self.pixel_ratio)) + 'px')
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
