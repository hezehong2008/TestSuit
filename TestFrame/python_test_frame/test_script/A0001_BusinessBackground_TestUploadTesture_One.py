#!/usr/bin/env python
# -*- coding: UTF-8 -*
import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import sys
reload(sys)
sys.setdefaultencoding('gbk')


class TestScript(unittest.TestCase):
    def setUp(self):
        self.browers = webdriver.Chrome()
        self.loginUrl = ""
        self.jumpUurl = ""
        self.script_id = "A0001"

    def doLogin(self):
        pass

    def doLogout(self):
        pass

    def test_upload_testure_one(self):
        print 123
        # self.uploadFileFromDlg(filePath="C:\diagram.png")