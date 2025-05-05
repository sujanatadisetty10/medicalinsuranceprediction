import tkinter as tk
from tkinter import END, Tk, messagebox
import sqlite3
from tkinter import *


class Firstpage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        border = tk.LabelFrame(self, text='Login', bg='#F1F0E8', bd=10, font=('Arial', 20))
        border.pack(fill="both", expand="yes", padx=150, pady=150)

        L1 = tk.Label(border, text="E-mail", font=("Arial Bold", 15), bg='#F8F6F4')
        L1.place(x=50, y=20)
        T1 = tk.Entry(border, width=30, bd=5)
        T1.place(x=180, y=20)

        L2 = tk.Label(border, text="Password", font=("Arial Bold", 15), bg='#F8F6F4')
        L2.place(x=50, y=80)
        T2 = tk.Entry(border, width=30, show='*', bd=5)
        T2.place(x=180, y=80)

        def verify():
            email = T1.get()
            password = T2.get()
            if not email or not password:
                messagebox.showerror('Enter all fields')
                return
            try:
                conn = sqlite3.connect('medical_data.db')
                c = conn.cursor()
                sql_query = "SELECT email, password FROM signup WHERE email=? and password=?"
                c.execute(sql_query, (email, password))
                result = c.fetchone()
                if result:
                    messagebox.showinfo("Welcome", "Login is successful")
                    controller.show_frame(Secondpage)
                else:
                    messagebox.showerror("Error", "Invalid Login!! Try Again")
                conn.close()
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Connection problem: {e}")

        B1 = tk.Button(border, text="Submit", bg="#D2E0FB", font=("Arial", 15), command=verify)
        B1.place(x=370, y=115)

        def register():
            root = Tk()
            root.title("Register")

            bkg = "#6895D2"

            frame = tk.Frame(root, bg=bkg)

            label_email = tk.Label(frame, text="E-mail: ", font=('verdana', 12), bg=bkg)
            label_email.grid(row=0, column=0, sticky='e')
            entry_email = tk.Entry(frame)
            entry_email.grid(row=0, column=1, pady=15, padx=15)

            label_password = tk.Label(frame, text="Password: ", font=('verdana', 12), bg=bkg)
            label_password.grid(row=1, column=0, sticky='e', pady=10, padx=10)
            entry_password = tk.Entry(frame)
            entry_password.grid(row=1, column=1, pady=15, padx=15)

            label_cpassword = tk.Label(frame, text="Confirm Password: ", font=('verdana', 12), bg=bkg)
            label_cpassword.grid(row=2, column=0, sticky='e', pady=10, padx=10)
            entry_cpassword = tk.Entry(frame)
            entry_cpassword.grid(row=2, column=1, pady=15, padx=15)

            def insertData():
                try:
                    conn = sqlite3.connect('medical_data.db')
                    cursor = conn.cursor()

                    # Create the table if it does not exist
                    create_table_query = """
                        CREATE TABLE IF NOT EXISTS signup (
                            id INTEGER PRIMARY KEY,
                            email TEXT UNIQUE NOT NULL CHECK (email LIKE '%@gmail.com'),
                            password TEXT NOT NULL,
                            cpassword TEXT NOT NULL
                        )
                    """
                    cursor.execute(create_table_query)

                    # Check if all fields are filled
                    if entry_email.get() == "" or entry_password.get() == "" or entry_cpassword.get() == "":
                        messagebox.showinfo("Error", "Please fill in all the details!")
                        return

                    # Check if password and confirm password match
                    if entry_password.get() != entry_cpassword.get():
                        messagebox.showinfo("Welcome", "Your passwords don't match!")
                        return

                    # Insert data into the table
                    email = entry_email.get()
                    password = entry_password.get()
                    cpassword = entry_cpassword.get()

                    insert_query = "INSERT INTO signup (email, password, cpassword) VALUES (?, ?, ?)"
                    values = (email, password, cpassword)
                    cursor.execute(insert_query, values)
                    conn.commit()

                    # Clear entry fields
                    entry_email.delete(0, 'end')
                    entry_password.delete(0, 'end')
                    entry_cpassword.delete(0, 'end')

                    messagebox.showinfo("Welcome", "You are registered successfully!")
                    root.destroy()

                except sqlite3.Error as err:
                    messagebox.showerror("Error", f"An error occurred: {err}")

                finally:
                    cursor.close()
                    conn.close()

            button_insert = tk.Button(frame, text="Sign-Up", font=('verdana', 14), bg='#EEF5FF', command=insertData)
            button_insert.grid(row=3, column=0, columnspan=2, pady=10, padx=10)

            frame.pack() 
            root.mainloop() 

        B2 = tk.Button(self, text="Register", bg="#8EACCD", font=("Arial", 15), command=register)
        B2.place(x=650, y=20)


