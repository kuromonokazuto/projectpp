import sqlite3
import re
import random
import string
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from time import strftime
from datetime import date
from tkinter import scrolledtext as tkst

root = Tk()
root.geometry("1366x768")
root.title("Retail Manager(ADMIN)")

user = StringVar()
passwd = StringVar()
fname = StringVar()
lname = StringVar()

with sqlite3.connect("./Database/electric.db") as db:
    cur = db.cursor()
    cur.execute("PRAGMA foreign_keys = ON")


def valid_phone(phn):
    return True

def on_start():
    create_tables()

create_households_table = """
CREATE TABLE IF NOT EXISTS households (
    id INTEGER PRIMARY KEY AUTOINCREMENT ,
    owner_name VARCHAR (30) NOT NULL ,
    address VARCHAR (100) NOT NULL ,
    phone_number VARCHAR (10) NOT NULL ,
    payment_status INTEGER NOT NULL ,
    area_id INTEGER NOT NULL ,
    monthly_consumption FLOAT,
    FOREIGN KEY (area_id) 
        REFERENCES areas (id)
            ON DELETE CASCADE 
            ON UPDATE NO ACTION 
)
"""

create_areas_table = """
CREATE TABLE IF NOT EXISTS areas (
    id INTEGER PRIMARY KEY AUTOINCREMENT ,
    price INTEGER NOT NULL 
)
"""

create_meters_table = """
CREATE TABLE IF NOT EXISTS meters (
    id INTEGER PRIMARY KEY AUTOINCREMENT ,
    household_id VARCHAR (10) NOT NULL , 
    `month` INTEGER NOT NULL ,
    `year` INTEGER NOT NULL ,
    `value` INTEGER NOT NULL ,
    FOREIGN KEY (household_id)
        REFERENCES households (id)
            ON DELETE CASCADE 
            ON UPDATE NO ACTION 
)
"""

create_accounts_table = """
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT ,
    username VARCHAR (30) NOT NULL , 
    password VARCHAR (30) NOT NULL ,
    authority VARCHAR (30) NOT NULL
)
"""

def create_tables():
    cur.execute(create_areas_table)
    cur.execute(create_households_table)
    cur.execute(create_meters_table)

class login_page:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("Retail Manager(ADMIN)")

        self.label1 = Label(root)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="images/login.png")
        self.label1.configure(image=self.img)

        self.entry1 = Entry(root)
        self.entry1.place(relx=0.373, rely=0.273, width=374, height=24)
        self.entry1.configure(font="-family {Poppins} -size 12")
        self.entry1.configure(relief="flat")
        self.entry1.configure(textvariable=user)
        self.entry1.focus_set()

        self.entry2 = Entry(root)
        self.entry2.place(relx=0.373, rely=0.384, width=374, height=24)
        self.entry2.configure(font="-family {Poppins} -size 12")
        self.entry2.configure(relief="flat")
        self.entry2.configure(show="*")
        self.entry2.configure(textvariable=passwd)

        self.button1 = Button(root)
        self.button1.place(relx=0.366, rely=0.685, width=356, height=43)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#D2463E")
        self.button1.configure(cursor="hand2")
        self.button1.configure(foreground="#ffffff")
        self.button1.configure(background="#D2463E")
        self.button1.configure(font="-family {Poppins SemiBold} -size 20")
        self.button1.configure(borderwidth="0")

        self.button1.configure(text="""LOGIN""")
        self.button1.configure(command=self.login)

    def login(self, Event=None):
        username = user.get()
        password = passwd.get()

        with sqlite3.connect("./Database/electric.db") as db:
            cur = db.cursor()
        find_user = "SELECT * FROM accounts WHERE username = ? and password = ?"
        cur.execute(find_user, [username, password])
        results = cur.fetchall()
        if results:
            if results[0][3] == "Admin":
                messagebox.showinfo("Login Page", "The login is successful.")
                page1.entry1.delete(0, END)
                page1.entry2.delete(0, END)

                root.withdraw()
                global adm
                global page2
                adm = Toplevel()
                page2 = Admin_Page(adm)
                # page2.time()
                adm.protocol("WM_DELETE_WINDOW", exitt)
                adm.mainloop()
        else:
            messagebox.showerror("Error", "Incorrect username or password.")
            page1.entry2.delete(0, END)


def exitt():
    sure = messagebox.askyesno("Exit", "Are you sure you want to exit?", parent=root)
    if sure == True:
        adm.destroy()
        root.destroy()


def households():
    adm.withdraw()
    global household
    global page3
    household = Toplevel()
    page3 = Households(household)
    page3.time()
    household.protocol("WM_DELETE_WINDOW", exitt)
    household.mainloop()


def areas():
    adm.withdraw()
    global area
    global page5
    area = Toplevel()
    page5 = Areas(area)
    page5.time()
    area.protocol("WM_DELETE_WINDOW", exitt)
    area.mainloop()


def meters():
    adm.withdraw()
    global meter
    global page7
    meter = Toplevel()
    page7 = Meters(meter)
    page7.time()
    meter.protocol("WM_DELETE_WINDOW", exitt)
    meter.mainloop()


def about():
    pass


