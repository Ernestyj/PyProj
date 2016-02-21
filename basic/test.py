import sys, re, urllib

__author__ = 'Eugene'


def wget2(url):
  try:
    ufile = urllib.urlopen(url)
    if ufile.info().gettype() == 'text/html':
      print ufile.read()
  except IOError:
    print 'problem reading url:', url

if __name__ == "__main__":

    pass
