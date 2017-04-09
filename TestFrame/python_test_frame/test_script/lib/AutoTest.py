#!/usr/bin/env python
# -*- coding: UTF-8 -*
import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
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
logger = logging.getLogger("logger")
logger.setLevel(logging.DEBUG)
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)


class TestScript(unittest.TestCase):
    def _point1(self):
        hwnd = win32gui.GetDesktopWindow()
        hwndChildList = self.get_child_windows(parent=hwnd)
        for item in hwndChildList:
            title, classname = str(win32gui.GetWindowText(item)), str(win32gui.GetClassName(item))

            title = title.replace(" ", "")
            if "#32770" in classname:
                try:
                    title = title.decode('gbk').encode('utf-8')
                except Exception:
                    pass
                if "打开" in title:
                    print '********************************* Get Dialog **************************'
                    print title, classname, item
                    print '********************************* Get Dialog **************************'
                    dlglist = self.get_child_windows(item)
                    for item2 in dlglist:
                        _title, classname = str(win32gui.GetWindowText(item2)), str(win32gui.GetClassName(item2))
                        try:
                            _title = _title.decode('gbk').encode('utf-8')
                        except Exception:
                            pass
                        if "Edit" in classname:
                            self.input(item2, "C:\diagram.png")

                        if "Button" in classname and "打开" in _title:
                            print 'Got Button'
                            time.sleep(10)
                            print _title, classname
                            self.click(item2)
                            break
                    break

    def test3(self):
        self.uploadFileFromDlg(filePath="C:\diagram.png")

    def uploadFileFromDlg(self, filePath=None, dlgClassname ="#32770", dlgTitle ="打开", buttonTitle="打开",
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
                    logger.debug('*********************** Get Dialog ********************%s %s '
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
                            logger.debug('******************* Get Button ****************** %s %s'
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
        '''
        click button specified by hwnd
        parameter: hwnd, handle of ctrl
        '''
        ret = win32gui.SendMessage(hwnd, win32con.WM_SETFOCUS)
        ret = win32gui.SendMessage(hwnd, win32con.BM_CLICK)
        return ret

if __name__ == "__main__":
    unittest.main()