class Admin_Page:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("ADMIN Mode")

        self.label1 = Label(adm)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        # TODO: Edit image admin.png
        self.img = PhotoImage(file="./images/admin.png")
        self.label1.configure(image=self.img)

        self.message = Label(adm)
        self.message.place(relx=0.046, rely=0.056, width=62, height=30)
        self.message.configure(font="-family {Poppins} -size 12")
        self.message.configure(foreground="#ffffff")
        self.message.configure(background="#FE6B61")
        self.message.configure(text="""ADMIN""")
        self.message.configure(anchor="w")

        self.button1 = Button(adm)
        self.button1.place(relx=0.035, rely=0.106, width=76, height=23)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#CF1E14")
        self.button1.configure(cursor="hand2")
        self.button1.configure(foreground="#ffffff")
        self.button1.configure(background="#CF1E14")
        self.button1.configure(font="-family {Poppins SemiBold} -size 12")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""Logout""")
        self.button1.configure(command=self.Logout)

        self.button2 = Button(adm)
        self.button2.place(relx=0.14, rely=0.508, width=146, height=63)
        self.button2.configure(relief="flat")
        self.button2.configure(overrelief="flat")
        self.button2.configure(activebackground="#ffffff")
        self.button2.configure(cursor="hand2")
        self.button2.configure(foreground="#333333")
        self.button2.configure(background="#ffffff")
        self.button2.configure(font="-family {Poppins SemiBold} -size 12")
        self.button2.configure(borderwidth="0")
        self.button2.configure(text="""Households""")
        self.button2.configure(command=households)

        self.button3 = Button(adm)
        self.button3.place(relx=0.338, rely=0.508, width=146, height=63)
        self.button3.configure(relief="flat")
        self.button3.configure(overrelief="flat")
        self.button3.configure(activebackground="#ffffff")
        self.button3.configure(cursor="hand2")
        self.button3.configure(foreground="#333333")
        self.button3.configure(background="#ffffff")
        self.button3.configure(font="-family {Poppins SemiBold} -size 12")
        self.button3.configure(borderwidth="0")
        self.button3.configure(text="""Areas""")
        self.button3.configure(command=areas)

        self.button4 = Button(adm)
        self.button4.place(relx=0.536, rely=0.508, width=146, height=63)
        self.button4.configure(relief="flat")
        self.button4.configure(overrelief="flat")
        self.button4.configure(activebackground="#ffffff")
        self.button4.configure(cursor="hand2")
        self.button4.configure(foreground="#333333")
        self.button4.configure(background="#ffffff")
        self.button4.configure(font="-family {Poppins SemiBold} -size 12")
        self.button4.configure(borderwidth="0")
        self.button4.configure(text="""Meters""")
        self.button4.configure(command=meters)

        self.button5 = Button(adm)
        self.button5.place(relx=0.732, rely=0.508, width=146, height=63)
        self.button5.configure(relief="flat")
        self.button5.configure(overrelief="flat")
        self.button5.configure(activebackground="#ffffff")
        self.button5.configure(cursor="hand2")
        self.button5.configure(foreground="#333333")
        self.button5.configure(background="#ffffff")
        self.button5.configure(font="-family {Poppins SemiBold} -size 12")
        self.button5.configure(borderwidth="0")
        self.button5.configure(text="""About Us""")
        self.button5.configure(command=about)

    def Logout(self):
        sure = messagebox.askyesno("Logout", "Are you sure you want to logout?", parent=adm)
        if sure == True:
            adm.destroy()
            root.deiconify()
            page1.entry1.delete(0, END)
            page1.entry2.delete(0, END)


class Households:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("Household")

        self.label1 = Label(household)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="./images/household.png")
        self.label1.configure(image=self.img)

        self.message = Label(household)
        self.message.place(relx=0.046, rely=0.055, width=136, height=30)
        self.message.configure(font="-family {Poppins} -size 10")
        self.message.configure(foreground="#000000")
        self.message.configure(background="#ffffff")
        self.message.configure(text="""ADMIN""")
        self.message.configure(anchor="w")

        self.clock = Label(household)
        self.clock.place(relx=0.9, rely=0.065, width=102, height=36)
        self.clock.configure(font="-family {Poppins Light} -size 12")
        self.clock.configure(foreground="#000000")
        self.clock.configure(background="#ffffff")

        self.entry1 = Entry(household)
        self.entry1.place(relx=0.040, rely=0.286, width=240, height=28)
        self.entry1.configure(font="-family {Poppins} -size 12")
        self.entry1.configure(relief="flat")

        self.button1 = Button(household)
        self.button1.place(relx=0.229, rely=0.289, width=76, height=23)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#CF1E14")
        self.button1.configure(cursor="hand2")
        self.button1.configure(foreground="#ffffff")
        self.button1.configure(background="#CF1E14")
        self.button1.configure(font="-family {Poppins SemiBold} -size 10")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""Search""")
        self.button1.configure(command=self.search_household)

        self.button2 = Button(household)
        self.button2.place(relx=0.035, rely=0.106, width=76, height=23)
        self.button2.configure(relief="flat")
        self.button2.configure(overrelief="flat")
        self.button2.configure(activebackground="#CF1E14")
        self.button2.configure(cursor="hand2")
        self.button2.configure(foreground="#ffffff")
        self.button2.configure(background="#CF1E14")
        self.button2.configure(font="-family {Poppins SemiBold} -size 12")
        self.button2.configure(borderwidth="0")
        self.button2.configure(text="""Logout""")
        self.button2.configure(command=self.Logout)

        self.button3 = Button(household)
        self.button3.place(relx=0.052, rely=0.432, width=306, height=28)
        self.button3.configure(relief="flat")
        self.button3.configure(overrelief="flat")
        self.button3.configure(activebackground="#CF1E14")
        self.button3.configure(cursor="hand2")
        self.button3.configure(foreground="#ffffff")
        self.button3.configure(background="#CF1E14")
        self.button3.configure(font="-family {Poppins SemiBold} -size 12")
        self.button3.configure(borderwidth="0")
        self.button3.configure(text="""ADD HOUSEHOLD""")
        self.button3.configure(command=self.add_household)

        self.button4 = Button(household)
        self.button4.place(relx=0.052, rely=0.5, width=306, height=28)
        self.button4.configure(relief="flat")
        self.button4.configure(overrelief="flat")
        self.button4.configure(activebackground="#CF1E14")
        self.button4.configure(cursor="hand2")
        self.button4.configure(foreground="#ffffff")
        self.button4.configure(background="#CF1E14")
        self.button4.configure(font="-family {Poppins SemiBold} -size 12")
        self.button4.configure(borderwidth="0")
        self.button4.configure(text="""UPDATE HOUSEHOLD""")
        self.button4.configure(command=self.update_household)

        self.button5 = Button(household)
        self.button5.place(relx=0.052, rely=0.57, width=306, height=28)
        self.button5.configure(relief="flat")
        self.button5.configure(overrelief="flat")
        self.button5.configure(activebackground="#CF1E14")
        self.button5.configure(cursor="hand2")
        self.button5.configure(foreground="#ffffff")
        self.button5.configure(background="#CF1E14")
        self.button5.configure(font="-family {Poppins SemiBold} -size 12")
        self.button5.configure(borderwidth="0")
        self.button5.configure(text="""DELETE HOUSEHOLD""")
        self.button5.configure(command=self.delete_household)

        self.button6 = Button(household)
        self.button6.place(relx=0.135, rely=0.885, width=76, height=23)
        self.button6.configure(relief="flat")
        self.button6.configure(overrelief="flat")
        self.button6.configure(activebackground="#CF1E14")
        self.button6.configure(cursor="hand2")
        self.button6.configure(foreground="#ffffff")
        self.button6.configure(background="#CF1E14")
        self.button6.configure(font="-family {Poppins SemiBold} -size 12")
        self.button6.configure(borderwidth="0")
        self.button6.configure(text="""EXIT""")
        self.button6.configure(command=self.Exit)

        self.scrollbarx = Scrollbar(household, orient=HORIZONTAL)
        self.scrollbary = Scrollbar(household, orient=VERTICAL)
        self.tree = ttk.Treeview(household)
        self.tree.place(relx=0.307, rely=0.203, width=880, height=550)
        self.tree.configure(
            # TODO:???
            yscrollcommand=self.scrollbary.set, xscrollcommand=self.scrollbarx.set
        )
        self.tree.configure(selectmode="extended")

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.scrollbary.configure(command=self.tree.yview)
        self.scrollbarx.configure(command=self.tree.xview)

        self.scrollbary.place(relx=0.954, rely=0.203, width=22, height=548)
        self.scrollbarx.place(relx=0.307, rely=0.924, width=884, height=22)

        self.tree.configure(
            columns=(
                "Household ID",
                "Owner Name",
                "Address",
                "Phone Number",
                "Payment Status",
                "Area ID",
                "Monthly Consumption",
            )
        )

        self.tree.heading("Household ID", text="Household ID", anchor=W)
        self.tree.heading("Owner Name", text="Owner Name", anchor=W)
        self.tree.heading("Address", text="Address", anchor=W)
        self.tree.heading("Phone Number", text="Phone Number", anchor=W)
        self.tree.heading("Payment Status", text="Payment Status", anchor=W)
        self.tree.heading("Area ID", text="Area ID", anchor=W)
        self.tree.heading("Monthly Consumption", text="Monthly Consumption", anchor=W)

        self.tree.column("#0", stretch=NO, minwidth=0, width=0)
        self.tree.column("#1", stretch=NO, minwidth=0, width=80)
        self.tree.column("#2", stretch=NO, minwidth=0, width=260)
        self.tree.column("#3", stretch=NO, minwidth=0, width=198)
        self.tree.column("#4", stretch=NO, minwidth=0, width=100)
        self.tree.column("#5", stretch=NO, minwidth=0, width=80)
        self.tree.column("#6", stretch=NO, minwidth=0, width=80)
        self.tree.column("#7", stretch=NO, minwidth=0, width=80)

        self.DisplayData()

    def DisplayData(self):
        cur.execute("SELECT * FROM households")
        fetch = cur.fetchall()
        for data in fetch:
            self.tree.insert("", "end", values=(data))

    def search_household(self):
        val = []
        for i in self.tree.get_children():
            val.append(i)
            for j in self.tree.item(i)["values"]:
                val.append(j)

        try:
            to_search = int(self.entry1.get())
        except ValueError:
            messagebox.showerror("Oops!!", "Invalid Household ID.", parent=household)
        else:
            for search in val:
                if search == to_search:
                    self.tree.selection_set(val[val.index(search) - 1])
                    self.tree.focus(val[val.index(search) - 1])
                    messagebox.showinfo("Success!!", "Household ID: {} found.".format(self.entry1.get()),
                                        parent=household)
                    break
            else:
                messagebox.showerror("Oops!!", "Household ID: {} not found.".format(self.entry1.get()),
                                     parent=household)

    # TODO:??
    sel = []

    def on_tree_select(self, Event):
        self.sel.clear()
        for i in self.tree.selection():
            if i not in self.sel:
                self.sel.append(i)

    def delete_household(self):
        val = []
        to_delete = []

        if len(self.sel) != 0:
            sure = messagebox.askyesno("Confirm", "Are you sure you want to delete selected households?",
                                       parent=household)
            if sure:
                for i in self.sel:
                    for j in self.tree.item(i)["values"]:
                        val.append(j)

                for j in range(len(val)):
                    if j % 7 == 0:
                        to_delete.append(val[j])

                for k in to_delete:
                    delete = "DELETE FROM households WHERE id = ?"
                    cur.execute(delete, [k])
                    db.commit()

                messagebox.showinfo("Success!!", "Households deleted from database.", parent=household)
                self.sel.clear()
                self.tree.delete(*self.tree.get_children())

                self.DisplayData()
        else:
            messagebox.showerror("Error!!", "Please select a household.", parent=household)

    def update_household(self):
        if len(self.sel) == 1:
            global hh_update
            hh_update = Toplevel()
            page9 = Update_Household(hh_update)
            page9.time()
            hh_update.protocol("WM_DELETE_WINDOW", self.ex2)
            global valll
            valll = []
            for i in self.sel:
                for j in self.tree.item(i)["values"]:
                    valll.append(j)

            page9.entry1.insert(0, valll[1])
            page9.entry2.insert(0, valll[2])
            page9.entry3.insert(0, valll[4])
            page9.entry6.insert(0, valll[3])
            page9.entry7.insert(0, valll[6])


        elif len(self.sel) == 0:
            messagebox.showerror("Error", "Please choose a household to update.", parent=household)
        else:
            messagebox.showerror("Error", "Can only update one household at a time.", parent=household)

        hh_update.mainloop()

    def add_household(self):
        global hh_add
        global page4
        hh_add = Toplevel()
        page4 = add_household(hh_add)
        page4.time()
        hh_add.mainloop()

    def time(self):
        # ??
        string = strftime("%H:%M:%S %p")
        self.clock.config(text=string)
        self.clock.after(1000, self.time)

    def Exit(self):
        sure = messagebox.askyesno("Exit", "Are you sure you want to exit?", parent=household)
        if sure:
            household.destroy()
            adm.deiconify()

    def ex2(self):
        sure = messagebox.askyesno("Exit", "Are you sure you want to exit?", parent=hh_update)
        if sure == True:
            hh_update.destroy()
            household.deiconify()

    def Logout(self):
        sure = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if sure == True:
            root.deiconify()
            page1.entry1.delete(0, END)
            page1.entry2.delete(0, END)