class Secondpage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.heading_label = tk.Label(self, text="Medical Insurance", font=("Arial", 30, 'bold'))
        self.heading_label.place(x=200, y=20)

        self.name_label = tk.Label(self, text="Name", font=("Arial", 16, 'bold'))
        self.name_label.place(x=50, y=80)
        self.name_entry = tk.Entry(self, font=("Arial", 16))
        self.name_entry.place(x=300, y=80)

        self.age_label = tk.Label(self, text="Age", font=("Arial", 16, 'bold'))
        self.age_label.place(x=50, y=120)
        self.age_entry = tk.Entry(self, font=("Arial", 16))
        self.age_entry.place(x=300, y=120)

        self.gender_label = tk.Label(self, text="Gender", font=("Arial", 16, 'bold'))
        self.gender_label.place(x=50, y=160)
        self.gender_var = tk.StringVar()
        self.gender_var.set("Male")
        self.gender_dropdown = tk.OptionMenu(self, self.gender_var, "Male", "Female", "Other")
        self.gender_dropdown.place(x=300, y=160)

        self.address_label = tk.Label(self, text="Address", font=("Arial", 16, 'bold'))
        self.address_label.place(x=50, y=200)
        self.address_entry = tk.Entry(self, font=("Arial", 16))
        self.address_entry.place(x=300, y=200)

        self.marital_status_label = tk.Label(self, text="Marital Status", font=("Arial", 16, 'bold'))
        self.marital_status_label.place(x=50, y=240)
        self.marital_status_var = tk.StringVar()
        self.marital_status_var.set("Single")
        self.marital_status_dropdown = tk.OptionMenu(self, self.marital_status_var, "Single", "Married", "Divorced", "Widowed")
        self.marital_status_dropdown.place(x=300, y=240)

        self.children_label = tk.Label(self, text="Number of Children", font=("Arial", 16, 'bold'))
        self.children_label.place(x=50, y=280)
        self.children_entry = tk.Entry(self, font=("Arial", 16))
        self.children_entry.place(x=300, y=280)

        self.disease_label = tk.Label(self, text="Disease", font=("Arial", 16, 'bold'))
        self.disease_label.place(x=50, y=320)
        self.disease_var = tk.StringVar()
        self.disease_var.set("None")
        self.disease_dropdown = tk.OptionMenu(self, self.disease_var, "None", "diabetes", "blood pressure", "cardial disease")
        self.disease_dropdown.place(x=300, y=320)

        self.predict_button = tk.Button(self, text="Predict", font=("Arial", 16, 'bold'), command=self.predict_clicked)
        self.predict_button.place(x=250, y=370)

    def predict_clicked(self):
        # Check if any field is empty
        if (not self.name_entry.get() or
            not self.age_entry.get() or
            not self.address_entry.get() or
            not self.children_entry.get()):
            messagebox.showerror("Error", "Please fill in all the details.")
            return
        
        # Check if age is greater than 18
        try:
            age = int(self.age_entry.get())
            if age <= 18:
                messagebox.showerror("Error", "Age must be greater than 18.")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid age value.")
            return

        # If all checks pass, proceed with inserting data into the database
        conn = sqlite3.connect('medical_data.db')
        c = conn.cursor()

        # Create a table if it does not exist
        c.execute('''CREATE TABLE IF NOT EXISTS medical_data 
                    (name TEXT, age INTEGER, gender TEXT, address TEXT, marital_status TEXT, children INTEGER, disease TEXT)''')

        # Get the values from the entry widgets
        name = self.name_entry.get()
        gender = self.gender_var.get()
        address = self.address_entry.get()
        marital_status = self.marital_status_var.get()
        children = int(self.children_entry.get())
        disease = self.disease_var.get()

        # Insert the data into the table
        c.execute("INSERT INTO medical_data VALUES (?, ?, ?, ?, ?, ?, ?)", (name, age, gender, address, marital_status, children, disease))

        # Commit changes and close the connection
        conn.commit()
        conn.close()

        total = 0
        gender = self.gender_var.get()
        marital_status = self.marital_status_var.get()
        disease = self.disease_var.get()

        if gender == "Male":
            if 19 <= age <= 28:
                total += 50
            elif 29 <= age <= 38:
                total += 60
            elif 39 <= age <= 48:
                total += 70
            elif 49 <= age <= 58:
                total += 80
        elif gender == "Female":
            if 19 <= age <= 28:
                total += 50
            elif 29 <= age <= 38:
                total += 60
            elif 39 <= age <= 48:
                total += 70
            elif 49 <= age <= 58:
                total += 80

        if marital_status == "Married":
            if gender == "Male":
                if 19 <= age <= 28:
                    total += 20
                elif 29 <= age <= 38:
                    total += 30
                elif 39 <= age <= 48:
                    total += 40
                elif 49 <= age <= 58:
                    total += 50
            elif gender == "Female":
                if 19 <= age <= 28:
                    total += 10
                elif 29 <= age <= 38:
                    total += 20
                elif 39 <= age <= 48:
                    total += 30
                elif 49 <= age <= 58:
                    total += 40

        if disease == "diabetes":
            if 19 <= age <= 28:
                total += 30
            elif 29 <= age <= 38:
                total += 40
            elif 39 <= age <= 48:
                total += 50
            elif 49 <= age <= 58:
                total += 60
        elif disease == "blood pressure":
            if 19 <= age <= 28:
                total += 40
            elif 29 <= age <= 38:
                total += 50
            elif 39 <= age <= 48:
                total += 60
            elif 49 <= age <= 58:
                total += 70
        elif disease == "cardial disease":
            if 19 <= age <= 28:
                total += 50
            elif 29 <= age <= 38:
                total += 60
            elif 39 <= age <= 48:
                total += 70
            elif 49 <= age <= 58:
                total += 80

        # Create a new window for the prediction result
        result_window = tk.Toplevel(self.master)
        result_window.title("Prediction Result")
        result_window.geometry('300x200')

        # Display the predicted value name label
        predicted_name_label = tk.Label(result_window, text="Predicted Value", font=("Arial", 16, 'bold'))
        predicted_name_label.place(x=60, y=50)

        # Display the predicted value
        predicted_value_entry = tk.Entry(result_window, font=("Arial", 12))
        predicted_value_entry.insert(0, str(total))
        predicted_value_entry.config(state='readonly')  # Make the entry read-only
        predicted_value_entry.place(x=60, y=100)



class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # creating window
        window = tk.Frame(self)
        window.pack()
        window.grid_rowconfigure(0, minsize=500)
        window.grid_columnconfigure(0, minsize=800)
        self.frames = {}
        for F in (Firstpage, Secondpage):
            frame = F(window,controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Firstpage)

    def show_frame(self, page, username=None):
        frame = self.frames[page]
        frame.tkraise()
        if username:
            frame.username = username
        elif page == Firstpage:
            self.title(" Login")


app = Application()
app.maxsize(900, 700)
app.mainloop()
