import cv2
import os
from PIL import Image
import ctypes
import presentationController


tempDir = "temp/"
savedSlidesDir = "SavedSlides/"
filepath = None
tempSavedDir = "tempSaved/"
cColor = (0, 0, 255)

def addNote():
    arrayNote = presentationController.dictOfAnnotations
    print(arrayNote)
    count = 0
    for image in os.listdir(tempDir):
        count += 1
    aux = 1
    while aux <= count:
        print("salvataggio nuova foto")
        imgCurrent = cv2.imread(tempDir + 'out_img' + str(aux) + '.jpg')
        if aux-1 in arrayNote:
            note = arrayNote[aux - 1]
            print(note)
            for i in range(len(note)):
                for j in range(len(note[i])):
                    if j != 0:
                        imgCurrent = cv2.line(imgCurrent, note[i][j - 1], note[i][j], cColor, 5)
        cv2.imwrite(tempSavedDir + 'out_img' + str(aux) + '.jpg', imgCurrent)
        aux += 1
    jpg2pdf()



#funzione per convertire i jpg modificati in pdf e salvarli nell'apposita cartella
def jpg2pdf():
    image_list = []
    count = 0
    for image in os.listdir(tempSavedDir):
        count += 1

    if count != 0:
        image = Image.open(tempSavedDir + 'out_img1.jpg')
        image = image.convert('RGB')
    aux = 2
    while aux <= count:
        imageAux = Image.open(tempSavedDir + 'out_img' + str(aux) + '.jpg')
        imageAux = imageAux.convert('RGB')
        image_list.append(imageAux)
        aux += 1

    count = 0
    for pdf in os.listdir(savedSlidesDir):
        count += 1

    image.save(savedSlidesDir + 'savedSlides' + str(count) + '.pdf', save_all =True, append_images=image_list)


#funzione invocata se si decide di salvare
def savedSlide():
    #jpg2pdf()
    addNote()
    for file_name in os.listdir(tempDir):
        file = tempDir + file_name
        #eliminiamo le immagini temporanee
        if os.path.isfile(file):
            print('Eliminazione file:', file)
            os.remove(file)
    for file_name in os.listdir(tempSavedDir):
        file = tempSavedDir + file_name
        #eliminiamo le immagini temporanee
        if os.path.isfile(file):
            print('Eliminazione immagini modificate:', file)
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