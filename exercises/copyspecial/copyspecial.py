#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import os
import shutil
import commands

"""Copy Special exercise
"""

# +++your code here+++
# Write functions and modify main() to call them
def getSpecialPaths(dir):
  list = []
  filenames = os.listdir(dir)
  for filename in filenames:
    match = re.search(r'__\w+__', filename)
    if match:
      list.append(os.path.abspath(os.path.join(dir, filename)))
  return list

def copyTo(absFilePaths, desDir):
  if not os.path.exists(desDir):
    os.mkdir(desDir)
  for absFilePath in absFilePaths:
    shutil.copy(absFilePath, os.path.join(desDir, os.path.basename(absFilePath)))

def zipFile(absFilePaths, zipFilename):
  cmd = 'zip -j '+zipFilename+' '+' '.join(absFilePaths)
  print 'Ready to excute cmd: ', cmd
  (status, output) = commands.getstatusoutput(cmd)
  if status!=0:
    sys.stderr.write(output)
    sys.exit(1)
  print output


def main():
  # This basic command line argument parsing code is provided.
  # Add code to call your functions below.

  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]
  if not args:
    print "usage: [--todir dir][--tozip zipfile] dir [dir ...]";
    sys.exit(1)

  # todir and tozip are either set from command line
  # or left as the empty string.
  # The args array is left just containing the dirs.
  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  tozip = ''
  if args[0] == '--tozip':
    tozip = args[1]
    del args[0:2]

  if len(args) == 0:
    print "error: must specify one or more dirs"
    sys.exit(1)

  # +++your code here+++
  # Call your functions
  specialFilePaths = []
  for arg in args:
    specialFilePaths.extend(getSpecialPaths(arg))
  if todir != '':
    copyTo(specialFilePaths, todir)
  elif tozip != '':
    zipFile(specialFilePaths, tozip)
  else:
    print specialFilePaths
  
if __name__ == "__main__":
  main()
