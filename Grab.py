__author__ = 'mingw'

import urllib2

def garb():
    content = urllib2.urlopen('http://sh.58.com/banjia/20016251012738x.shtml').read()

    print content.decode('utf-8')

if __name__ == '__main__':
    garb()
    pass




