import os
import sys
import random

characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHUJKLMNOPQRSTUVWXYZ'
base_url1='http://stackoverflow.com/questions/5557214/crc32-checksum-in-python-with-hex-input/'
base_url2='http://stackoverflow.com/questions/444591/convert-a-string-of-bytes-into-an-int-python'

def newtempname(ln=8):
    choose = random.Random().choice
    letters = [choose(characters) for dummy in range(ln)]
    return ''.join(letters)


s = set()
with open ('./urls.txt', "w") as f:
    for i in range(1000000):
        base_url = ''
        if i < 500000:
            base_url = base_url1
        else:
            base_url = base_url2

        url = ''
        tname = newtempname()
        if tname not in s:
            s.add(tname)
            url=base_url + tname +'\n'
            f.write(url)
    
