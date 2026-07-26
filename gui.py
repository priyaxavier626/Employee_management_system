import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# ---------------- DATABASE ----------------

def get_connection():
    return sqlite3.connect("employee.db")


# ---------------- ADD EMPLOYEE ----------------

def add_employee():
    name = name_entry.get()
    age = age_entry.get()
    department = department_entry.get()
    salary = salary_entry.get()

    if not name or not age or not department or not salary:
        messagebox.showerror("Error", "Please fill all fields")
        return

    if not age.isdigit():
        messagebox.showerror("Error", "Age must be a number")
        return

    try:
        float(salary)
    except ValueError:
        messagebox.showerror("Error", "Salary must be a number")
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO employees(name, age, department, salary)
        VALUES (?, ?, ?, ?)
        """,
        (name, int(age), department, float(salary))
    )

    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Employee Added Successfully!")

    clear_fields()
    view_employees()
# ---------------- VIEW EMPLOYEES ----------------

def view_employees():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM employees")
    rows = cursor.fetchall()

    employee_table.delete(*employee_table.get_children())

    for row in rows:
        employee_table.insert("", tk.END, values=row)

    conn.close()


# ---------------- SEARCH EMPLOYEE ----------------

def search_employee():
    name = name_entry.get()

    if not name:
        messagebox.showerror("Error", "Enter employee name")
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM employees WHERE name LIKE ?",
        ("%" + name + "%",)
    )

    rows = cursor.fetchall()

    employee_table.delete(*employee_table.get_children())

    if rows:
        for row in rows:
            employee_table.insert("", tk.END, values=row)
    else:
        messagebox.showinfo("Search", "Employee not found")

    conn.close()

#---------------- UPDATE EMPLOYEE ----------------

def update_employee():
    emp_id = id_entry.get()
    salary = salary_entry.get()

    if not emp_id or not salary:
        messagebox.showerror("Error", "Enter Employee ID and Salary")
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE employees SET salary=? WHERE id=?",
        (float(salary), int(emp_id))
    )

    conn.commit()

    if cursor.rowcount > 0:
        messagebox.showinfo("Success", "Employee Updated Successfully!")
    else:
        messagebox.showerror("Error", "Employee ID Not Found")

    conn.close()

    clear_fields()
    view_employees()


# ---------------- DELETE EMPLOYEE ----------------

def delete_employee():
    emp_id = id_entry.get()

    if not emp_id:
        messagebox.showerror("Error", "Enter Employee ID")
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM employees WHERE id=?",
        (int(emp_id),)
    )

    conn.commit()

    if cursor.rowcount > 0:
        messagebox.showinfo("Success", "Employee Deleted Successfully!")
    else:
        messagebox.showerror("Error", "Employee ID Not Found")

    conn.close()

    clear_fields()
    view_employees()


# ---------------- CLEAR FIELDS ----------------

def clear_fields():
    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    department_entry.delete(0, tk.END)
    salary_entry.delete(0, tk.END)
    
#---------------- GUI ----------------

window = tk.Tk()
window.title("Employee Management System")
window.geometry("900x700")

title = tk.Label(
    window,
    text="Employee Management System",
    font=("Arial", 20, "bold")
)
title.pack(pady=10)

tk.Label(window, text="Employee ID").pack()
id_entry = tk.Entry(window, width=40)
id_entry.pack()

tk.Label(window, text="Name").pack()
name_entry = tk.Entry(window, width=40)
name_entry.pack()

tk.Label(window, text="Age").pack()
age_entry = tk.Entry(window, width=40)
age_entry.pack()

tk.Label(window, text="Department").pack()
department_entry = tk.Entry(window, width=40)
department_entry.pack()

tk.Label(window, text="Salary").pack()
salary_entry = tk.Entry(window, width=40)
salary_entry.pack(pady=5)

tk.Button(
    window,
    font="Arial,12",
    text="Add Employee",
    bg="green",
    fg="white",
    command=add_employee,
    width=25
).pack(pady=5)

tk.Button(
    window,
    font="Arial,12",
    text="View Employees",
    bg="green",
    fg="white",
    command=view_employees,
    width=25
).pack(pady=5)

tk.Button(
    window,
    font="Arial,12",
    text="Search Employee",
    bg="green",
    fg="white",
    command=search_employee,
    width=25
).pack(pady=5)

tk.Button(
    window,
    font="Arial,12",
    text="Update Employee",
    bg="green",
    fg="white",
    command=update_employee,
    width=25
).pack(pady=5)

tk.Button(
    window,
    font="Arial,12",
    text="Delete Employee",
    bg="green",
    fg="white",
    command=delete_employee,
    width=25
).pack(pady=5)

tk.Button(
    window,
    font="Arial,12",
    text="Clear",
     bg="green",
    fg="white",
    command=clear_fields,
    width=25
).pack(pady=5)

employee_table = ttk.Treeview(
    window,
    columns=("ID", "Name", "Age", "Department", "Salary"),
    show="headings",
    height=10
)

employee_table.heading("ID", text="ID")
employee_table.heading("Name", text="Name")
employee_table.heading("Age", text="Age")
employee_table.heading("Department", text="Department")
employee_table.heading("Salary", text="Salary")

employee_table.column("ID", width=60)
employee_table.column("Name", width=150)
employee_table.column("Age", width=70)
employee_table.column("Department", width=150)
employee_table.column("Salary", width=120)

employee_table.pack(pady=20)

tk.Button(
    window,
    text="Exit",
    bg="green",
    fg="white",
    command=window.destroy,
    width=20
).pack(pady=10)

view_employees()

window.mainloop()    