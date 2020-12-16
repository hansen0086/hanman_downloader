import os
import img2pdf
import glob

import re


from PIL import Image


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [atoi(c) for c in re.split(r'(\d+)', text)]


def remove_transparency():
    # Absolute path to this script
    scriptdir = os.path.dirname(os.path.abspath(__file__))

    # Walk through directory
    for root, subfolders, files in os.walk(scriptdir):
        for file in files:
            try:
                image = Image.open(os.path.join(scriptdir, root, file))
                # If image has an alpha channel
                if image.mode == 'RGBA':
                    # Create a blank background image
                    bg = Image.new('RGB', image.size, (255, 255, 255))
                    # Paste image to background image
                    bg.paste(image, (0, 0), image)
                    # Save pasted image as image
                    bg.save(os.path.join(scriptdir, root, file), "PNG")

            except:
                pass


remove_transparency()
imagelist = glob.glob("*.jpg")

#folderlist = glob.glob('室友*')
folderlist = os.listdir(os.getcwd())
folderlist.sort(key=natural_keys)
# print(folderlist)
temp = []

with open(os.path.basename(os.getcwd())+".pdf", "wb") as f:
    for folder in folderlist:
        currjpgs = glob.glob(folder+"/"+"*.jpg")
        for i in currjpgs:
            imagelist.append(i)
    # imagelist = imagelist[]
    # print(imagelist[-1])

    f.write(img2pdf.convert([i for i in imagelist if i.endswith(".jpg")]))
