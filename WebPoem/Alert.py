#!python3
#encoding=utf-8
from __future__ import print_function, division
from selenium.webdriver.common.keys import Keys

class Alert:
    def __init__(self, alert):
        self.alert = alert

    def click(self):
        self.alert.accept()

    def send_keys(self, val):
        self.alert.send_keys(val)
