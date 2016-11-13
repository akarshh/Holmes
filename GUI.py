from tkinter import *
from tkinter import filedialog
from main import *

class GUI:
    def __init__(self, root):
        self.win = root


        self.f1 = Frame(self.win)
        self.f1.pack(side = TOP)

        self.f2 = Frame(self.win)
        self.f2.pack(side = BOTTOM)

        self.image = PhotoImage(file = "holmes.gif")
        self.logo = Label(self.f1, image = self.image)
        self.logo.grid(row = 0, column = 0, padx = 5, pady = 5, columnspan = 3)

        self.b1 = Button(self.f1, text = "Authorize new user", width = 30, command = self.newUser)
        self.b1.grid(row = 1, column = 0, padx = 5, pady =5)

        self.b2 = Button(self.f1, text = "Add face to existing person", width = 30, command = self.addFace)
        self.b2.grid(row = 1, column = 2, padx = 5, pady = 5)

    def newUser(self):

        self.l1 = Label(self.f2, text = "Add a new authorized person", width = 30)
        self.l1.grid(row = 0, column = 1)

        self.e1 = Entry(self.f2, width = 30)
        self.e1.grid(row = 1, column = 1, padx = 5, pady = 5, columnspan = 2)
        self.e1.insert(0, "No image selected")
        self.e1.config(state = "readonly")

        self.e2 = Entry(self.f2, width=30)
        self.e2.grid(row = 2, column = 1, padx = 5, pady = 5, columnspan = 2)
        self.e2.insert(0, "Select an image first")
        self.e2.config(state="readonly")

        self.bb1 = Button(self.f2, text = "Browse images", command = self.selectImage)
        self.bb1.grid(row = 1, column = 4, padx = 5, pady = 5, columnspan = 2)

        self.bb2  = Button(self.f2, text = "Authorize new person", width = 30, command = self.authorizePerson)
        self.bb2.grid(row = 3, column = 1, padx = 5, pady = 5)


    def selectImage(self):
        self.filename = filedialog.askopenfilename()
        self.e1.config(state="normal")
        self.e1.delete(0, END)
        self.e1.insert(0, self.filename)
        self.e1.config(state="readonly")
        self.e2.config(state = "normal")
        self.e2.delete(0, END)

    def selectImage2(self):
        self.filename = filedialog.askopenfilename()
        self.ee1.config(state="normal")
        self.ee1.delete(0, END)
        self.ee1.insert(0, self.filename)
        self.ee1.config(state="readonly")
        self.ee2.config(state="normal")
        self.ee2.delete(0, END)


    def addFace(self):
        self.ll1 = Label(self.f2, text="Add a face to an existing person", width=30)
        self.ll1.grid(row=0, column=1)

        self.ee1 = Entry(self.f2, width=30)
        self.ee1.grid(row=1, column=1, padx=5, pady=5, columnspan=2)
        self.ee1.insert(0, "No image selected")
        self.ee1.config(state="readonly")

        self.ee2 = Entry(self.f2, width=30)
        self.ee2.grid(row=2, column=1, padx=5, pady=5, columnspan=2)
        self.ee2.insert(0, "Select an image first")
        self.ee2.config(state="readonly")

        self.bb3 = Button(self.f2, text="Browse images", command=self.selectImage2)
        self.bb3.grid(row=1, column=4, padx=5, pady=5, columnspan=2)

        self.bb4 = Button(self.f2, text="Authorize new person", width=30, command=self.addNewFace)
        self.bb4.grid(row=3, column=1, padx=5, pady=5)


    def authorizePerson(self):
        create_person(self.e2.get(), self.e1.get())

    def addNewFace(self):
        add_face(self.ee2.get(), self.ee1.get())



root = Tk()
root.title("Add a known person")
app = GUI(root)
root.mainloop()