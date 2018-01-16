#!python3
#encoding=utf-8
from __future__ import print_function, division
from contextlib import contextmanager

# o contextmanager serve
# para que consiga
# utilizar a função com o statement
# with:
@contextmanager
def NewWindow():
    driver = WebPoem.driver
    driver.switch_to_window(driver.window_handles[1])
    try:
        yield driver
    finally:
        driver.close()
        driver.switch_to_window(driver.window_handles[0])

from WebPoem.WebPoem import WebPoem
