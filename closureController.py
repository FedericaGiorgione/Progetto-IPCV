import cv2
import os
from PIL import Image
import ctypes

tempDir = "temp/"
savedSlidesDir = "SavedSlides/"
filepath = None

#funzione per convertire i jpg modificati in pdf e salvarli nell'apposita cartella
def jpg2pdf():
    image_list = []
    count = 0
    for image in os.listdir(tempDir):
        count += 1

    if count != 0:
        image = Image.open(tempDir + 'out_img1.jpg')
        image = image.convert('RGB')
    aux = 2
    while aux <= count:
        imageAux = Image.open(tempDir + 'out_img' + str(aux) + '.jpg')
        imageAux = imageAux.convert('RGB')
        image_list.append(imageAux)
        aux += 1

    count = 0
    for pdf in os.listdir(savedSlidesDir):
        count += 1

    image.save(savedSlidesDir + 'savedSlides' + str(count) + '.pdf', save_all =True, append_images=image_list)


#funzione invocata se si decide di salvare
def savedSlide():
    jpg2pdf()
    for file_name in os.listdir(tempDir):
        file = tempDir + file_name
        #eliminiamo le immagini temporanee
        if os.path.isfile(file):
            print('Deleting file:', file)
            os.remove(file)



#funzione invocata se si decide di non salvare, elimina le immagini temporanee che avevamo creato
def deleteAllTmpFile():
    #path = r"E:\demos\files\reports\\"
    for file_name in os.listdir(tempDir):
        # construct full file path
        file = tempDir + file_name
        if os.path.isfile(file):
            print('Deleting file:', file)
            os.remove(file)



def closingApp():
    style = 3
    res = ctypes.windll.user32.MessageBoxW(0, 'Do you want to save the presentation??', 'Close', style)
    if res == 6:
        #stiamo premendo si
        savedSlide()
    if res == 7:
        #stiamo premendo no
        deleteAllTmpFile()
    cv2.destroyAllWindows()