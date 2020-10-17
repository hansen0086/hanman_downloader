import os
import img2pdf
import glob

import re


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [atoi(c) for c in re.split(r'(\d+)', text)]


imagelist = glob.glob("*.jpg")

#folderlist = glob.glob('室友*')
folderlist = os.listdir(os.getcwd())
folderlist.sort(key=natural_keys)
# print(folderlist)
temp = []

with open("output.pdf", "wb") as f:
    for folder in folderlist:
        currjpgs = glob.glob(folder+"/"+"*.jpg")
        for i in currjpgs:
            imagelist.append(i)
    # imagelist = imagelist[]
    # print(imagelist[-1])

    f.write(img2pdf.convert([i for i in imagelist if i.endswith(".jpg")]))
