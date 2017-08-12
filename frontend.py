from Tkinter import *
import ttk
import backend
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_selected_row(event):
    global selected_account
    index = list1.curselection()
    selected_account = list1.get(index)


def list_accounts():
    list1.delete(0, END)
    for row in backend.view():
        list1.insert(END, row[1])


def check_existing(name):
    for row in backend.view():
        if row[1] == name:
            return True



def register_window():

    def register():
        if account_name.get() == "" or username.get() == "" or pwd.get() == "" or a1.get() == "" or a2.get() == "" or a3.get() == "":
            blank_field_popup = Toplevel(reg_window)
            warning_label = Label(blank_field_popup, text="All fields must be filled!", width=20, height=3)
            warning_label.grid(row=0, column=0)
            btn = Button(blank_field_popup, text="OK", width=10, command=blank_field_popup.destroy)
            btn.grid(row=1, column=0, columnspan=2)
        elif check_existing(account_name.get()):
            existing = Toplevel(reg_window)
            warning_label = Label(existing, text="This account name already exists.", width=30, height=4)
            warning_label.grid(row=0, column=0)
            btn = Button(existing, text="OK", width=10, command=existing.destroy)
            btn.grid(row=1, column=0, columnspan=2)
        else:
            backend.register(account_name.get(), username.get(), pwd.get(), a1.get(), a2.get(), a3.get())
            reg_window.destroy()
            list_accounts()

    reg_window = Toplevel(window)
    reg_window.wm_title("Register")

    l1 = Label(reg_window, text="Account name")
    l1.grid(row=0, column=0)
    account_name = StringVar()
    e1 = Entry(reg_window, textvariable=account_name)
    e1.grid(row=0, column=1)

    sep = ttk.Separator(reg_window, orient=HORIZONTAL)
    sep.grid(row=2, column=0, columnspan=2, sticky="ew")


    l2 = Label(reg_window, text="Username")
    l2.grid(row=3, column=0)
    username = StringVar()
    e2 = Entry(reg_window, textvariable=username)
    e2.grid(row=3, column=1)

    l3 = Label(reg_window, text="Password")
    l3.grid(row=4, column=0)
    pwd = StringVar()
    e3 = Entry(reg_window, textvariable=pwd)
    e3.grid(row=4, column=1)

    l4 = Label(reg_window, text="Answer #1")
    l4.grid(row=5, column=0)
    a1 = StringVar()
    e4 = Entry(reg_window, textvariable=a1)
    e4.grid(row=5, column=1)

    l5 = Label(reg_window, text="Answer #2")
    l5.grid(row=6, column=0)
    a2 = StringVar()
    e5 = Entry(reg_window, textvariable=a2)
    e5.grid(row=6, column=1)

    l6 = Label(reg_window, text="Answer #3")
    l6.grid(row=7, column=0)
    a3 = StringVar()
    e6 = Entry(reg_window, textvariable=a3)
    e6.grid(row=7, column=1)

    sep = ttk.Separator(reg_window, orient=HORIZONTAL)
    sep.grid(row=8, column=0, columnspan=2, sticky="ew")

    b1 = Button(reg_window, text="Register", command=register)
    b1.grid(row=9, column=0, columnspan=2)


def delete_confirm_window():

    def delete_account():
        backend.delete(selected_account)
        confirm.destroy()
        list_accounts()

    confirm = Toplevel(window)
    confirm.wm_title("Confirm")

    label = Label(confirm, text="Are you sure that you want to delete account:\n" + selected_account, width=40, height=3)
    label.grid(row=0, column=0, columnspan=4)
    b1 = Button(confirm, text="YES", command=delete_account)
    b1.grid(row=1, column=1)
    b2 = Button(confirm, text="NO", command=confirm.destroy)
    b2.grid(row=1, column=2)


def login():
    chrome_options = Options()
    chrome_options.add_argument("window-size=800,750")
    chrome_options.add_argument("window-position=300,30")
    chrome_options.add_argument("--app=https://www.webcare2.com/kerryroi/login.html")
    account = backend.get_user_info(selected_account)
    user_id = account[2]
    pwd = account[3]
    URL = "https://www.webcare2.com/kerryroi/login.html"
    answer1 = account[4]
    answer2 = account[5]
    answer3 = account[6]
    wd = webdriver.Chrome("./chromedriver", chrome_options=chrome_options)

    wd.get(URL)
    username = wd.find_element_by_name("j_username")
    password = wd.find_element_by_name("j_password")
    username.send_keys(user_id)
    password.send_keys(pwd)
    wd.find_element_by_class_name("inputtype_submit").click()

    question1 = wd.find_element_by_id("0")
    question2 = wd.find_element_by_id("1")
    question3 = wd.find_element_by_id("2")

    question1.send_keys(answer1)
    question2.send_keys(answer2)
    question3.send_keys(answer3)

    wd.find_element_by_class_name("inputtype_submit").click()
    wd.get("https://www.webcare2.com/kerryroi/users/7867cf53-0acb-469c-84f1-a2d2f89a21c0/payslips")


window = Tk()
window.wm_title("One Click Payslip")

list1 = Listbox(window, width=20, height=5)
list1.grid(row=0, column=0, rowspan=2)
list_accounts()
list1.bind("<<ListboxSelect>>", get_selected_row)

b1 = ttk.Button(window, text="Register", command=register_window)
b1.grid(row=3, column=1)

b2 = Button(window, text="Delete\n selected", height=3, width=5, command=delete_confirm_window)
b2.grid(row=0, column=1)

b3 = Button(window, text="Login", command=login)
b3.grid(row=3, column=0)

window.mainloop()
