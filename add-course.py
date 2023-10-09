from tkinter import *
from tkinter import ttk
from tkinter import messagebox as msg
import pyodbc

loginForm = Tk()
loginForm.title('Login Form')
loginForm.geometry('750x550')
right = int(loginForm.winfo_screenwidth() / 2 - 900 / 2)
down = int(loginForm.winfo_screenheight() / 2 - 500 / 2)
loginForm.geometry('+{}+{}'.format(right, down))
loginForm.resizable(0, 0)
loginForm.iconbitmap('images/login.ico')


def checkvalidation(*args):
    if len(txtcoursename.get()) > 20:
        txtcoursename.set(txtcoursename.get()[:20])


def loginFunctionSqlServer():
    connectionString = 'Driver={SQL SERVER};server=localhost;database=AddCourse;Trusted_Connection=yes;'
    commandtext = 'EXEC [dbo].[RegisterCourse] ?,?,?'
    params = (txtcoursecode.get(), txtcoursename.get(), txtduration.get())
    with pyodbc.connect(connectionString) as connection:
        cursor = connection.cursor()
        cursor.execute(commandtext, params)
        connection.commit()
    msg.showinfo('Register', 'Course Register')
    resetForm()
    tree.insert("", "end", values=(txtcoursecode.get(), txtcoursename.get(), txtduration.get()))

def populate_table_from_database():
    connectionString = 'Driver={SQL SERVER};server=localhost;database=AddCourse;Trusted_Connection=yes;'
    query = 'SELECT CourseCode, CourseName, Duration FROM dbo.Course_Backup'

    with pyodbc.connect(connectionString) as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        for row in cursor.fetchall():
            formatted_row = tuple(str(value) for value in row)
            tree.insert("", "end", values=formatted_row)


selected_item = None

def on_tree_select(event):
    global selected_item
    selected_items = tree.selection()
    if selected_items:
        item = selected_items[0]
        selected_item = tree.item(item, 'values')
        txtcoursecode.set(selected_item[0])
        txtcoursename.set(selected_item[1])
        txtduration.set(selected_item[2])
    else:
        selected_item = None



def editFunctionSqlServer():
    global selected_item
    if selected_item is None:
        msg.showwarning('Edit Course', 'Please select a course to edit.')
        return

    connectionString = 'Driver={SQL SERVER};server=localhost;database=AddCourse;Trusted_Connection=yes;'
    commandtext = 'EXEC [dbo].[EditCourse] ?,?,?'
    params = (txtcoursecode.get(), txtcoursename.get(), txtduration.get())

    with pyodbc.connect(connectionString) as connection:
        cursor = connection.cursor()
        cursor.execute(commandtext, params)
        connection.commit()

    msg.showinfo('Edit Course', 'Course edited')

    # Update the selected item in the tree with the new data
    updated_item = (txtcoursecode.get(), txtcoursename.get(), txtduration.get())
    tree.item(tree.selection()[0], values=updated_item)

    resetForm()

def DeleteFunctionSqlServer():
    global selected_item
    if selected_item is None:
        msg.showwarning('Delete Course', 'Please select a course to delete.')
        return

    connectionString = 'Driver={SQL SERVER};server=localhost;database=AddCourse;Trusted_Connection=yes;'
    commandtext = 'EXEC [dbo].[DeleteCourse] ?'  # The SP has one parameter, so only one "?" is needed
    params = (txtcoursecode.get(),)

    with pyodbc.connect(connectionString) as connection:
        cursor = connection.cursor()
        cursor.execute(commandtext, params)
        connection.commit()

    msg.showinfo('Delete Course', 'Course deleted')

    # Remove the selected item from the tree
    selected_item_id = tree.selection()[0]
    tree.delete(selected_item_id)

    resetForm()


def resetForm():
    for widget in loginForm.winfo_children():
        if isinstance(widget, ttk.Entry):
            widget.delete(0, END)

def set_background_color(widget, color):
    widget.configure(background=color)

set_background_color(loginForm, 'AliceBlue')
lblcoursecode = Label(loginForm, text='CourseCode:',bg="AliceBlue")
lblcoursecode.grid(row=0, column=0, padx=0, pady=10)

txtcoursecode = StringVar()
entcoursecode = Entry(loginForm, width=30, textvariable=txtcoursecode)
entcoursecode.grid(row=0, column=1, padx=0, pady=10,sticky='w')

lblcoursename = Label(loginForm, text='CourseName:',bg="AliceBlue")
lblcoursename.grid(row=1, column=0, padx=0, pady=10)

txtcoursename = StringVar()
txtcoursename.trace('w', checkvalidation)
entcoursename = Entry(loginForm, width=30, textvariable=txtcoursename)
entcoursename.grid(row=1, column=1, padx=0, pady=10,sticky='w')

lblduration = Label(loginForm, text='Duration:',bg="AliceBlue")
lblduration.grid(row=2, column=0, padx=0, pady=10)

txtduration = IntVar(value="0")
entduration = Entry(loginForm, width=30, textvariable=txtduration)
entduration.grid(row=2, column=1, padx=0, pady=10,sticky='w')

# btnlogin=ttk.Button(loginForm,text='Login',width=20,command=loginFunctionSqlite)
buttonstyle = ttk.Style()
buttonstyle.configure("RoundedButton.TButton", relief="flat", borderwidth=9, padding=5, background="lightblue")

btnlogin = ttk.Button(loginForm, text='ADD Course', width=15,style='RoundedButton.TButton',command=loginFunctionSqlServer)
btnlogin.grid(row=3, column=0, padx=10, pady=10)

btnedit = ttk.Button(loginForm, text='Edit Course', width=15,style='RoundedButton.TButton',command=editFunctionSqlServer)
btnedit.grid(row=3, column=1, padx=10, pady=10,sticky='w')

btndelete = ttk.Button(loginForm, text='Delete Course', width=15,style='RoundedButton.TButton',command=DeleteFunctionSqlServer)
btndelete.grid(row=4, column=0, padx=10, pady=10)

#view
table_frame = ttk.Frame(loginForm)
table_frame.grid(row=5, column=0, columnspan=2, padx=25, pady=10, sticky='w')
tree = ttk.Treeview(table_frame, columns=("Course Code", "Course Name", "Duration"), show="headings")
tree.heading("#1", text="Course Code")
tree.heading("#2", text="Course Name")
tree.heading("#3", text="Duration")
tree.pack(fill='both', expand=True)
tree.bind('<<TreeviewSelect>>', on_tree_select)

populate_table_from_database()

loginForm.mainloop()
