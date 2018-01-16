#!python3
#encoding=utf-8
from __future__ import print_function, division
from selenium.webdriver.common.keys import Keys


class Elements:
    last = None
    
    def __init__(self, els):
        # els sempre vai ser uma lista, mesmo que seja de apenas 1 elemento
        self.els = els if type(els) is list else [els]
    
    def fill(self, val):
        res = []
        for e in self.els:
            if e.tag_name == 'input':
                t = e.get_attribute('type')
                if t is None:
                    t = "text"

                if t == 'hidden':
                    continue

                if t in ['text', 'password']:
                    res.append(e)

        for e in res:
            e.click()
            e.send_keys(val)
            e.send_keys(Keys.TAB)

            Elements.last = e

        return Elements(res)

    def click(self):
        if len(self.els) == 0:
            return False
        self.els.click()
        return True


    def isClickable(self):
        if len(self.els) == 0:
            return False

        if self.els[0].value_of_css_property('cursor') == 'pointer':
            return True

        return False

    def __len__(self):
        return len(self.els)

    def __getitem__(self, key):
        return self.els[key]

    def text(self):
        return [x.text for x in self.els]
