import sys

from pdf2image import convert_from_path
import os

outputDir = "Slides/"

def convert(file, outputDir):
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)

    pages = convert_from_path(file, 500)
    count = 1
    for page in pages:
        myFile = outputDir + 'out_img' + str(count) + '.jpg'
        count += 1
        page.save(myFile, "JPEG")

fileList = os.listdir("Presentation\\")
if fileList is None:
    print("There is no presentation")
    exit(1)

if len(fileList)==1 and (fileList[0].find(".pdf")!=-1 or fileList[0].find(".PDF")!=-1):
    file = fileList[0]

    print("PDF2JPEG conversion...")
    convert("Presentation\\" + file, outputDir)
    print("PDF2JPEG converted!")


