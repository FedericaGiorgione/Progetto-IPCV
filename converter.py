poppler_path = r"C:\ProgramData\poppler-22.04.0\Library\bin"
from pdf2image import convert_from_path
from tkinter import *
from tkinter import messagebox
from tkinter import  filedialog

root = Tk()
root.title("PDF to JPEG")
root.geometry('420x170')
root.config(bg='#FCF3CF')


outputDir = "Slides/"

def pdf2jpg():
    try:
        """images = convert_from_path(pdf_path=str(enter_path.get()), dpi=200, poppler_path=poppler_path)
        for i in images:
            i.save('output.jpg', 'JPEG')"""
        pages = convert_from_path(pdf_path=str(enter_path.get()), dpi=200, poppler_path=poppler_path, size=(1280, 720))
        count = 1
        for page in pages:
            myFile = outputDir + 'out_img' + str(count) + '.jpg'
            count += 1
            page.save(myFile, "JPEG")
    except:
        Result = "Enter pdf file path"
        messagebox.showinfo("Result", Result)
    else:
        Result = "Successful"
        messagebox.showinfo("Result", Result)



def openFile():
    filepath = filedialog.askopenfilename()
    print(filepath)
    enter_path.insert(0, filepath)




Label(root, text="Convert PDF to JPEG", font=("Helvetica 15 bold"), fg="black", bg='#FCF3CF').pack(pady=10)
Label(root, text="File Location:", font=("Helvetica 10"), bg='#FCF3CF').place(x=20, y=55)

enter_path = Entry(root, width=18, font=("poppins 15"), bg="white", border=3)
enter_path.focus()
enter_path.place(x=110, y=50)

btn = Button(root, text="Convert", relief=RAISED, borderwidth=2, font=('popins', 10, 'bold'), bg='#FCF3CF', fg="black", cursor="hand2", command=pdf2jpg)
btn.place(x=150, y=100)
button = Button(root, text="Open", relief=RAISED, borderwidth=2, font=('popins', 10, 'bold'), bg='#FCF3CF', fg="black", cursor="hand2", command=openFile)
button.place(x = 320, y = 50)




root.mainloop()