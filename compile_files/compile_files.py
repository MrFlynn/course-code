#!/usr/bin/env python3

"""
Imports:
"""
import shutil
import glob
import os

"""
Global vars:
"""
extension = '.asm'  # Modify this.
directive = './**/*{0}'

files_dirs = glob.glob(directive.format(extension, ), recursive=True)

"""
Functions:
"""

# createDirName : str -> str
# Gets the directory name for a passed in filename.
def createDirName(filename: str) -> str:
    return (filename.split('/')[-1]).split("_")[0]

# copyFile : str ->
# Copies the given file to a new directory.
def copyFile(file: str):
    dirname = createDirName(file)

    if not os.path.exists(dirname):
        os.makedirs(dirname)

    currdir = '{0}/{1}'.format(os.getcwd(), file[1:], )
    movedir = '{0}/{1}'.format(os.getcwd(), dirname, )
    shutil.copy2(currdir, movedir)

# main:
def main():
    for file in files_dirs:
        copyFile(file)

# Runner:
if __name__ == '__main__':
    main()
