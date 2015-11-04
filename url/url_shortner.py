#! /usr/bin/python3.4

import argparse
import logging
import logging.handlers
import sys
import random
import hmac
import hashlib
import base64
import binascii
import math
import pickle

instance = "0"
handler='url-shortner-['+instance+']'
formatter = ('\n'+handler+':%(asctime)s-[%(filename)s:%(lineno)s]-%(levelname)s - %(message)s')
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=formatter)
logger = logging.getLogger('mailHandler')


class dehydrate_url:
    def __init__(self, alphatype=True, input_file = None, url=None):
        self.allowed_chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHUJKLMNOPQRSTUVWXYZ'
        if not alphatype:
            self.allowed_chars += '$-_.+'
            self.allowed_chars += '!(||,'
            self.allowed_chars += '{}|\^~[]<>'
        self.base_map = list(self.allowed_chars)
        self.base = len(self.base_map)
        print(self.base_map)
        print(len(self.base_map))
        self.inputfile = None
        self.url = None
        if input_file:
            self.inputfile = input_file
        elif url and len(url):
            self.url = url
        
        _key = "url shortner test"
        #self._key = base64.urlsafe_b64encode(_key).decode()
        self._key = _key
        print (len(self._key))

    '''
    def shorten(self, url):
        url_s = ''
        m = hashlib.md5()
        m.update(url.encode())
        h = m.digest()[::3]
        h =(int.from_bytes(h, byteorder='big') )
        while h != 0:
            if self.base_map[int(h % self.base)] != '0':
                url_s += self.base_map[int(h % self.base)]
            h = h / (self.base)
        
        print (" long url {} --> [{}] ".format(url, url_s) )
     '''

    def shorten(self):
        if self.url and len(self.url):
            self.url_dehydrate(self.url)
        elif self.inputfile and len(self.inputfile):
            try:
                opfile = (self.inputfile+'_output.txt')
                wf = open(self.inputfile+'_output.txt', 'w')
                with open(self.inputfile, 'r') as rf:
                    l = rf.read().split('\n')
                    lines = [i.strip() for i in l]
                    logger.info("Type {}".format(type(lines)) )
                    logger.info("No of Urls in file {}".format(len(lines)) )
                    for i in lines:
                        urls = self.url_dehydrate(i+self._key)
                        if urls:
                            ops = i + '|' + urls
                            #logger.info(i)
                            wf.write(urls+'\n')
                logger.info("Please check o/p in file {}".format(opfile))
            except:
                logger.error("Unable to open the input file\n")
            finally:
                rf.close()
                wf.close()


    def url_dehydrate(self, url):
        if len(url) <= 0:
            return None

        url_s = ''
        crc = binascii.crc32(binascii.a2b_qp(url))
        while crc != 0:
            url_s += str(self.base_map[math.floor(crc % self.base)])
            crc = math.floor(crc/ (self.base))
        #print (url_s)
        #url_s = base64.urlsafe_b64encode(url_s.encode())
        #logger.info ("{} [{}] ".format(url, url_s.decode()) )
        #print (url_s.decode())
        return url_s


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Url Shortner .')
    group = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument('-ta','--type_alpha', help='type-aplha true / flase', required=True)
    group.add_argument('-f','--file', help='Input File containing the URLs')
    group.add_argument('-u','--url', help='Single Url input through command line arg')
    args = parser.parse_args()

    argsdict = vars(args)
    print (argsdict.keys())

    inputfile = ''
    inputurl = ''
    if 'file' in argsdict and argsdict['file'] is not None:
        logger.info("File as input")
        inputfile=argsdict['file']
        logger.info("inputfile : {}".format(inputfile))
    elif 'url' in argsdict and argsdict['url'] is not None:
        inputurl=argsdict['url']
        logger.info("Input Url  : {}".format(inputurl))
    else:
        raise ValueError("Invalid inputs\n")

    alpha_type = True
    types = argsdict.get('type_alpha')
    if types and types == 'True':
        alpha_type = True
    else:
        alpha_type = False


    if len(inputfile):
        d = dehydrate_url(alpha_type, input_file=inputfile)
    elif len(inputurl):
        d = dehydrate_url(alpha_type, url=inputurl)

    d.shorten()
    logger.info("Done")
