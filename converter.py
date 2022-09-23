poppler_path = r"poppler-22.04.0\Library\bin"
from pdf2image import convert_from_path
from tkinter import *
from tkinter import messagebox
from tkinter import  filedialog
import os
import shutil
from PIL import Image
import zoom_2


root = Tk()
root.title("Support++")
root.geometry('420x170')
root.config(bg='#FCF3CF')


tempDir = "temp/"
savedSlidesDir = "SavedSlides/"
filepath = None

#funzione per convertire il pdf in immagine
def pdf2jpg():
    try:
        pages = convert_from_path(pdf_path=str(enter_path.get()), dpi=200, poppler_path=poppler_path, size=(1280, 720))
        count = 1
        for page in pages:
            myFile = tempDir + 'out_img' + str(count) + '.jpg'
            count += 1
            page.save(myFile, "JPEG")
    except:
        Result = "Enter pdf file path"
        messagebox.showinfo("Result", Result)
    else:
        Result = "pdf loaded correctly"
        if messagebox.showinfo("Result", Result):
            print("ok let's go")



#funzione che serve per cercare un file nel file system e prenderne il path
def openFile():
    filepath = filedialog.askopenfilename()
    print(filepath)
    enter_path.insert(0, filepath)


#funzione invocata se si decide di non salvare, elimina le immagini temporanee che avevamo creato
def deleteAllTmpFile():
    #path = r"E:\demos\files\reports\\"
    for file_name in os.listdir(tempDir):
        # construct full file path
        file = tempDir + file_name
        if os.path.isfile(file):
            print('Deleting file:', file)
            os.remove(file)

#funzione invocata se si decide di salvare
def savedSlide():
    jpg2pdf()
    for file_name in os.listdir(tempDir):
        # construct full file path
        file = tempDir + file_name
        #eliminiamo le immagini temporanee
        if os.path.isfile(file):
            print('Deleting file:', file)
            os.remove(file)


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



#funzione di conferma chiusura con possibilià di salvare/non salvare il lavoro
def on_closing():
    res = messagebox.askyesnocancel("Close", "Do you want to save the presentation??")
    #voglismo chiudere l'applicazione conservando le modifiche
    if res == True:
        savedSlide()
        root.destroy()
    #vogliamo chiudere l'applicazione senza conservare le modifiche
    elif res == False:
        #elimino l'intera cartella temporanea
        deleteAllTmpFile()
        root.destroy()



#settaggio grafica pagina di caricamento pdf
Label(root, text="Load your PDF", font=("Helvetica 15 bold"), fg="black", bg='#FCF3CF').pack(pady=10)
Label(root, text="File Location:", font=("Helvetica 10"), bg='#FCF3CF').place(x=20, y=55)

enter_path = Entry(root, width=18, font=("poppins 15"), bg="white", border=3)
enter_path.focus()
enter_path.place(x=110, y=50)

btn = Button(root, text="Open", relief=RAISED, borderwidth=2, font=('popins', 10, 'bold'), bg='#FCF3CF', fg="black", cursor="hand2", command=pdf2jpg)
btn.place(x=150, y=100)
button = Button(root, text="Find", relief=RAISED, borderwidth=2, font=('popins', 10, 'bold'), bg='#FCF3CF', fg="black", cursor="hand2", command=openFile)
button.place(x = 320, y = 50)

#protocollo che serve per gestire il pulsante X di chiusura
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()