class add_household:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("Add Household")

        self.label1 = Label(hh_add)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="./images/add_household.png")
        self.label1.configure(image=self.img)

        self.clock = Label(hh_add)
        self.clock.place(relx=0.84, rely=0.065, width=102, height=36)
        self.clock.configure(font="-family {Poppins Light} -size 12")
        self.clock.configure(foreground="#000000")
        self.clock.configure(background="#ffffff")

        self.entry1 = Entry(hh_add)
        self.entry1.place(relx=0.132, rely=0.296, width=996, height=30)
        self.entry1.configure(font="-family {Poppins} -size 12")
        self.entry1.configure(relief="flat")

        self.entry2 = Entry(hh_add)
        self.entry2.place(relx=0.132, rely=0.413, width=374, height=30)
        self.entry2.configure(font="-family {Poppins} -size 12")
        self.entry2.configure(relief="flat")

        self.r2 = hh_add.register(self.testint)

        self.entry3 = Entry(hh_add)
        self.entry3.place(relx=0.132, rely=0.529, width=374, height=30)
        self.entry3.configure(font="-family {Poppins} -size 12")
        self.entry3.configure(relief="flat")
        self.entry3.configure(validate="key", validatecommand=(self.r2, "%P"))

        self.entry4 = Entry(hh_add)
        self.entry4.place(relx=0.132, rely=0.646, width=374, height=30)
        self.entry4.configure(font="-family {Poppins} -size 12")
        self.entry4.configure(relief="flat")
        self.entry4.configure(validate="key", validatecommand=(self.r2, "%P"))

        self.entry6 = Entry(hh_add)
        self.entry6.place(relx=0.527, rely=0.413, width=374, height=30)
        self.entry6.configure(font="-family {Poppins} -size 12")
        self.entry6.configure(relief="flat")
        self.entry6.configure(validate="key", validatecommand=(self.r2, "%P"))

        self.entry7 = Entry(hh_add)
        self.entry7.place(relx=0.527, rely=0.529, width=374, height=30)
        self.entry7.configure(font="-family {Poppins} -size 12")
        self.entry7.configure(relief="flat")
        self.entry7.configure(validate="key", validatecommand=(self.r2, "%P"))

        self.button1 = Button(hh_add)
        self.button1.place(relx=0.408, rely=0.836, width=96, height=34)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#CF1E14")
        self.button1.configure(cursor="hand2")
        self.button1.configure(foreground="#ffffff")
        self.button1.configure(background="#CF1E14")
        self.button1.configure(font="-family {Poppins SemiBold} -size 14")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""ADD""")
        self.button1.configure(command=self.add)

        self.button2 = Button(hh_add)
        self.button2.place(relx=0.526, rely=0.836, width=86, height=34)
        self.button2.configure(relief="flat")
        self.button2.configure(overrelief="flat")
        self.button2.configure(activebackground="#CF1E14")
        self.button2.configure(cursor="hand2")
        self.button2.configure(foreground="#ffffff")
        self.button2.configure(background="#CF1E14")
        self.button2.configure(font="-family {Poppins SemiBold} -size 14")
        self.button2.configure(borderwidth="0")
        self.button2.configure(text="""CLEAR""")
        self.button2.configure(command=self.clearr)

    def add(self):
        owner_name = self.entry1.get()
        address = self.entry2.get()
        area_id = self.entry3.get()
        phone_number = self.entry4.get()
        register_month = self.entry6.get()
        register_year = self.entry7.get()

        if owner_name.strip():
            if address.strip():
                try:
                    int(register_year)
                except ValueError:
                    messagebox.showerror("Oops!", "Invalid register year.", parent=hh_add)
                else:
                    try:
                        int(register_month)
                    except ValueError:
                        messagebox.showerror("Oops!", "Invalid register month.", parent=hh_add)
                    else:
                        if 1 <= int(register_month) <= 12:
                            try:
                                int(area_id)
                            except ValueError:
                                messagebox.showerror("Oops!", "Invalid area ID.", parent=hh_add)
                            else:
                                with sqlite3.connect("./Database/electric.db") as db:
                                    cur = db.cursor()
                                cur.execute("""SELECT id FROM areas""")
                                results = cur.fetchall()
                                area_ids = []
                                for result in results:
                                    area_ids.append(result[0])
                                if int(area_id) not in area_ids:
                                    messagebox.showerror("Oops!", "Area ID does not exist.", parent=hh_add)
                                else:
                                    if valid_phone(phone_number):
                                        with sqlite3.connect("./Database/electric.db") as db:
                                            cur = db.cursor()
                                        insert_into_households = (
                                            "INSERT INTO households (owner_name, address, phone_number, payment_status, area_id, monthly_consumption) VALUES(?,?,?,?,?,?)"
                                        )
                                        cur.execute(insert_into_households,
                                                    [owner_name, address, phone_number, 0, int(area_id), 0])
                                        db.commit()

                                        cur.execute("""SELECT id FROM households""")
                                        results = cur.fetchall()
                                        household_id = results[-1][0]
                                        insert_into_meters = (
                                            "INSERT INTO meters (household_id, `month`, `year`, `value`) VALUES (?,?,?,?)"
                                        )
                                        cur.execute(insert_into_meters,
                                                    [household_id, int(register_month), int(register_year), 0])
                                        db.commit()

                                        messagebox.showinfo("Success!!", "Household successfully added into database.",
                                                            parent=hh_add)
                                        hh_add.destroy()
                                        page3.tree.delete(*page3.tree.get_children())
                                        page3.DisplayData()
                                        hh_add.destroy()
                                    else:
                                        messagebox.showerror("Oops!", "Invalid phone number.", parent=hh_add)
                        else:
                            messagebox.showerror("Oops!", "Invalid register month.", parent=hh_add)
            else:
                messagebox.showerror("Oops!", "Please enter product category.", parent=hh_add)
        else:
            messagebox.showerror("Oops!", "Please enter product name", parent=hh_add)

    def clearr(self):
        self.entry1.delete(0, END)
        self.entry2.delete(0, END)
        self.entry3.delete(0, END)
        self.entry4.delete(0, END)
        self.entry6.delete(0, END)
        self.entry7.delete(0, END)

    def testint(self, val):
        if val.isdigit():
            return True
        elif val == "":
            return True
        return False

    def time(self):
        string = strftime("%H:%M:%S %p")
        self.clock.config(text=string)
        self.clock.after(1000, self.time)


class Update_Household:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("Update Household")

        self.label1 = Label(hh_update)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="./images/update_household.png")
        self.label1.configure(image=self.img)

        self.clock = Label(hh_update)
        self.clock.place(relx=0.84, rely=0.065, width=102, height=36)
        self.clock.configure(font="-family {Poppins Light} -size 12")
        self.clock.configure(foreground="#000000")
        self.clock.configure(background="#ffffff")

        self.entry1 = Entry(hh_update)
        self.entry1.place(relx=0.132, rely=0.296, width=996, height=30)
        self.entry1.configure(font="-family {Poppins} -size 12")
        self.entry1.configure(relief="flat")

        self.entry2 = Entry(hh_update)
        self.entry2.place(relx=0.132, rely=0.413, width=374, height=30)
        self.entry2.configure(font="-family {Poppins} -size 12")
        self.entry2.configure(relief="flat")

        self.r2 = hh_update.register(self.testint)

        self.entry3 = Entry(hh_update)
        self.entry3.place(relx=0.132, rely=0.529, width=374, height=30)
        self.entry3.configure(font="-family {Poppins} -size 12")
        self.entry3.configure(relief="flat")
        self.entry3.configure(validate="key", validatecommand=(self.r2, "%P"))

        self.entry6 = Entry(hh_update)
        self.entry6.place(relx=0.527, rely=0.413, width=374, height=30)
        self.entry6.configure(font="-family {Poppins} -size 12")
        self.entry6.configure(relief="flat")
        self.entry6.configure(validate="key", validatecommand=(self.r2, "%P"))

        self.entry7 = Entry(hh_update)
        self.entry7.place(relx=0.527, rely=0.529, width=374, height=30)
        self.entry7.configure(font="-family {Poppins} -size 12")
        self.entry7.configure(relief="flat")
        self.entry7.configure(validate="key", validatecommand=(self.r2, "%P"))

        self.button1 = Button(hh_update)
        self.button1.place(relx=0.408, rely=0.836, width=96, height=34)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#CF1E14")
        self.button1.configure(cursor="hand2")
        self.button1.configure(foreground="#ffffff")
        self.button1.configure(background="#CF1E14")
        self.button1.configure(font="-family {Poppins SemiBold} -size 14")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""UPDATE""")
        self.button1.configure(command=self.update)

        self.button2 = Button(hh_update)
        self.button2.place(relx=0.526, rely=0.836, width=86, height=34)
        self.button2.configure(relief="flat")
        self.button2.configure(overrelief="flat")
        self.button2.configure(activebackground="#CF1E14")
        self.button2.configure(cursor="hand2")
        self.button2.configure(foreground="#ffffff")
        self.button2.configure(background="#CF1E14")
        self.button2.configure(font="-family {Poppins SemiBold} -size 14")
        self.button2.configure(borderwidth="0")
        self.button2.configure(text="""CLEAR""")
        self.button2.configure(command=self.clearr)

    def update(self):
        owner_name = self.entry1.get()
        address = self.entry2.get()
        area_id = self.entry3.get()
        phone_number = self.entry6.get()
        payment_status = self.entry7.get()

        if owner_name.strip():
            if address.strip():
                try:
                    int(area_id)
                except ValueError:
                    messagebox.showerror("Oops!", "Invalid area ID.", parent=hh_update)
                else:
                    if valid_phone(phone_number):
                        try:
                            int(payment_status)
                        except ValueError:
                            messagebox.showerror("Oops!", "Invalid payment status.", parent=hh_update)
                        else:
                            if 0 <= int(payment_status) <= 2:
                                with sqlite3.connect("./Database/electric.db") as db:
                                    cur = db.cursor()
                                cur.execute("""SELECT id FROM areas""")
                                results = cur.fetchall()
                                area_ids = []
                                for result in results:
                                    area_ids.append(result[0])
                                if int(area_id) not in area_ids:
                                    messagebox.showerror("Oops!", "Area ID does not exist.", parent=hh_update)
                                else:
                                    if valid_phone(phone_number):
                                        household_id = valll[0]
                                        with sqlite3.connect("./Database/electric.db") as db:
                                            cur = db.cursor()
                                        update = (
                                            "UPDATE households SET owner_name=?, address=?, phone_number=?,  payment_status=?, area_id=? WHERE id=?"
                                        )
                                        cur.execute(update,
                                                    [owner_name, address, phone_number, payment_status, int(area_id),
                                                     household_id])
                                        db.commit()

                                        messagebox.showinfo("Success!!", "Household successfully updated in database.",
                                                            parent=hh_update)
                                        valll.clear()
                                        Households.sel.clear()
                                        page3.tree.delete(*page3.tree.get_children())
                                        page3.DisplayData()
                                        hh_update.destroy()
                            else:
                                messagebox.showerror("Oops!", "Payment status must be an integer from 0 to 2.",
                                                     parent=hh_update)
                    else:
                        messagebox.showerror("Oops!", "Invalid phone number.", parent=hh_update)
            else:
                messagebox.showerror("Oops!", "Please enter product category.", parent=hh_update)
        else:
            messagebox.showerror("Oops!", "Please enter product name", parent=hh_update)

    def clearr(self):
        self.entry1.delete(0, END)
        self.entry2.delete(0, END)
        self.entry3.delete(0, END)
        self.entry6.delete(0, END)
        self.entry7.delete(0, END)

    def testint(self, val):
        if val.isdigit():
            return True
        elif val == "":
            return True
        return False

    def time(self):
        string = strftime("%H:%M:%S %p")
        self.clock.config(text=string)
        self.clock.after(1000, self.time)


