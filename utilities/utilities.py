import os
import sys

def append_hor(file1, file2, file3, folder, convert="magick convert"):
    "Horizontally add image file2 to the right of image file1."
    
    file1 = os.path.join(folder, file1)
    file2 = os.path.join(folder, file2)
    file3 = os.path.join(folder, file3)
    os.system("{0} +append {1} {2} {3}".format(convert, file1, file2, file3))