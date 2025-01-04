from tkinter import *
from tkinter import ttk, messagebox
from tkinter import filedialog as fd
from db import DataBaseManager

def input_fields_empty(parameters):
    return parameters[0] == '' or parameters[1] == '' or parameters[2] == '' or parameters[3] == ''

def select_record_to_edit(event):
    selected_item = tree.selection()
    if selected_item:
        # Fetch the data associated with the selected item
        record = tree.item(selected_item[0], 'values')

        # Populate the input fields with the selected record's data
        name_entry.delete(0, END)
        name_entry.insert(0, record[1])  # Assuming the name is the second column
        address_entry.delete(0, END)
        address_entry.insert(0, record[2])  # Assuming address is the third column
        age_entry.delete(0, END)
        age_entry.insert(0, record[3])  # Assuming age is the fourth column
        student_number_entry.delete(0, END)
        student_number_entry.insert(0, record[4])

def refresh_treeview():
    records = DataBaseManager.fetch_all_students()

    for item in tree.get_children():
        tree.delete(item)

    for record in records:
        tree.insert('', 'end', values=(record.id, record.name, record.address, record.age, record.student_number))

    tree.bind('<<TreeviewSelect>>', select_record_to_edit)

def open_file():

        file_name = fd.askopenfilename()

        if not is_json(file_name):
            messagebox.showerror('Error', 'File is not JSON.')
            return

        DataBaseManager.add_students_from_file(file_name)
        messagebox.showinfo('Success', 'Multiple students added successfully.')
        refresh_treeview()


def insert_data():
    parameters = (name_entry.get(), address_entry.get(), age_entry.get(), student_number_entry.get())

    if input_fields_empty(parameters):
        messagebox.showinfo("Warning", "Please fill all fields.")
        return
    DataBaseManager.add_student(parameters)
    messagebox.showinfo("Success", "Student data inserted successfully.")
    refresh_treeview()

def erase_input_fields():
    name_entry.delete(0, END)
    address_entry.delete(0, END)
    age_entry.delete(0, END)
    student_number_entry.delete(0, END)

def delete_data():
    try:
        selected_item = tree.selection()[0]
        student_id = tree.item(selected_item)['values'][0]
        DataBaseManager.delete_student(student_id)
        messagebox.showinfo("Success", "Student data deleted successfully.")
        erase_input_fields()
        refresh_treeview()
    except Exception as e:
        messagebox.showinfo("Error", "No record selected.")


def is_json(file):
    return file.endswith('.json')

def update_data():
    try:
        selected_item = tree.selection()[0]
        student_id = tree.item(selected_item)['values'][0]

        data = {
            "name": name_entry.get(),
            "address": address_entry.get(),
            "age": age_entry.get(),
            "student_number": student_number_entry.get()
        }

        DataBaseManager.update_student(student_id, data)
        messagebox.showinfo("Success", "Student data updated successfully.")
        refresh_treeview()
    except Exception as e:
        messagebox.showinfo("Error", "No record selected.")
root = Tk()
root.configure(background="grey")
root.title = "Student management system"
frame = LabelFrame(root, text="Student Data", bg="grey")
frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

Label(frame, text="Name:" , bg="grey").grid(row=0, column=0, padx=2, pady=2, sticky="w")
name_entry = Entry(frame)
name_entry.grid(row=0, column=1, pady=2, sticky="ew")

Label(frame, text="Address:", bg="grey").grid(row=1, column=0, padx=2, pady=2, sticky="w")
address_entry = Entry(frame)
address_entry.grid(row=1, column=1, pady=2, sticky="ew")

Label(frame, text="Age:", bg="grey").grid(row=2, column=0, padx=2, pady=2, sticky="w")
age_entry = Entry(frame)
age_entry.grid(row=2, column=1, pady=2, sticky="ew")

Label(frame, text="Student number:", bg="grey").grid(row=3, column=0, padx=2, pady=2, sticky="w")
student_number_entry = Entry(frame)
student_number_entry.grid(row=3, column=1, pady=2, sticky="ew")


button_frame = Frame(root, bg="grey")
button_frame.grid(row=1, column=0, pady=5, sticky="ew")

Button(button_frame, text="Create Table").grid(row=0, column=0, padx=5)
Button(button_frame, text="Add Data", command=insert_data).grid(row=0, column=1, padx=5)
Button(button_frame, text="Update Data", command=update_data).grid(row=0, column=2, padx=5)
Button(button_frame, text="Delete Data", command=delete_data).grid(row=0, column=3, padx=5)
Button(button_frame, text="Add from file", command=open_file).grid(row=0, column=4, padx=5)

tree_frame = Frame(root, bg="grey")
tree_frame.grid(row=2, column=0, padx=10, sticky="nsew")

tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)
tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="browse")
tree.pack()
tree_scroll.config(command=tree.yview)

tree["columns"] = ("student_id", "name", "address", "age", "student number")
tree.column("#0", width=0, stretch=NO)
tree.column("student_id", anchor=CENTER, width=80)
tree.column("name", anchor=CENTER, width=120)
tree.column("address", anchor=CENTER, width=120)
tree.column("age", anchor=CENTER, width=50)
tree.column("student number", anchor=CENTER, width=120)

tree.heading("student_id", text="ID", anchor=CENTER)
tree.heading("name", text="Name", anchor=CENTER)
tree.heading("address", text="Address", anchor=CENTER)
tree.heading("age", text="Age", anchor=CENTER)
tree.heading("student number", text="Student Number", anchor=CENTER)

refresh_treeview()
root.mainloop()