class Areas:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("Area")

        self.label1 = Label(area)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="./images/area.png")
        self.label1.configure(image=self.img)

        self.message = Label(area)
        self.message.place(relx=0.046, rely=0.055, width=136, height=30)
        self.message.configure(font="-family {Poppins} -size 10")
        self.message.configure(foreground="#000000")
        self.message.configure(background="#ffffff")
        self.message.configure(text="""ADMIN""")
        self.message.configure(anchor="w")

        self.clock = Label(area)
        self.clock.place(relx=0.9, rely=0.065, width=102, height=36)
        self.clock.configure(font="-family {Poppins Light} -size 12")
        self.clock.configure(foreground="#000000")
        self.clock.configure(background="#ffffff")

        self.entry1 = Entry(area)
        self.entry1.place(relx=0.040, rely=0.286, width=240, height=28)
        self.entry1.configure(font="-family {Poppins} -size 12")
        self.entry1.configure(relief="flat")

        self.button1 = Button(area)
        self.button1.place(relx=0.229, rely=0.289, width=76, height=23)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#CF1E14")
        self.button1.configure(cursor="hand2")
        self.button1.configure(foreground="#ffffff")
        self.button1.configure(background="#CF1E14")
        self.button1.configure(font="-family {Poppins SemiBold} -size 10")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""Search""")
        self.button1.configure(command=self.search_area)

        self.button2 = Button(area)
        self.button2.place(relx=0.035, rely=0.106, width=76, height=23)
        self.button2.configure(relief="flat")
        self.button2.configure(overrelief="flat")
        self.button2.configure(activebackground="#CF1E14")
        self.button2.configure(cursor="hand2")
        self.button2.configure(foreground="#ffffff")
        self.button2.configure(background="#CF1E14")
        self.button2.configure(font="-family {Poppins SemiBold} -size 12")
        self.button2.configure(borderwidth="0")
        self.button2.configure(text="""Logout""")
        self.button2.configure(command=self.Logout)

        self.button3 = Button(area)
        self.button3.place(relx=0.052, rely=0.432, width=306, height=28)
        self.button3.configure(relief="flat")
        self.button3.configure(overrelief="flat")
        self.button3.configure(activebackground="#CF1E14")
        self.button3.configure(cursor="hand2")
        self.button3.configure(foreground="#ffffff")
        self.button3.configure(background="#CF1E14")
        self.button3.configure(font="-family {Poppins SemiBold} -size 12")
        self.button3.configure(borderwidth="0")
        self.button3.configure(text="""ADD AREA""")
        self.button3.configure(command=self.add_area)

        self.button4 = Button(area)
        self.button4.place(relx=0.052, rely=0.5, width=306, height=28)
        self.button4.configure(relief="flat")
        self.button4.configure(overrelief="flat")
        self.button4.configure(activebackground="#CF1E14")
        self.button4.configure(cursor="hand2")
        self.button4.configure(foreground="#ffffff")
        self.button4.configure(background="#CF1E14")
        self.button4.configure(font="-family {Poppins SemiBold} -size 12")
        self.button4.configure(borderwidth="0")
        self.button4.configure(text="""UPDATE AREA""")
        self.button4.configure(command=self.update_area)

        self.button5 = Button(area)
        self.button5.place(relx=0.052, rely=0.57, width=306, height=28)
        self.button5.configure(relief="flat")
        self.button5.configure(overrelief="flat")
        self.button5.configure(activebackground="#CF1E14")
        self.button5.configure(cursor="hand2")
        self.button5.configure(foreground="#ffffff")
        self.button5.configure(background="#CF1E14")
        self.button5.configure(font="-family {Poppins SemiBold} -size 12")
        self.button5.configure(borderwidth="0")
        self.button5.configure(text="""DELETE AREA""")
        self.button5.configure(command=self.delete_area)

        self.button6 = Button(area)
        self.button6.place(relx=0.135, rely=0.885, width=76, height=23)
        self.button6.configure(relief="flat")
        self.button6.configure(overrelief="flat")
        self.button6.configure(activebackground="#CF1E14")
        self.button6.configure(cursor="hand2")
        self.button6.configure(foreground="#ffffff")
        self.button6.configure(background="#CF1E14")
        self.button6.configure(font="-family {Poppins SemiBold} -size 12")
        self.button6.configure(borderwidth="0")
        self.button6.configure(text="""EXIT""")
        self.button6.configure(command=self.Exit)

        self.scrollbarx = Scrollbar(area, orient=HORIZONTAL)
        self.scrollbary = Scrollbar(area, orient=VERTICAL)
        self.tree = ttk.Treeview(area)
        self.tree.place(relx=0.307, rely=0.203, width=880, height=550)
        self.tree.configure(
            yscrollcommand=self.scrollbary.set, xscrollcommand=self.scrollbarx.set
        )
        self.tree.configure(selectmode="extended")

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.scrollbary.configure(command=self.tree.yview)
        self.scrollbarx.configure(command=self.tree.xview)

        self.scrollbary.place(relx=0.954, rely=0.203, width=22, height=548)
        self.scrollbarx.place(relx=0.307, rely=0.924, width=884, height=22)

        self.tree.configure(
            columns=(
                "Area ID",
                "Area Price",
            )
        )

        self.tree.heading("Area ID", text="Area ID", anchor=W)
        self.tree.heading("Area Price", text="Area Price", anchor=W)

        self.tree.column("#0", stretch=NO, minwidth=0, width=0)
        self.tree.column("#1", stretch=NO, minwidth=0, width=220)
        self.tree.column("#2", stretch=NO, minwidth=0, width=660)

        self.DisplayData()

    def DisplayData(self):
        cur.execute("SELECT * FROM areas")
        fetch = cur.fetchall()
        for data in fetch:
            # TODO: ???
            self.tree.insert("", "end", values=(data))

    def search_area(self):
        val = []
        for i in self.tree.get_children():
            val.append(i)
            for j in self.tree.item(i)["values"]:
                val.append(j)

        try:
            to_search = int(self.entry1.get())
        except ValueError:
            messagebox.showerror("Oops!!", "Invalid Area ID.", parent=area)
        else:
            for search in val:
                if search == to_search:
                    self.tree.selection_set(val[val.index(search) - 1])
                    self.tree.focus(val[val.index(search) - 1])
                    messagebox.showinfo("Success!!", "Area ID: {} found.".format(self.entry1.get()),
                                        parent=area)
                    break
            else:
                messagebox.showerror("Oops!!", "Area ID: {} not found.".format(self.entry1.get()),
                                     parent=area)

    sel = []

    def on_tree_select(self, Event):
        self.sel.clear()
        for i in self.tree.selection():
            if i not in self.sel:
                self.sel.append(i)

    def delete_area(self):
        val = []
        to_delete = []

        if len(self.sel) != 0:
            sure = messagebox.askyesno("Confirm", "Are you sure you want to delete selected area(s)?", parent=area)
            if sure == True:
                for i in self.sel:
                    for j in self.tree.item(i)["values"]:
                        val.append(j)
                # TODO: ???
                for j in range(len(val)):
                    if j % 2 == 0:
                        to_delete.append(val[j])

                for k in to_delete:
                    delete = "DELETE FROM areas WHERE id = ?"
                    cur.execute(delete, [k])
                    db.commit()

                messagebox.showinfo("Success!!", "Area(s) deleted from database.", parent=area)
                self.sel.clear()
                self.tree.delete(*self.tree.get_children())
                self.DisplayData()
        else:
            messagebox.showerror("Error!!", "Please select an employee.", parent=area)

    def update_area(self):

        if len(self.sel) == 1:
            global area_update
            area_update = Toplevel()
            page8 = Update_Area(area_update)
            page8.time()
            area_update.protocol("WM_DELETE_WINDOW", self.ex2)
            global vall
            vall = []
            for i in self.sel:
                for j in self.tree.item(i)["values"]:
                    vall.append(j)

            page8.entry1.insert(0, vall[1])
            area_update.mainloop()
        elif len(self.sel) == 0:
            messagebox.showerror("Error", "Please select an area to update.")
        else:
            messagebox.showerror("Error", "Can only update one area at a time.")

    def add_area(self):
        global area_add
        area_add = Toplevel()
        page6 = add_area(area_add)
        page6.time()
        area_add.protocol("WM_DELETE_WINDOW", self.ex)
        area_add.mainloop()

    def ex(self):
        area_add.destroy()
        self.tree.delete(*self.tree.get_children())
        self.DisplayData()

    def ex2(self):
        area_update.destroy()
        self.tree.delete(*self.tree.get_children())
        self.DisplayData()

    def time(self):
        string = strftime("%H:%M:%S %p")
        self.clock.config(text=string)
        self.clock.after(1000, self.time)

    def Exit(self):
        sure = messagebox.askyesno("Exit", "Are you sure you want to exit?", parent=area)
        if sure == True:
            area.destroy()
            adm.deiconify()

    def Logout(self):
        sure = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if sure == True:
            area.destroy()
            root.deiconify()

            page1.entry1.delete(0, END)
            page1.entry2.delete(0, END)


class add_area:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("Add Area")

        self.label1 = Label(area_add)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="./images/add_area.png")
        self.label1.configure(image=self.img)

        self.clock = Label(area_add)
        self.clock.place(relx=0.84, rely=0.065, width=102, height=36)
        self.clock.configure(font="-family {Poppins Light} -size 12")
        self.clock.configure(foreground="#000000")
        self.clock.configure(background="#ffffff")

        self.r1 = area_add.register(self.testint)
        self.entry1 = Entry(area_add)
        self.entry1.place(relx=0.47, rely=0.4325, width=50, height=30)
        self.entry1.configure(font="-family {Poppins} -size 12")
        self.entry1.configure(relief="flat")
        self.entry1.configure(validate="key", validatecommand=(self.r1, "%P"))
        self.entry1.focus_set()

        self.button1 = Button(area_add)
        self.button1.place(relx=0.408, rely=0.836, width=96, height=34)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#CF1E14")
        self.button1.configure(cursor="hand2")
        self.button1.configure(foreground="#ffffff")
        self.button1.configure(background="#CF1E14")
        self.button1.configure(font="-family {Poppins SemiBold} -size 14")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""ADD""")
        self.button1.configure(command=self.add)

        self.button2 = Button(area_add)
        self.button2.place(relx=0.526, rely=0.836, width=86, height=34)
        self.button2.configure(relief="flat")
        self.button2.configure(overrelief="flat")
        self.button2.configure(activebackground="#CF1E14")
        self.button2.configure(cursor="hand2")
        self.button2.configure(foreground="#ffffff")
        self.button2.configure(background="#CF1E14")
        self.button2.configure(font="-family {Poppins SemiBold} -size 14")
        self.button2.configure(borderwidth="0")
        self.button2.configure(text="""CLEAR""")
        self.button2.configure(command=self.clearr)

    def testint(self, val):
        if val.isdigit():
            return True
        elif val == "":
            return True
        return False

    def time(self):
        string = strftime("%H:%M:%S %p")
        self.clock.config(text=string)
        self.clock.after(1000, self.time)

    def add(self):
        area_price = self.entry1.get()

        if area_price.strip():
            try:
                int(area_price)
            except ValueError:
                messagebox.showerror("Oops!", "Invalid Area Price.")
            else:
                insert = (
                    "INSERT INTO areas (price) VALUES (?)"
                )
                cur.execute(insert, [area_price])
                db.commit()
                messagebox.showinfo("Success!!", "Area was successfully added into database.",
                                    parent=area_add)
                self.clearr()
        else:
            messagebox.showerror("Oops!", "Please enter area price.", parent=area_add)

    def clearr(self):
        self.entry1.delete(0, END)


