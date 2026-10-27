
import tkinter as tk
from tkinter import messagebox
import mysql.connector
import re

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=input("MySQL password: "),
    database="python_assignment"
)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS Contact(
id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(100),
email VARCHAR(100) UNIQUE,
phone VARCHAR(20),
category VARCHAR(50),
notes TEXT)
""")
conn.commit()


def add():
    name = e1.get().strip()
    email = e2.get().strip()
    phone = e3.get().strip()

    if not name or not phone or not re.fullmatch(
        r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+", email
    ):
        messagebox.showerror("Error", "Enter valid details")
        return

    try:
        cur.execute(
            "INSERT INTO Contact(name,email,phone,category,notes) VALUES(%s,%s,%s,%s,%s)",
            (name, email, phone, category.get(), notes.get())
        )
        conn.commit()
        messagebox.showinfo("Success", "Contact added")
        show()
    except mysql.connector.Error as error:
        messagebox.showerror("Error", str(error))


def show():
    lb.delete(0, tk.END)
    cur.execute("SELECT id,name,email,phone FROM Contact ORDER BY name")
    for row in cur.fetchall():
        lb.insert(tk.END, str(row))


root = tk.Tk()
root.title("Contact Manager")

e1 = tk.Entry(root)
e2 = tk.Entry(root)
e3 = tk.Entry(root)
category = tk.StringVar(value="Personal")
notes = tk.StringVar()

for label, entry in [
    ("Name", e1), ("Email", e2), ("Phone", e3)
]:
    tk.Label(root, text=label).pack()
    entry.pack()

tk.OptionMenu(
    root, category, "Personal", "Faculty", "Friend", "Other"
).pack()

tk.Entry(root, textvariable=notes).pack()
tk.Button(root, text="Add Contact", command=add).pack()
tk.Button(root, text="Show Contacts", command=show).pack()

lb = tk.Listbox(root, width=60)
lb.pack()
show()
root.mainloop()
