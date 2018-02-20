#!python3
#encoding=utf-8
from __future__ import print_function, division, absolute_import
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains
from WebPoem import WebPoem

class Elements:
    last = None
    
    def __init__(self, els):
        # els sempre vai ser uma lista, mesmo que seja de apenas 1 elemento
        self.els = els if type(els) is list else [els]
    
    def fill(self, *vals):
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

        for i, val in enumerate(vals):
            # caso o parametro seja um número
            # ou outro tipo de objeto
            val = str(val)
            e = res[i]
            e.click()
            # seleciona tudo oq tá dentro
            # do input
            e.send_keys(Keys.CONTROL, 'a')
            # insere o valor
            e.send_keys(val)
            # ativa os callbacks
            # de onkeyup
            e.send_keys(Keys.TAB)

            Elements.last = e

        return Elements(res)

    def select(self, *vals):
        for e in self.els:
            if e.tag_name == 'select':
                # caso o parametro seja um número
                # ou outro tipo de objeto
                select = Select(e)
                Elements.last = e
                # seleciona o primeiro
                val = str(vals[0])
                select.select_by_visible_text(val)
                
                if len(vals) == 1:
                    return Elements(e)

                # tem mais de um vals
                # seleciona os demais com control
                act = ActionChains(WebPoem.driver)
                act.key_down(Keys.CONTROL, e)
                for i, val in enumerate(vals[1:]):
                    val = str(val)
                    act.click(select.select_by_visible_text(val))

                return Elements(e)

    def click(self):
        if len(self.els) == 0:
            return False
        self.els[0].click()
        return self


    def isClickable(self):
        if len(self.els) == 0:
            return False

        if self.els[0].value_of_css_property('cursor') == 'pointer':
            return True

        return False

    def send_keys(self, *args, **kwargs):
        for e in self.els:
            e.send_keys(*args, **kwargs)

    def __len__(self):
        return len(self.els)

    def __getitem__(self, key):
        return self.els[key]

    def __str__(self):
        return str(self.els)

    def text(self):
        return [x.text for x in self.els]
