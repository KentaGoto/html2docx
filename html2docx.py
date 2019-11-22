# coding: utf-8

import os
import shutil
import win32com
from win32com.client import *


def all_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            yield os.path.join(root, file)


def html2docx(html_fullpath, word):
    html_fullpath = html_fullpath.replace("/", "\\")
    print(html_fullpath)

    dirname = os.path.dirname(html_fullpath)
    current_file = os.path.basename(html_fullpath)
    fname, ext = os.path.splitext(current_file)
    doc = word.Documents.Open(html_fullpath)  # Open the htm(l) in Word
    # Save as DOCX file
    doc.SaveAs(dirname + '/' + fname + '.docx', FileFormat=16)
    doc.Close()


if __name__ == '__main__':
    s = input("Dir: ")
    root_dir = s.strip('\"')
    root_dir_copy = root_dir + '__copy'
    shutil.copytree(root_dir, root_dir_copy)

    # com object
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0

    print('Processing...')

    for i in all_files(root_dir_copy):
        dirname = os.path.dirname(i)
        current_file = os.path.basename(i)
        fname, ext = os.path.splitext(current_file)

        if ext == '.htm' or ext == '.html':
            try:
                # Convert htm(l) to Doc(x)
                html2docx(dirname + '/' + current_file, word)
            except:
                print('Error: ' + i)

            # Delete htm(l) files
            os.remove(dirname + '/' + current_file)
        else:
            # Delete non-Doc(x) files
            os.remove(i)

    word.Quit()

    print('')
    print('Done!')
    print('Enter to exit.')
    os.system("pause > nul")