class Update_Area:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("Update Area")

        self.label1 = Label(area_update)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="./images/update_area.png")
        self.label1.configure(image=self.img)

        self.clock = Label(area_update)
        self.clock.place(relx=0.84, rely=0.065, width=102, height=36)
        self.clock.configure(font="-family {Poppins Light} -size 12")
        self.clock.configure(foreground="#000000")
        self.clock.configure(background="#ffffff")

        self.r1 = area_update.register(self.testint)

        self.entry1 = Entry(area_update)
        self.entry1.place(relx=0.49, rely=0.415, width=50, height=30)
        self.entry1.configure(font="-family {Poppins} -size 12")
        self.entry1.configure(relief="flat")
        self.entry1.configure(validate="key", validatecommand=(self.r1, "%P"))
        self.entry1.focus_set()

        self.button1 = Button(area_update)
        self.button1.place(relx=0.408, rely=0.836, width=96, height=34)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#CF1E14")
        self.button1.configure(cursor="hand2")
        self.button1.configure(foreground="#ffffff")
        self.button1.configure(background="#CF1E14")
        self.button1.configure(font="-family {Poppins SemiBold} -size 14")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""UPDATE""")
        self.button1.configure(command=self.update)

        self.button2 = Button(area_update)
        self.button2.place(relx=0.526, rely=0.836, width=86, height=34)
        self.button2.configure(relief="flat")
        self.button2.configure(overrelief="flat")
        self.button2.configure(activebackground="#CF1E14")
        self.button2.configure(cursor="hand2")
        self.button2.configure(foreground="#ffffff")
        self.button2.configure(background="#CF1E14")
        self.button2.configure(font="-family {Poppins SemiBold} -size 14")
        self.button2.configure(borderwidth="0")
        self.button2.configure(text="""CLEAR""")
        self.button2.configure(command=self.clearr)

    def update(self):
        area_price = self.entry1.get()

        if area_price.strip():
            try:
                int(area_price)
            except ValueError:
                messagebox.showerror("Oops!", "Invalid Area Price.")
            else:
                id = vall[0]
                update = (
                    "UPDATE areas SET price = ? WHERE id = ?"
                )
                cur.execute(update, [area_price, id])
                db.commit()
                messagebox.showinfo("Success!!",
                                    "Area was successfully updated in database.",
                                    parent=area_update)
                vall.clear()
                page5.tree.delete(*page5.tree.get_children())
                page5.DisplayData()
                Areas.sel.clear()
                area_update.destroy()
        else:
            messagebox.showerror("Oops!", "Please enter area price.", parent=area_add)

    def clearr(self):
        self.entry1.delete(0, END)

    def testint(self, val):
        if val.isdigit():
            return True
        elif val == "":
            return True
        return False

    def time(self):
        string = strftime("%H:%M:%S %p")
        self.clock.config(text=string)
        self.clock.after(1000, self.time)


class Meters:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("Meters")

        self.label1 = Label(meter)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="./images/meter.png")
        self.label1.configure(image=self.img)

        self.message = Label(meter)
        self.message.place(relx=0.046, rely=0.055, width=136, height=30)
        self.message.configure(font="-family {Poppins} -size 10")
        self.message.configure(foreground="#000000")
        self.message.configure(background="#ffffff")
        self.message.configure(text="""ADMIN""")
        self.message.configure(anchor="w")

        self.clock = Label(meter)
        self.clock.place(relx=0.9, rely=0.065, width=102, height=36)
        self.clock.configure(font="-family {Poppins Light} -size 12")
        self.clock.configure(foreground="#000000")
        self.clock.configure(background="#ffffff")

        self.entry1 = Entry(meter)
        self.entry1.place(relx=0.040, rely=0.286, width=240, height=28)
        self.entry1.configure(font="-family {Poppins} -size 12")
        self.entry1.configure(relief="flat")

        self.button1 = Button(meter)
        self.button1.place(relx=0.229, rely=0.289, width=76, height=23)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#CF1E14")
        self.button1.configure(cursor="hand2")
        self.button1.configure(foreground="#ffffff")
        self.button1.configure(background="#CF1E14")
        self.button1.configure(font="-family {Poppins SemiBold} -size 10")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""Search""")
        self.button1.configure(command=self.search_meter)

        self.button2 = Button(meter)
        self.button2.place(relx=0.035, rely=0.106, width=76, height=23)
        self.button2.configure(relief="flat")
        self.button2.configure(overrelief="flat")
        self.button2.configure(activebackground="#CF1E14")
        self.button2.configure(cursor="hand2")
        self.button2.configure(foreground="#ffffff")
        self.button2.configure(background="#CF1E14")
        self.button2.configure(font="-family {Poppins SemiBold} -size 12")
        self.button2.configure(borderwidth="0")
        self.button2.configure(text="""Logout""")
        self.button2.configure(command=self.Logout)

        self.button3 = Button(meter)
        self.button3.place(relx=0.052, rely=0.432, width=306, height=28)
        self.button3.configure(relief="flat")
        self.button3.configure(overrelief="flat")
        self.button3.configure(activebackground="#CF1E14")
        self.button3.configure(cursor="hand2")
        self.button3.configure(foreground="#ffffff")
        self.button3.configure(background="#CF1E14")
        self.button3.configure(font="-family {Poppins SemiBold} -size 12")
        self.button3.configure(borderwidth="0")
        self.button3.configure(text="""ADD METER""")
        self.button3.configure(command=self.add_meter)

        self.button4 = Button(meter)
        self.button4.place(relx=0.052, rely=0.5, width=306, height=28)
        self.button4.configure(relief="flat")
        self.button4.configure(overrelief="flat")
        self.button4.configure(activebackground="#CF1E14")
        self.button4.configure(cursor="hand2")
        self.button4.configure(foreground="#ffffff")
        self.button4.configure(background="#CF1E14")
        self.button4.configure(font="-family {Poppins SemiBold} -size 12")
        self.button4.configure(borderwidth="0")
        self.button4.configure(text="""DELETE METER""")
        self.button4.configure(command=self.delete_meter)

        self.button6 = Button(meter)
        self.button6.place(relx=0.135, rely=0.885, width=76, height=23)
        self.button6.configure(relief="flat")
        self.button6.configure(overrelief="flat")
        self.button6.configure(activebackground="#CF1E14")
        self.button6.configure(cursor="hand2")
        self.button6.configure(foreground="#ffffff")
        self.button6.configure(background="#CF1E14")
        self.button6.configure(font="-family {Poppins SemiBold} -size 12")
        self.button6.configure(borderwidth="0")
        self.button6.configure(text="""EXIT""")
        self.button6.configure(command=self.Exit)

        self.scrollbarx = Scrollbar(meter, orient=HORIZONTAL)
        self.scrollbary = Scrollbar(meter, orient=VERTICAL)
        self.tree = ttk.Treeview(meter)
        self.tree.place(relx=0.307, rely=0.203, width=880, height=550)
        self.tree.configure(
            yscrollcommand=self.scrollbary.set, xscrollcommand=self.scrollbarx.set
        )
        self.tree.configure(selectmode="extended")

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.scrollbary.configure(command=self.tree.yview)
        self.scrollbarx.configure(command=self.tree.xview)

        self.scrollbary.place(relx=0.954, rely=0.203, width=22, height=548)
        self.scrollbarx.place(relx=0.307, rely=0.924, width=884, height=22)

        self.tree.configure(
            columns=(
                "Meter ID",
                "Household ID",
                "Household owner name",
                "Month",
                "Year",
                "Meter value",
                "Consumption",
                "Payment"
            )
        )

        self.tree.heading("Meter ID", text="Meter ID", anchor=W)
        self.tree.heading("Household ID", text="Household ID", anchor=W)
        self.tree.heading("Household owner name", text="Household owner name", anchor=W)
        self.tree.heading("Month", text="Month", anchor=W)
        self.tree.heading("Year", text="Year", anchor=W)
        self.tree.heading("Meter value", text="Meter value", anchor=W)
        self.tree.heading("Consumption", text="Consumption", anchor=W)
        self.tree.heading("Payment", text="Payment", anchor=W)

        self.tree.column("#0", stretch=NO, minwidth=0, width=0)
        self.tree.column("#1", stretch=NO, minwidth=0, width=80)
        self.tree.column("#2", stretch=NO, minwidth=0, width=80)
        self.tree.column("#3", stretch=NO, minwidth=0, width=180)
        self.tree.column("#4", stretch=NO, minwidth=0, width=100)
        self.tree.column("#5", stretch=NO, minwidth=0, width=100)
        self.tree.column("#6", stretch=NO, minwidth=0, width=100)
        self.tree.column("#7", stretch=NO, minwidth=0, width=100)
        self.tree.column("#8", stretch=NO, minwidth=0, width=138)

        self.DisplayData()

    def DisplayData(self):
        cur.execute(f"""SELECT id FROM households""")
        results = cur.fetchall()
        household_ids = []
        for result in results:
            household_ids.append(result[0])
        for household_id in household_ids:
            cur.execute(f"""
            SELECT meters.id, households.id, households.owner_name, meters.`month`, meters.`year`, meters.`value`, areas.price
            FROM households
            INNER JOIN meters ON meters.household_id = households.id
            INNER JOIN areas ON households.area_id = areas.id
            WHERE households.id = {household_id}
            """)
            results = cur.fetchall()
            register_data = (results[0][0], results[0][1], results[0][2], results[0][3], results[0][4], results[0][5],
                        0, 0)
            self.tree.insert("", "end", values=(register_data))
            for i in range(1, len(results)):
                data = (results[i][0], results[i][1], results[i][2], results[i][3], results[i][4], results[i][5],
                        results[i][5] - results[i - 1][5], (results[i][5] - results[i - 1][5]) * results[i][6])
                self.tree.insert("", "end", values=(data))

    def search_meter(self):
        val = []
        for i in self.tree.get_children():
            val.append(i)
            for j in self.tree.item(i)["values"]:
                val.append(j)

        try:
            to_search = int(self.entry1.get())
        except ValueError:
            messagebox.showerror("Oops!!", "Invalid Meter ID.", parent=meter)
        else:
            for search in val:
                if search == to_search:
                    self.tree.selection_set(val[val.index(search) - 1])
                    self.tree.focus(val[val.index(search) - 1])
                    messagebox.showinfo("Success!!", "Meter ID: {} found.".format(self.entry1.get()),
                                        parent=meter)
                    break
            else:
                messagebox.showerror("Oops!!", "Meter ID: {} not found.".format(self.entry1.get()),
                                     parent=meter)

    sel = []

    def on_tree_select(self, Event):
        self.sel.clear()
        for i in self.tree.selection():
            if i not in self.sel:
                self.sel.append(i)

    def delete_meter(self):
        val = []
        to_delete = []

        if len(self.sel) != 0:
            sure = messagebox.askyesno("Confirm", "Are you sure you want to delete selected meter(s)?", parent=meter)
            if sure == True:
                for i in self.sel:
                    for j in self.tree.item(i)["values"]:
                        val.append(j)

                for j in range(len(val)):
                    if j % 8 == 0:
                        to_delete.append(val[j])

                for k in to_delete:
                    delete = "DELETE FROM meters WHERE id = ?"
                    cur.execute(delete, [k])
                    db.commit()
                    messagebox.showinfo("Success!!", "Meter(s) deleted from database.", parent=meter)
                    self.sel.clear()
                    self.tree.delete(*self.tree.get_children())
                    self.DisplayData()
        else:
            messagebox.showerror("Error!!", "Please select a meter.", parent=meter)

    def add_meter(self):
        global meter_add
        meter_add = Toplevel()
        page10 = add_meter(meter_add)
        page10.time()
        meter_add.protocol("WM_DELETE_WINDOW", self.ex)
        meter_add.mainloop()

    def ex(self):
        meter_add.destroy()
        self.tree.delete(*self.tree.get_children())
        self.DisplayData()

    def time(self):
        string = strftime("%H:%M:%S %p")
        self.clock.config(text=string)
        self.clock.after(1000, self.time)

    def Exit(self):
        sure = messagebox.askyesno("Exit", "Are you sure you want to exit?", parent=meter)
        if sure == True:
            meter.destroy()
            adm.deiconify()

    def Logout(self):
        sure = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if sure == True:
            meter.destroy()
            root.deiconify()

            page1.entry1.delete(0, END)
            page1.entry2.delete(0, END)


