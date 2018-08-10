import os
import sys
import subprocess
import atexit
from PyQt5 import QtWidgets


class CalcWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(CalcWindow, self).__init__()
        self.setWindowTitle("Embedded Calc")
        lines_widget = LinesWidget()
        self.setCentralWidget(lines_widget)
        calc_path = "C:\\Windows\\system32\\calc.exe"
        print("Path = " + calc_path)
        print("Exists: " + str(os.path.exists(calc_path)))
        p = subprocess.Popen(calc_path)
        atexit.register(self.kill_proc, p)

    @staticmethod
    def kill_proc(proc):
        try:
            proc.terminate()
        except Exception:
            pass


class LinesWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.vLayout = QtWidgets.QVBoxLayout()
        self.line1 = QtWidgets.QHBoxLayout()
        self.line1.addWidget(QtWidgets.QLabel("HELLO"))
        self.line1.addWidget(QtWidgets.QLabel("WORLD"))
        self.line2 = QtWidgets.QHBoxLayout()
        self.line2.addWidget(QtWidgets.QLabel("SUP"))
        self.line2.addWidget(QtWidgets.QLabel("DAWG"))
        self.vLayout.addLayout(self.line1)
        self.vLayout.addLayout(self.line2)
        self.setLayout(self.vLayout)


def main():
    app = QtWidgets.QApplication(sys.argv)
    calc = CalcWindow()
    calc.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()