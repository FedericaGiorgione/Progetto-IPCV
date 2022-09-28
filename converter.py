poppler_path = r"poppler-22.04.0\Library\bin"
from pdf2image import convert_from_path
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import os
import  presentationControllerV2
from pdfrw import PdfReader
import  closureController

root = Tk()
root.title("Support++")
root.geometry('420x170')
root.config(bg='#FCF3CF')


tempDir = "temp/"
savedSlidesDir = "SavedSlides/"
filepath = None
nameOfPdf = None

#funzione per convertire il pdf in immagine
def pdf2jpg():
    pdf = PdfReader(enter_path.get())
    x0, y0, x1, y1 = pdf.pages[0].MediaBox
    x0 = float(x0)
    x1 = float(x1)
    y0 = float(y0)
    y1 = float(y1)
    width = x1 - x0
    height = y1 - y0

    width = int(width)
    height = int(height)
    print("dimensione pagina: ", width, height)
    try:
        pages = convert_from_path(pdf_path=str(enter_path.get()), dpi=200, poppler_path=poppler_path,
                                  size=(width, height))
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
        #conserviano il nome del pdf nel caso in cui volessimo salvarlo alla chiusura
        closureController.nameOfPdf = os.path.basename(enter_path.get())
        print(closureController.nameOfPdf)
        if messagebox.showinfo("Result", Result):
            #avviamo le slide
            root.destroy()
            presentationControllerV2.main()



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

def main():
    #protocollo che serve per gestire il pulsante X di chiusura
    root.protocol("WM_DELETE_WINDOW", deleteAllTmpFile)
    root.mainloop()



if __name__ == "__main__":
    main()

