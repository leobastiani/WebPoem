#!python3
#encoding=utf-8
from __future__ import print_function, division
import sys
sys.path.append(r'D:\Facul\IC\WebPoem\WebPoem')
from WebPoem import *

nums = [
    'De R$ 1000,00 POR: R$1000.00',
    '1000.00',
    '1000,00',
    '1.000,00',
    '1,000.00',
]

for n in nums:
    print("Numbers("+str(n)+"):", Numbers(n))