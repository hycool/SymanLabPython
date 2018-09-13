import win32api
import win32con

if __name__ == '__main__':
    print('u will send message')
    win32api.SendMessage(2426910, win32con.WM_SETTEXT, None, '00000000')
