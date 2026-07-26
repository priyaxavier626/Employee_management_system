import sqlite3

while True:
    print("\n===== Employee Management System =====")
    print("1. Add Employee")
    print("2. View Employees")
    print("3. Search Employee")
    print("4. Update Employee Salary")
    print("5. Delete Employee")
    print("6. Exit")

    choice = input("Enter your choice: ")

    conn = sqlite3.connect("employee.db")
    cursor = conn.cursor()

    if choice == "1":
        name = input("Enter employee name: ")
        age = int(input("Enter employee age: "))
        department = input("Enter department: ")
        salary = float(input("Enter salary: "))

        cursor.execute(
            "INSERT INTO employees (name, age, department, salary) VALUES (?, ?, ?, ?)",
            (name, age, department, salary)
        )

        conn.commit()
        print("Employee added successfully!")

    elif choice == "2":
        cursor.execute("SELECT * FROM employees")
        employees = cursor.fetchall()

        if employees:
            print("\n===== Employee Records =====")
            for employee in employees:
                print(f"ID: {employee[0]}")
                print(f"Name: {employee[1]}")
                print(f"Age: {employee[2]}")
                print(f"Department: {employee[3]}")
                print(f"Salary: {employee[4]}")
                print("-" * 30)
        else:
            print("No employee records found!")

    elif choice == "3":
        name = input("Enter employee name to search: ")

        cursor.execute(
            "SELECT * FROM employees WHERE name = ?",
            (name,)
        )

        employees = cursor.fetchall()

        if employees:
            print("\n===== Employee Found =====")
            for employee in employees:
                print(f"ID: {employee[0]}")
                print(f"Name: {employee[1]}")
                print(f"Age: {employee[2]}")
                print(f"Department: {employee[3]}")
                print(f"Salary: {employee[4]}")
                print("-" * 30)
        else:
            print("Employee not found!")

    elif choice == "4":
        emp_id = int(input("Enter Employee ID: "))
        new_salary = float(input("Enter New Salary: "))

        cursor.execute(
            "UPDATE employees SET salary = ? WHERE id = ?",
            (new_salary, emp_id)
        )

        conn.commit()

        if cursor.rowcount > 0:
            print("Salary updated successfully!")
        else:
            print("Employee ID not found!")

    elif choice == "5":
        emp_id = int(input("Enter Employee ID to delete: "))

        cursor.execute(
            "DELETE FROM employees WHERE id = ?",
            (emp_id,)
        )

        conn.commit()

        if cursor.rowcount > 0:
            print("Employee deleted successfully!")
        else:
            print("Employee ID not found!")

    elif choice == "6":
        conn.close()
        print("Thank you!")
        break

    else:
        print("Invalid choice!")

    conn.close()