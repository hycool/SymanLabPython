import win32api
import win32con

if __name__ == '__main__':
    print('u will send message')
    win32api.SendMessage(920928, 0x9527, 0, 0)
