from tkinter import *
from tkinter import messagebox as ns
import sqlite3

# Connect to the database
with sqlite3.connect("autoriz.db") as db:
    c = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS user (username TEXT NOT NULL PRIMARY KEY, password TEXT NOT NULL);")
    db.commit()


# Define the main class
class Main:
    def __init__(self, master):
        self.master = master
        self.username = StringVar()
        self.password = StringVar()
        self.n_username = StringVar()
        self.n_password = StringVar()

        # Create and configure the window
        self.head = Label(self.master, text='Авторизация', font=('Helvetica', 35), pady=10)
        self.head.pack()

        self.logf = Frame(self.master, padx=18, pady=10)
        self.widgets()

    def login(self):
        # Connect to the database
        with sqlite3.connect('autoriz.db') as db:
            c = db.cursor()

            # Check if the username and password match
            find_user = 'SELECT * FROM user WHERE username = ? and password = ?'
            c.execute(find_user, [(self.username.get()), (self.password.get())])
            result = c.fetchall()

            if result:
                self.logf.pack_forget()
                self.head['text'] = self.username.get() + '\nДобрый день!'
                self.head['pady'] = 150
                ns.showerror('Уведомление', 'Данный пользователь не найден!')
            else:
                ns.showinfo('Успех', 'Пользователь создан!')
                self.log()

    def new_user(self):
        # Connect to the database
        with sqlite3.connect('autoriz.db') as db:
            c = db.cursor()

            # Check if the username already exists
            find_user = 'SELECT username FROM user WHERE username = ?'
            c.execute(find_user, [(self.n_username.get())])

            if c.fetchone():
                ns.showerror('Уведомление', 'Имя пользователя занято, попробуйте другое.')
            else:
                ns.showinfo('Успех', 'Пользователь создан!')
                self.log()

                # Insert the new user into the database
                insert_query = 'INSERT INTO user(username, password) VALUES (?, ?)'
                c.execute(insert_query, [(self.n_username.get()), (self.n_password.get())])
                db.commit()

    def log(self):
        self.username.set('')
        self.password.set('')
        self.logf.pack_forget()
        self.head['text'] = 'Astoomsaus'
        self.logf.pack()

    def cr(self):
        self.n_username.set('')
        self.n_password.set('')
        self.logf.pack_forget()
        self.head['text'] = 'Astoomsaus'
        self.logf.pack()

    def widgets(self):
        Label(self.logf, text='Username:', font=('Helvetica', 20), pady=5, padx=5).grid(sticky=W)
        Entry(self.logf, textvariable=self.username, bd=5, font=('Helvetica', 15)).grid(row=0, column=1)

        Label(self.logf, text='Password:', font=('Helvetica', 20), pady=5, padx=5).grid(sticky=W)
        Entry(self.logf, textvariable=self.password, bd=5, font=('Helvetica', 15), show='*').grid(row=1, column=1)

        Button(self.logf, text='Login', bd=3, font=('Helvetica', 15), padx=5, pady=5, command=self.login).grid(row=2,
                                                                                                               column=0)
        Button(self.logf, text='Create Account', bd=3, font=('Helvetica', 15), padx=5, pady=5, command=self.cr).grid(
            row=2, column=1)

        self.logf.pack()


# Create the main window
root = Tk()
root.title("Authentication System")

# Initialize the Main class
app = Main(root)

# Run the application
root.mainloop()
