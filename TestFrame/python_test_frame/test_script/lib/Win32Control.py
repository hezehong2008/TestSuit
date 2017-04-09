#!/usr/bin/env python
# -*- coding: UTF-8 -*
import json

import time
import win32gui, win32com.client
import win32con
import win32api
import logging
import sys
reload(sys)
sys.setdefaultencoding('gbk')

logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='logger_static_ui.log',
                    filemode='w')
__logger__ = logging.getLogger("logger")
__logger__.setLevel(logging.DEBUG)
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
__logger__.addHandler(ch)


class WinCtrl:
    def __init__(self, classname=None, title=None, ctrlType=None):
        self.classname = classname
        self.title = title

    def __getattr__(self, item):
        pass
        # json.loads()


class Win32Controller:

    @classmethod
    def getInstance(cls):
        pass

    def __init__(self, logger=None):
        if logger:
            self.logger = logger
        else:
            self.logger = __logger__

    def uploadFileFromDlg(self, filePath, dlgClassname ="#32770", dlgTitle ="打开", buttonTitle="打开",
                          buttonClassname="Button", editClassname="Edit", wait_time=10):
        """
        :param filePath:
        :param dlgClassname:
        :param dlgTitle:
        :param buttonTitle:
        :param buttonClassname:
        :param editClassname:
        :param wait_time:
        :return:  true or fault
        """

        hwnd = win32gui.GetDesktopWindow()
        hwndChildList = self.get_child_windows(parent=hwnd)
        button_list = ()
        for item in hwndChildList:
            title, classname = str(win32gui.GetWindowText(item)), str(win32gui.GetClassName(item))
            title = title.replace(" ", "")
            if classname.find(dlgClassname) != -1:
                try:
                    title = title.decode('gbk').encode('utf-8')
                except Exception:
                    pass
                if title.find(dlgTitle) != -1:
                    self.logger.debug('*********************** Get Dialog ********************%s %s '
                                 %(classname, title))
                    dlglist = self.get_child_windows(item)
                    for item2 in dlglist:
                        _title, classname = str(win32gui.GetWindowText(item2)), str(win32gui.GetClassName(item2))
                        try:
                            _title = _title.decode('gbk').encode('utf-8')
                        except Exception:
                            pass
                        if classname.find(editClassname) != -1:
                            self.input(item2, filePath)

                        if classname.find(buttonClassname) != -1 and _title.find(buttonTitle) != -1:
                            button_list = (item2, classname, _title)
                            time.sleep(wait_time)
                            self.logger.debug('******************* Get Button ****************** %s %s'
                                         % (classname, _title))
                    self.click(button_list[0])
                    return True

    def get_child_windows(self, parent):

        if not parent:
            return
        hwndChildList = []
        win32gui.EnumChildWindows(parent, lambda hwnd, param: param.append(hwnd), hwndChildList)
        return hwndChildList

    def input(self, hwnd, text):
        """
        :param hwnd:  the handle handle fof the windows
        :param text:
        :return:
        """
        time.sleep(0.01)
        win32gui.SetCursor(hwnd)
        ret = win32gui.SendMessage(hwnd, win32con.WM_SETTEXT, 0, text)
        return ret

    def click(self, hwnd):
        """
        click button specified by hwnd
        parameter: hwnd, handle of ctrl
        """
        ret = win32gui.SendMessage(hwnd, win32con.WM_SETFOCUS)
        ret = win32gui.SendMessage(hwnd, win32con.BM_CLICK)
        return ret

    def double_click(self, hwnd):
        """
        :param hwnd:
        :return:
        """
        ret = win32gui.SendMessage(hwnd, win32con.DOUBLE_CLICK)
        return ret

    def get_all_windows(self):
        hwnd = win32gui.GetDesktopWindow()
        hwndChildList = self.get_child_windows(parent=hwnd)
        return hwndChildList

    def get_text(self, hwnd):
        ''''''

        len = win32gui.SendMessage(hwnd, win32con.WM_GETTEXTLENGTH)+1
        buffer = '0'*len
        win32gui.SendMessage(hwnd, win32con.WM_GETTEXT, len, buffer)
        return buffer

    def findwindow(self, classname, title):
        """
        breadth-first traversal to find all the child ctrls in window
        parameters: classname is window's classname
                    title, windows's title
                    you can obtain above attributions by spy++
        return all the handle of ctrls in a window
        """
        try:
            parent = win32gui.FindWindow(classname, title)
            ctrls = [parent]
            ret_ctrls = []
            node = None
            child = None

            while ctrls != []:
                node = ctrls.pop(0)
                ret_ctrls.append(node)
                child = win32gui.GetWindow(node, win32con.GW_CHILD)
                while child is not 0:
                    ctrls.append(child)
                    child = win32gui.GetWindow(child, win32con.GW_HWNDNEXT)
        except win32gui.error, e :
            import logging
            logging.error('Fail to find win32 window')
            raise RuntimeError(e)
        return ret_ctrls

    def drag(self, x, y, x1, y1):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSE_MOVED)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)


if __name__ == "__main__":
    ctrl = Win32Controller()
    ctrl.drag(0,0, 100, 100)

