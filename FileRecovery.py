#Author         TheStair
#Assignment     Project3
#Class          Comp5350

#Personal Statement
#I Certify that this code is solely my own, and/or when I utilize external sources it is clearly cited.


#Project Goal
#Extract files from a supplied disk image using file signatures.

import os
import sys
import shutil
import hashlib

#Define File Signature variables
#Sourced from www.garykessler.net/library/file_sigs.html

#I originally planned to utilize defined variables, but after consideration, a dictionary is a better
# way to structure the file signatures

# I used ChatGPT to figure out how to define byte literals in python. (the \x)

#Dictionary Structure, 'fileType': (file start signature, EOF marker)
fileSignatures = {
    'pdf': (b'\x25\x50\x44\x46',b'\x25\x25\x45\x4f\x46'),
    'gif87': (b'\x47\x49\x46\x38\x37\x61', b'\x47\x49\x46\x38\x39\x61'),
    'gif89': (b'\x47\x49\x46\x38\x39\x61', b'\x47\x49\x46\x38\x39\x61'),
    'jpg': (b'\xff\xd8', b'\xff\xd9'),
    'png': (b'\x80\x50\x4e\x47\x0d\x0a\x1a\x0a', b'\x49\x45\x4e\x44\xae\x42\x60\x82'),
    'avi': (b'\x52\x49\x46\x46', b'\x00\x00') #Placeholder, AVI file size is 4 bytes LE after sig
}




def findSignature(data, signature):
    return data.find(signature)

def carve_file(diskImage, outputFile):

    with open(diskImage, 'rb') as f:
        data = f.read()

    carvedFileInfo = []

    i = 0
    while i != -1:
        i = findSignature(data, i)
    with open(outputFile, 'wb') as fileOut:
        fileOut.write(carvedData)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please enter a disk image to analyze.")
        sys.exit(1)

