from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    pass_entry.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_numb = [random.choice(numbers) for _ in range(nr_numbers)]
    password_symb = [random.choice(symbols) for _ in range(nr_symbols)]

    password_list = password_letters + password_numb + password_symb
    random.shuffle(password_list)

    password = "".join(password_list)  # this line of code will do the exact work
    # password = ""
    # for char in password_list:
    #     password += char

    pass_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website_name = website_entry.get()
    try:
        with open("data.json", "r") as data_file:
            website_data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No data file found!")
    else:
        email = website_data[website_name]["email"]
        password = website_data[website_name]["password"]
        messagebox.showinfo(title=website_name, message=f"Email: {email} \nPassword: {password}")


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    # retrieving entered data
    website_name = website_entry.get()
    email_name = email_entry.get()
    password = pass_entry.get()
    new_data = {
        website_name: {
            "email": email_name,
            "password": password
        }
    }

    # If there is no entry written to add
    if len(website_name) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Don't leave any fields empty!")
    else:
        # Dialog box to ask for confirmation, it will gonna return true if okay and false if cancel
        is_ok = messagebox.askokcancel(title=website_name,
                                       message=f"These are the details entered: \nEmail: {email_name} \nPassword: {
                                       password}")

        # If is_ok = True, data gets add to the json file
        if is_ok:
            try:
                # READING OLD DATA IF THE FILE EXISTS
                with open("data.json", "r") as data_file:
                    old_data = json.load(data_file)

            except FileNotFoundError:
                # IF FILE DOES NOT EXIST, THEN WRITING NEW DATA TO IT
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)

            else:
                # IF FILE EXISTS, THEN UPDATING OLD DATA WITH NEW DATA
                old_data.update(new_data)
                # ADDING OLD DATA BACK TO THE FILE
                with open("data.json", "w") as data_file:
                    json.dump(old_data, data_file, indent=4)

            finally:
                # OLD ENTRIES GET CLEARED ONCE ADDED
                website_entry.delete(0, END)
                pass_entry.delete(0, END)

        # DIALOG BOX TO SHOW SUCCUESS
        messagebox.showinfo(title="Success", message=f"Added {website_name} to the data store.")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canva = Canvas(width=200, height=200)
logo = PhotoImage(file="logo.png")
canva.create_image(130, 100, image=logo)
canva.grid(row=0, column=1)

website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
website_entry = Entry(width=36)
website_entry.focus()
website_entry.grid(row=1, column=1, sticky="EW")

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)
email_entry = Entry(width=36)
email_entry.grid(row=2, column=1, columnspan=2, sticky="EW")
email_entry.insert(0, "muskan@gmail.com")

pass_label = Label(text="Password:")
pass_label.grid(row=3, column=0)
pass_entry = Entry(width=30)
pass_entry.grid(row=3, column=1, sticky="EW")

# BUTTONS
genrate_button = Button(text="Generate Password", command=generate_password)
genrate_button.grid(row=3, column=2, sticky="EW")
add_button = Button(text="Add", width=30, command=save)
add_button.grid(row=4, column=1, columnspan=2, sticky="EW")
search_button = Button(text="search", command=find_password)
search_button.grid(row=1, column=2, sticky="EW")

window.mainloop()