class add_meter:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("Add Meter")

        self.label1 = Label(meter_add)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="./images/add_meter.png")
        self.label1.configure(image=self.img)

        self.clock = Label(meter_add)
        self.clock.place(relx=0.84, rely=0.065, width=102, height=36)
        self.clock.configure(font="-family {Poppins Light} -size 12")
        self.clock.configure(foreground="#000000")
        self.clock.configure(background="#ffffff")

        self.r1 = meter_add.register(self.testint)

        self.entry1 = Entry(meter_add)
        self.entry1.place(relx=0.132, rely=0.296, width=374, height=30)
        self.entry1.configure(font="-family {Poppins} -size 12")
        self.entry1.configure(relief="flat")
        self.entry1.configure(validate="key", validatecommand=(self.r1, "%P"))

        self.entry2 = Entry(meter_add)
        self.entry2.place(relx=0.132, rely=0.413, width=374, height=30)
        self.entry2.configure(font="-family {Poppins} -size 12")
        self.entry2.configure(relief="flat")
        self.entry2.configure(validate="key", validatecommand=(self.r1, "%P"))

        self.entry4 = Entry(meter_add)
        self.entry4.place(relx=0.527, rely=0.296, width=374, height=30)
        self.entry4.configure(font="-family {Poppins} -size 12")
        self.entry4.configure(relief="flat")
        self.entry4.configure(validate="key", validatecommand=(self.r1, "%P"))

        self.entry5 = Entry(meter_add)
        self.entry5.place(relx=0.527, rely=0.413, width=374, height=30)
        self.entry5.configure(font="-family {Poppins} -size 12")
        self.entry5.configure(relief="flat")
        self.entry5.configure(validate="key", validatecommand=(self.r1, "%P"))

        self.button1 = Button(meter_add)
        self.button1.place(relx=0.408, rely=0.836, width=96, height=34)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#CF1E14")
        self.button1.configure(cursor="hand2")
        self.button1.configure(foreground="#ffffff")
        self.button1.configure(background="#CF1E14")
        self.button1.configure(font="-family {Poppins SemiBold} -size 14")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""ADD""")
        self.button1.configure(command=self.add)

        self.button2 = Button(meter_add)
        self.button2.place(relx=0.526, rely=0.836, width=86, height=34)
        self.button2.configure(relief="flat")
        self.button2.configure(overrelief="flat")
        self.button2.configure(activebackground="#CF1E14")
        self.button2.configure(cursor="hand2")
        self.button2.configure(foreground="#ffffff")
        self.button2.configure(background="#CF1E14")
        self.button2.configure(font="-family {Poppins SemiBold} -size 14")
        self.button2.configure(borderwidth="0")
        self.button2.configure(text="""CLEAR""")
        self.button2.configure(command=self.clearr)

    def testint(self, val):
        if val.isdigit():
            return True
        elif val == "":
            return True
        return False

    def time(self):
        string = strftime("%H:%M:%S %p")
        self.clock.config(text=string)
        self.clock.after(1000, self.time)

    def add(self):
        household_id = self.entry1.get()
        value = self.entry2.get()
        month = self.entry4.get()
        year = self.entry5.get()

        try:
            int(household_id)
        except ValueError:
            messagebox.showerror("Oops!", "Invalid household ID.")
        else:
            with sqlite3.connect("./Database/electric.db") as db:
                cur = db.cursor()
            cur.execute("""SELECT id FROM households""")
            results = cur.fetchall()
            household_ids = []
            for result in results:
                household_ids.append(result[0])
            if int(household_id) not in household_ids:
                messagebox.showerror("Oops!", "Household ID does not exist.", parent=hh_add)
            else:
                try:
                    int(month)
                except ValueError:
                    messagebox.showerror("Oops!", "Invalid month.")
                else:
                    if 1 <= int(month) <= 12:
                        with sqlite3.connect("./Database/electric.db") as db:
                            cur = db.cursor()
                        cur.execute(
                            f"""SELECT `month`, `year`, `value` FROM meters WHERE household_id = {household_id}""")
                        results = cur.fetchall()
                        fail = 0
                        if len(results) > 0:
                            if int(year) < results[-1][1]:
                                messagebox.showerror("Oops!",
                                                     "The time of the update must be after the previous one's!")
                                fail = 1
                            elif int(year) == results[-1][1]:
                                if int(month) <= results[-1][0]:
                                    messagebox.showerror("Oops!",
                                                         "The time of the update must be after the previous one's!")
                                    fail = 1
                                elif int(month) - results[-1][0] > 1:
                                    messagebox.showerror("Oops!",
                                                         "The time interval between 2 updates must be 1 month!")
                                    fail = 1
                            else:
                                if int(year) - results[-1][1] > 1:
                                    messagebox.showerror("Oops!",
                                                         "The time interval between 2 updates must be 1 month!")
                                    fail = 1
                                elif int(month) != 1 or results[-1][2] != 12:
                                    messagebox.showerror("Oops!",
                                                         "The time interval between 2 updates must be 1 month!")
                                    fail = 1
                            if int(value) <= results[-1][2]:
                                messagebox.showerror("Oops!",
                                                     "The value of the update must be larger than the previous one's!")
                                fail = 1
                        if fail == 0:
                            insert = (
                                "INSERT INTO meters (household_id, `month`, `year`, `value`) VALUES (?,?,?,?)"
                            )
                            cur.execute(insert, [household_id, month, year, value])
                            db.commit()

                            cur.execute(
                                f"""SELECT `value` FROM meters WHERE household_id = {household_id}"""
                            )
                            results = cur.fetchall()
                            total_consumption = 0
                            for result in results:
                                total_consumption += result[0]
                            monthly_consumption = round((float(total_consumption) / float(len(results) - 1)) * 10) / 10.0
                            # Update the monthly consumption in households
                            cur.execute(
                                f"""UPDATE households
                                                    SET monthly_consumption = {float(monthly_consumption)}
                                                    WHERE id = {household_id}"""
                            )
                            # Commit changes
                            db.commit()

                            messagebox.showinfo("Success!!", "Meter data successfully added in database.", parent=meter_add)
                            self.clearr()
                    else:
                        messagebox.showerror("Oops!", "Invalid month.")

    def clearr(self):
        self.entry1.delete(0, END)
        self.entry2.delete(0, END)
        self.entry4.delete(0, END)
        self.entry5.delete(0, END)

if __name__ == '__main__':
    on_start()
    page1 = login_page(root)
    root.bind("<Return>", login_page.login)
    root.mainloop()