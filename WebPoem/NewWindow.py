#!python3
#encoding=utf-8
from __future__ import print_function, division, absolute_import
from contextlib import contextmanager

# o contextmanager serve
# para que consiga
# utilizar a função com o statement
# with:
@contextmanager
def NewWindow():
    driver = WebPoem.driver
    if len(driver.window_handles) == 1:
        # não tem outra janela, é
        # um alert, confirm ou prompt
        WebPoem.alert = Alert(driver.switch_to_alert())
        yield WebPoem.alert
    else:
        # é um window.open
        driver.switch_to_window(driver.window_handles[1])
        try:
            yield driver
        finally:
            driver.close()
            driver.switch_to_window(driver.window_handles[0])

from WebPoem.WebPoem import WebPoem
from WebPoem.Alert import Alert