import tkinter as tk
from sqlite3 import Error
import sqlite3
from tkinter import ttk
from tkinter.ttk import Progressbar
from tkinter import messagebox
import math
import tkinter.font as font


class Household:
    def __init__(self, id, name, address, area, payment_status=0, monthly_consumption=0):
        self.__id = id
        self.__name = name
        self.__address = address
        self.__payment_status = payment_status
        self.__area = area
        self.__monthly_consumption = monthly_consumption

    def get_hid(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_address(self):
        return self.__address

    def get_payment_status(self):
        return self.__payment_status

    def get_area(self):
        return self.__area

    def get_monthly_consumption(self):
        return self.__monthly_consumption

    def set_id(self, id):
        self.__id = id

    def set_name(self, name):
        self.__name = name

    def set_address(self, address):
        self.__address = address

    def set_payment_status(self, payment_status):
        self.__payment_status = payment_status

    def set_area(self, area):
        self.__area = area

    def set_monthly_consumption(self, monthly_consumption):
        self.__monthly_consumption = monthly_consumption


class Meter:
    def __init__(self, id, hid, register_year, register_month):
        self.__id = id
        self.__hid = hid
        self.__measurements = [(register_year, register_month, 0)]
        self.__total_months = 0
        self.__total_values = 0

    def get_id(self):
        return self.__id

    def get_hid(self):
        return self.__hid

    def get_total_months(self):
        return self.__total_months

    def get_total_values(self):
        return self.__total_values

    def add_measurements(self, year, month, value):
        self.__measurements.append((year, month, value))
        if self.__measurements[-1][0] == self.__measurements[-2][0]:
            self.__total_months += self.__measurements[-1][1] - self.__measurements[-2][1]
        elif self.__measurements[-1][0] > self.__measurements[-2][0]:
            self.__total_months += self.__measurements[-1][1] + (12 - self.__measurements[-2][1])
        else:
            print("The updated time must be later than the previous one")
        self.__total_values += value

    def get_measurements(self):
        return self.__measurements


class Area:
    def __init__(self, id, price):
        self.__id = id
        self.__price = price

    def set_id(self, id):
        self.__id = id

    def get_id(self):
        return self.__id

    def set_price(self, price):
        self.__price = price

    def get_price(self):
        return self.__price


class Engine:
    number_of_areas = 0
    number_of_households = 0

    # Create the database electric.db (if not existed) or connect to it (if existed)
    conn = sqlite3.connect('electric.db')
    # Create a cursor
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = ON")
    # Create tables
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

    def create_tables(self):
        self.c.execute(self.create_areas_table)
        self.c.execute(self.create_households_table)
        self.c.execute(self.create_meters_table)

    def load_number_of_areas(self):
        self.c.execute("""SELECT * FROM areas""")
        results = self.c.fetchall()
        self.number_of_areas = len(results)

    def load_number_of_households(self):
        self.c.execute("""SELECT * FROM households""")
        results = self.c.fetchall()
        self.number_of_households = len(results)

    def on_start(self):
        self.create_tables()
        self.load_number_of_areas()
        self.load_number_of_households()

    def input_areas(self, parent):
        try:
            sub = tk.Toplevel(master=parent)
            sub.title("Input Areas")
            sub.resizable(height=False, width=False)

            # Create text entries
            price_ent = tk.Entry(sub, width=30)
            price_ent.grid(row=1, column=1, padx=20)

            # Create text labels
            id_lbl = tk.Label(sub, text=f"Area {self.number_of_areas + 1}: ")
            id_lbl.grid(row=0, column=0, columnspan=2)
            price_lbl = tk.Label(sub, text="Corresponding price: ")
            price_lbl.grid(row=1, column=0)

            # Create Submit Function for Database:
            def submit():
                try:
                    # Create the electric.db or connect to it
                    conn = sqlite3.connect('electric.db')
                    # Create cursor
                    c = conn.cursor()
                    c.execute("PRAGMA foreign_keys = ON")
                    # Insert into table
                    c.execute(
                        """INSERT INTO areas (price) VALUES (:price)""",
                        {
                            'price': price_ent.get()
                        }
                    )
                    self.number_of_areas += 1
                    id_lbl["text"] = f"Area {self.number_of_areas + 1}: "
                    # Clear the entries
                    price_ent.delete(0, tk.END)
                    # Commit changes
                    conn.commit()
                    # Close connection
                    conn.close()
                except Error as e:
                    return e

            # Create Submit Button
            submit_btn = tk.Button(sub, text="Add Record to Database", command=submit)
            submit_btn.grid(row=2, column=0, columnspan=2, ipadx=5, ipady=5, pady=5, padx=5)
        except Error as e:
            return e

    def input_households(self, parent):
        try:
            sub = tk.Toplevel(master=parent)
            sub.title("Input Households")
            sub.resizable(height=False, width=False)

            # Create text entries
            name_ent = tk.Entry(sub, width=30)
            name_ent.grid(row=1, column=1, padx=20)
            address_ent = tk.Entry(sub, width=30)
            address_ent.grid(row=2, column=1, padx=20)
            phone_number_ent = tk.Entry(sub, width=30)
            phone_number_ent.grid(row=3, column=1, padx=20)
            area_ent = tk.Entry(sub, width=30)
            area_ent.grid(row=4, column=1, padx=20)
            register_month_ent = tk.Entry(sub, width=30)
            register_month_ent.grid(row=5, column=1, padx=20)
            register_year_ent = tk.Entry(sub, width=30)
            register_year_ent.grid(row=6, column=1, padx=20)

            # Create text labels
            id_lbl = tk.Label(sub, text=f"Household {self.number_of_households + 1}: ")
            id_lbl.grid(row=0, column=0, columnspan=2)
            name_lbl = tk.Label(sub, text="Owner's name: ")
            name_lbl.grid(row=1, column=0)
            address_lbl = tk.Label(sub, text="Address: ")
            address_lbl.grid(row=2, column=0)
            phone_number_lbl = tk.Label(sub, text="Phone number: ")
            phone_number_lbl.grid(row=3, column=0)
            area_lbl = tk.Label(sub, text="Area: ")
            area_lbl.grid(row=4, column=0)
            register_month_lbl = tk.Label(sub, text="Register month: ")
            register_month_lbl.grid(row=5, column=0)
            register_year_lbl = tk.Label(sub, text="Register year: ")
            register_year_lbl.grid(row=6, column=0)

            # Create Submit Function for Database:
            def submit():
                try:
                    # Create the electric.db or connect to it
                    conn = sqlite3.connect('electric.db')
                    # Create cursor
                    c = conn.cursor()
                    c.execute("PRAGMA foreign_keys = ON")
                    # Check if areas exist:
                    c.execute("""SELECT * FROM areas""")
                    results = c.fetchall()
                    if len(results) == 0:
                        messagebox.showerror(message="You have to input areas first!")
                        sub.destroy()
                    # Check if area_id exist:
                    c.execute("""SELECT id FROM areas""")
                    results = c.fetchall()
                    area_ids = []
                    for result in results:
                        area_ids.append(result[0])
                    if int(area_ent.get()) not in area_ids:
                        messagebox.showerror(message="Area ID does not exist")
                        self.input_households(parent)
                        sub.destroy()
                    if int(register_month_ent.get()) < 1 or int(register_month_ent.get()) > 12:
                        messagebox.showerror(message="Invalid register month")
                        self.input_households(parent)
                        sub.destroy()
                    try:
                        int(phone_number_ent.get())
                    except ValueError:
                        messagebox.showerror(message="Invalid phone number")
                        self.input_households(parent)
                        sub.destroy()

                    # Insert into tables
                    c.execute(
                        """INSERT INTO households (owner_name, address, phone_number, payment_status, area_id, monthly_consumption) VALUES (:owner_name, :address, :phone_number, :payment_status, :area_id, :monthly_consumption)""",
                        {
                            'owner_name': name_ent.get(),
                            'address': address_ent.get(),
                            'phone_number': phone_number_ent.get(),
                            'payment_status': 0,
                            'area_id': area_ent.get(),
                            'monthly_consumption': 0
                        }
                    )
                    # Commit changes on households table
                    conn.commit()
                    self.number_of_households += 1
                    id_lbl["text"] = f"Household {self.number_of_households + 1}: "
                    c.execute("""SELECT id FROM households""")
                    results = c.fetchall()
                    household_id = results[-1][0]
                    c.execute(
                        f"""INSERT INTO meters (household_id, `month`, `year`, `value`) VALUES ({household_id}, {register_month_ent.get()}, {register_year_ent.get()}, 0)"""
                    )
                    # Commit changes on meters table
                    conn.commit()
                    # Clear the entries
                    name_ent.delete(0, tk.END)
                    phone_number_ent.delete(0, tk.END)
                    address_ent.delete(0, tk.END)
                    area_ent.delete(0, tk.END)
                    register_month_ent.delete(0, tk.END)
                    register_year_ent.delete(0, tk.END)
                    # Commit changes on meters table
                    conn.commit()
                    # Close connection
                    conn.close()
                except Error as e:
                    return e

            # Create Submit Button
            submit_btn = tk.Button(sub, text="Add Record to Database", command=submit)
            submit_btn.grid(row=7, column=0, columnspan=2, ipadx=5, ipady=5, pady=5, padx=5)
        except Error as e:
            return e

    def update_household_information_with_id(self, parent, household_id):
        try:
            sub = tk.Toplevel(master=parent)
            sub.title(f"Update household {household_id}")
            sub.resizable(height=False, width=False)

            # Create text entries
            name_ent = tk.Entry(sub, width=30)
            name_ent.grid(row=1, column=1, padx=20)
            address_ent = tk.Entry(sub, width=30)
            address_ent.grid(row=2, column=1, padx=20)
            phone_number_ent = tk.Entry(sub, width=30)
            phone_number_ent.grid(row=3, column=1, padx=20)
            area_ent = tk.Entry(sub, width=30)
            area_ent.grid(row=4, column=1, padx=20)

            # Create text labels
            id_lbl = tk.Label(sub, text=f"Updating Household {household_id}: ")
            id_lbl.grid(row=0, column=0, columnspan=2)
            name_lbl = tk.Label(sub, text="Owner's name: ")
            name_lbl.grid(row=1, column=0)
            address_lbl = tk.Label(sub, text="Address: ")
            address_lbl.grid(row=2, column=0)
            phone_number_lbl = tk.Label(sub, text="Phone number: ")
            phone_number_lbl.grid(row=3, column=0)
            area_lbl = tk.Label(sub, text="Area: ")
            area_lbl.grid(row=4, column=0)

            # Create Submit Function for Database:
            def submit():
                try:
                    # Create the electric.db or connect to it
                    conn = sqlite3.connect('electric.db')
                    # Create cursor
                    c = conn.cursor()
                    c.execute("PRAGMA foreign_keys = ON")
                    # Check if area_id exist:
                    c.execute("""SELECT id FROM areas""")
                    results = c.fetchall()
                    area_ids = []
                    for result in results:
                        area_ids.append(result[0])
                    if int(area_ent.get()) not in area_ids:
                        messagebox.showerror(message="Area ID does not exist")
                        self.update_household_information_with_id(parent, household_id)
                        sub.destroy()
                    # Insert into table
                    c.execute(
                        f"""UPDATE households 
                        SET owner_name = :owner_name,
                          address = :address,
                          phone_number = :phone_number, 
                          area_id = :area_id
                        WHERE id = {household_id}""",
                        {
                            'owner_name': name_ent.get(),
                            'address': address_ent.get(),
                            'phone_number': phone_number_ent.get(),
                            'area_id': area_ent.get()
                        }
                    )
                    # Commit changes
                    conn.commit()
                    # Close connection
                    conn.close()
                    # Close sub-window
                    sub.destroy()
                except Error as e:
                    return e

            # Create Submit Button
            submit_btn = tk.Button(sub, text="Update Record to Database", command=submit)
            submit_btn.grid(row=5, column=0, columnspan=2, ipadx=5, ipady=5, pady=5, padx=5)
        except Error as e:
            return e

    def update_household_information(self, parent):
        try:
            sub = tk.Toplevel(master=parent)
            sub.title(f"Update household")
            sub.resizable(height=False, width=False)

            # Create text entries
            id_ent = tk.Entry(sub, width=30)
            id_ent.grid(row=0, column=1, padx=20)

            # Create text labels
            id_lbl = tk.Label(sub, text="Enter the ID of the household to be updated: ")
            id_lbl.grid(row=0, column=0)

            # Create Submit Function for Database:
            def submit():
                try:
                    # Create the electric.db or connect to it
                    conn = sqlite3.connect('electric.db')
                    # Create cursor
                    c = conn.cursor()
                    c.execute("PRAGMA foreign_keys = ON")
                    # Check if household_id exist:
                    c.execute("""SELECT id FROM households""")
                    results = c.fetchall()
                    household_ids = []
                    for result in results:
                        household_ids.append(result[0])
                    if int(id_ent.get()) not in household_ids:
                        messagebox.showerror(message="Household ID does not exist")
                        self.update_household_information(parent)
                        sub.destroy()
                    else:
                        self.update_household_information_with_id(parent, int(id_ent.get()))
                        sub.destroy()
                except Error as e:
                    return e

            # Create Submit Button
            submit_btn = tk.Button(sub, text="Submit", command=submit)
            submit_btn.grid(row=5, column=0, columnspan=2, ipadx=5, ipady=5, pady=5, padx=5)
        except Error as e:
            return e

    def delete_household(self, parent):
        try:
            sub = tk.Toplevel(master=parent)
            sub.title(f"Delete household")
            sub.resizable(height=False, width=False)

            # Create text entries
            id_ent = tk.Entry(sub, width=30)
            id_ent.grid(row=0, column=1, padx=20)

            # Create text labels
            id_lbl = tk.Label(sub, text="Enter the ID of the household to be deleted: ")
            id_lbl.grid(row=0, column=0)

            # Create Delete Function for Database:
            def delete():
                try:
                    # Create the electric.db or connect to it
                    conn = sqlite3.connect('electric.db')
                    # Create cursor
                    c = conn.cursor()
                    c.execute("PRAGMA foreign_keys = ON")
                    # Check if household_id exist:
                    c.execute("""SELECT id FROM households""")
                    results = c.fetchall()
                    household_ids = []
                    for result in results:
                        household_ids.append(result[0])
                    if int(id_ent.get()) not in household_ids:
                        messagebox.showerror(message="Household ID does not exist")
                        self.delete_household(parent)
                        sub.destroy()
                    else:
                        c.execute(f"""DELETE FROM households WHERE id = {int(id_ent.get())}""")
                        # Commit changes
                        conn.commit()
                        # Close connection
                        conn.close()
                        # Close the sub-window
                        sub.destroy()
                except Error as e:
                    return e

            # Create Delete Button
            submit_btn = tk.Button(sub, text="Delete", command=delete)
            submit_btn.grid(row=5, column=0, columnspan=2, ipadx=5, ipady=5, pady=5, padx=5)

        except Error as e:
            return e

    def list_areas(self, parent):
        try:
            sub = tk.Toplevel(master=parent)
            sub.title(f"Listing areas:")
            sub.resizable(height=False, width=False)

            title_lbl = tk.Label(sub, text="All areas:")
            title_lbl.grid(row=0, column=0, columnspan=2)

            self.c.execute("""SELECT * FROM areas""")
            results = self.c.fetchall()
            id_title_lbl = tk.Label(sub, text="Area ID", borderwidth=1, relief="solid")
            price_title_lbl = tk.Label(sub, text="Price", borderwidth=1, relief="solid")
            id_title_lbl.grid(row=1, column=0, sticky="nsew")
            price_title_lbl.grid(row=1, column=1, sticky="nsew")
            for i in range(len(results)):
                id_lbl = tk.Label(sub, text=f"{results[i][0]}", borderwidth=1, relief="solid")
                price_lbl = tk.Label(sub, text=f"{results[i][1]}", borderwidth=1, relief="solid")
                id_lbl.grid(row=i + 2, column=0, sticky="nsew")
                price_lbl.grid(row=i + 2, column=1, sticky="nsew")
        except Error as e:
            return e

    def list_households(self, parent):
        try:
            sub = tk.Toplevel(master=parent)
            sub.title(f"Listing households:")
            sub.resizable(height=False, width=False)

            title_lbl = tk.Label(sub, text="All households:")
            title_lbl.grid(row=0, column=0, columnspan=7)
            self.c.execute("""SELECT * FROM households""")
            results = self.c.fetchall()
            id_title_lbl = tk.Label(sub, text="ID", borderwidth=1, relief="solid")
            name_title_lbl = tk.Label(sub, text="Household Owner Name", borderwidth=1, relief="solid")
            address_title_lbl = tk.Label(sub, text="Address", borderwidth=1, relief="solid")
            phone_number_title_lbl = tk.Label(sub, text="Phone number", borderwidth=1, relief="solid")
            payment_status_title_lbl = tk.Label(sub, text="Payment Status", borderwidth=1, relief="solid")
            area_id_title_lbl = tk.Label(sub, text="Area ID", borderwidth=1, relief="solid")
            monthly_consumption_title_lbl = tk.Label(sub, text="Monthly consumption", borderwidth=1, relief="solid")
            id_title_lbl.grid(row=1, column=0, sticky="nsew")
            name_title_lbl.grid(row=1, column=1, sticky="nsew")
            address_title_lbl.grid(row=1, column=2, sticky="nsew")
            phone_number_title_lbl.grid(row=1, column=3, sticky="nsew")
            payment_status_title_lbl.grid(row=1, column=4, sticky="nsew")
            area_id_title_lbl.grid(row=1, column=5, sticky="nsew")
            monthly_consumption_title_lbl.grid(row=1, column=6, sticky="nsew")
            for i in range(len(results)):
                id_lbl = tk.Label(sub, text=f"{results[i][0]}", borderwidth=1, relief="solid")
                name_lbl = tk.Label(sub, text=f"{results[i][1]}", borderwidth=1, relief="solid")
                address_lbl = tk.Label(sub, text=f"{results[i][2]}", borderwidth=1, relief="solid")
                phone_number_lbl = tk.Label(sub, text=f"{results[i][3]}", borderwidth=1, relief="solid")
                payment_status_lbl = tk.Label(sub, text=f"{results[i][4]}", borderwidth=1, relief="solid")
                area_id_lbl = tk.Label(sub, text=f"{results[i][5]}", borderwidth=1, relief="solid")
                monthly_consumption_lbl = tk.Label(sub, text=f"{results[i][6]}", borderwidth=1, relief="solid")
                id_lbl.grid(row=i + 2, column=0, sticky="nsew")
                name_lbl.grid(row=i + 2, column=1, sticky="nsew")
                address_lbl.grid(row=i + 2, column=2, sticky="nsew")
                phone_number_lbl.grid(row=i + 2, column=3, sticky="nsew")
                payment_status_lbl.grid(row=i + 2, column=4, sticky="nsew")
                area_id_lbl.grid(row=i + 2, column=5, sticky="nsew")
                monthly_consumption_lbl.grid(row=i + 2, column=6, sticky="nsew")
        except Error as e:
            return e

    def update_meter_information_with_id(self, parent, household_id):
        try:
            sub = tk.Toplevel(master=parent)
            sub.title(f"Update meter of household {household_id}")
            sub.resizable(height=False, width=False)

            # Create text entries
            month_ent = tk.Entry(sub, width=30)
            month_ent.grid(row=1, column=1, padx=20)
            year_ent = tk.Entry(sub, width=30)
            year_ent.grid(row=2, column=1, padx=20)
            value_ent = tk.Entry(sub, width=30)
            value_ent.grid(row=3, column=1, padx=20)

            # Create text labels
            id_lbl = tk.Label(sub, text=f"Updating meter of household {household_id}: ")
            id_lbl.grid(row=0, column=0, columnspan=2)
            month_lbl = tk.Label(sub, text="Month: ")
            month_lbl.grid(row=1, column=0)
            year_lbl = tk.Label(sub, text="Year: ")
            year_lbl.grid(row=2, column=0)
            value_lbl = tk.Label(sub, text="Value: ")
            value_lbl.grid(row=3, column=0)

            # Create Submit Function for Database:
            def submit():
                try:
                    # Create the electric.db or connect to it
                    conn = sqlite3.connect('electric.db')
                    # Create cursor
                    c = conn.cursor()
                    c.execute("PRAGMA foreign_keys = ON")
                    # Check if area_id exist:
                    c.execute(f"""SELECT * FROM meters WHERE household_id = {household_id}""")
                    results = c.fetchall()
                    if len(results) > 0:
                        if int(month_ent.get()) < 1 or int(month_ent.get()) > 12:
                            messagebox.showerror(message="Invalid register month")
                            self.update_meter_information_with_id(parent, household_id)
                            sub.destroy()
                        if int(year_ent.get()) < results[-1][3]:
                            messagebox.showerror(message="The time of the update must be after the previous one's!")
                            self.update_meter_information_with_id(parent, household_id)
                            sub.destroy()
                        elif int(year_ent.get()) == results[-1][3]:
                            if int(month_ent.get()) <= results[-1][2]:
                                messagebox.showerror(message="The time of the update must be after the previous one's!")
                                self.update_meter_information_with_id(parent, household_id)
                                sub.destroy()
                            elif int(month_ent.get()) - results[-1][2] > 2:
                                messagebox.showerror(message="The maximum interval of time between 2 updates is 2 months!")
                                self.update_meter_information_with_id(parent, household_id)
                                sub.destroy()
                        else:
                            if int(month_ent.get()) + (12 - results[-1][2]) > 2:
                                messagebox.showerror(
                                    message="The maximum interval of time between 2 updates is 2 months!")
                                self.update_meter_information_with_id(parent, household_id)
                                sub.destroy()
                        if int(value_ent.get()) <= results[-1][4]:
                            messagebox.showerror(
                                message="The value of the update must be larger than the previous one's!")
                            self.update_meter_information_with_id(parent, household_id)
                            sub.destroy()
                    # Insert into table meters
                    c.execute(
                        f"""INSERT INTO meters (household_id, `month`, `year`, `value`) VALUES ({household_id}, {month_ent.get()}, {year_ent.get()}, {value_ent.get()})"""
                    )
                    # Commit changes
                    conn.commit()
                    # Re-calculate the average consumption after a meter is updated
                    c.execute(
                        f"""SELECT `value` FROM meters WHERE household_id = {household_id}"""
                    )
                    results = c.fetchall()
                    total_consumption = 0
                    for result in results:
                        total_consumption += result[0]
                    monthly_consumption = round((float(total_consumption) / float(len(results) - 1)) * 10) / 10.0
                    # Update the monthly consumption in households
                    c.execute(
                        f"""UPDATE households
                        SET monthly_consumption = {float(monthly_consumption)}
                        WHERE id = {household_id}"""
                    )
                    # Commit changes
                    conn.commit()
                    # Close connection
                    conn.close()
                    # Close sub-window
                    sub.destroy()
                except Error as e:
                    return e

            # Create Submit Button
            submit_btn = tk.Button(sub, text="Update Record to Database", command=submit)
            submit_btn.grid(row=4, column=0, columnspan=2, ipadx=5, ipady=5, pady=5, padx=5)
        except Error as e:
            return e

    def update_meter_information(self, parent):
        try:
            sub = tk.Toplevel(master=parent)
            sub.title(f"Update meter")
            sub.resizable(height=False, width=False)

            # Create text entries
            id_ent = tk.Entry(sub, width=30)
            id_ent.grid(row=0, column=1, padx=20)

            # Create text labels
            id_lbl = tk.Label(sub, text="Enter the household ID of the meter to be updated: ")
            id_lbl.grid(row=0, column=0)

            # Create Submit Function for Database:
            def submit():
                try:
                    # Create the electric.db or connect to it
                    conn = sqlite3.connect('electric.db')
                    # Create cursor
                    c = conn.cursor()
                    c.execute("PRAGMA foreign_keys = ON")
                    # Check if household_id exist:
                    c.execute("""SELECT id FROM households""")
                    results = c.fetchall()
                    household_ids = []
                    for result in results:
                        household_ids.append(result[0])
                    if int(id_ent.get()) not in household_ids:
                        messagebox.showerror(message="Household ID does not exist")
                        self.update_household_information(parent)
                        sub.destroy()
                    else:
                        self.update_meter_information_with_id(parent, int(id_ent.get()))
                        sub.destroy()
                except Error as e:
                    return e

            # Create Submit Button
            submit_btn = tk.Button(sub, text="Submit", command=submit)
            submit_btn.grid(row=5, column=0, columnspan=2, ipadx=5, ipady=5, pady=5, padx=5)
        except Error as e:
            return e

    def update_payment_status_with_id(self, parent, household_id):
        try:
            sub = tk.Toplevel(master=parent)
            sub.title(f"Update payment status of household {household_id}")
            sub.resizable(height=False, width=False)

            # Create the electric.db or connect to it
            conn = sqlite3.connect('electric.db')
            # Create cursor
            c = conn.cursor()
            c.execute("PRAGMA foreign_keys = ON")
            # Check if area_id exist:
            c.execute(f"""SELECT payment_status FROM households WHERE id = {household_id}""")
            results = c.fetchall()
            current_payment_status = results[0][0]

            # Create text entries
            new_payment_status_ent = tk.Entry(sub, width=30)
            new_payment_status_ent.grid(row=1, column=1, padx=20)

            # Create text labels
            id_lbl = tk.Label(sub, text=f"Current payment status of household {household_id}: {current_payment_status}")
            id_lbl.grid(row=0, column=0, columnspan=2)
            new_payment_status_lbl = tk.Label(sub, text="Enter updated payment status: ")
            new_payment_status_lbl.grid(row=1, column=0)
            explain_lbl = tk.Label(sub,
                                   text="Payment status is the number of months that the household have not paid the bills (an integer from 0 to 2)")
            explain_lbl.grid(row=2, column=0, columnspan=2)
            explain_lbl = tk.Label(sub,
                                   text="Any household that have not paid the bills for 2 months will be deleted from the system")
            explain_lbl.grid(row=3, column=0, columnspan=2)

            # Create Submit Function for Database:
            def submit():
                try:
                    # Create the electric.db or connect to it
                    conn = sqlite3.connect('electric.db')
                    # Create cursor
                    c = conn.cursor()
                    c.execute("PRAGMA foreign_keys = ON")
                    if int(new_payment_status_ent.get()) > 2 or int(new_payment_status_ent.get()) < 0:
                        messagebox.showerror(message="Invalid payment status")
                        self.update_payment_status_with_id(parent, household_id)
                        sub.destroy()
                    # Insert into table
                    c.execute(
                        f"""UPDATE households 
                        SET payment_status = {int(new_payment_status_ent.get())}
                        WHERE id = {household_id}"""
                    )
                    # Commit changes
                    conn.commit()
                    # Close connection
                    conn.close()
                    # Close sub-window
                    sub.destroy()
                except Error as e:
                    return e

            # Create Submit Button
            submit_btn = tk.Button(sub, text="Update Record to Database", command=submit)
            submit_btn.grid(row=5, column=0, columnspan=2, ipadx=5, ipady=5, pady=5, padx=5)
        except Error as e:
            return e

    def update_payment_status(self, parent):
        try:
            sub = tk.Toplevel(master=parent)
            sub.title(f"Update payment status")
            sub.resizable(height=False, width=False)

            # Create text entries
            id_ent = tk.Entry(sub, width=30)
            id_ent.grid(row=0, column=1, padx=20)

            # Create text labels
            id_lbl = tk.Label(sub, text="Enter the ID of the household whose payment status to be updated: ")
            id_lbl.grid(row=0, column=0)

            # Create Submit Function for Database:
            def submit():
                try:
                    # Create the electric.db or connect to it
                    conn = sqlite3.connect('electric.db')
                    # Create cursor
                    c = conn.cursor()
                    c.execute("PRAGMA foreign_keys = ON")
                    # Check if household_id exist:
                    c.execute("""SELECT id FROM households""")
                    results = c.fetchall()
                    household_ids = []
                    for result in results:
                        household_ids.append(result[0])
                    if int(id_ent.get()) not in household_ids:
                        messagebox.showerror(message="Household ID does not exist")
                        self.update_household_information(parent)
                        sub.destroy()
                    else:
                        self.update_payment_status_with_id(parent, int(id_ent.get()))
                        sub.destroy()
                except Error as e:
                    return e

            # Create Submit Button
            submit_btn = tk.Button(sub, text="Submit", command=submit)
            submit_btn.grid(row=5, column=0, columnspan=2, ipadx=5, ipady=5, pady=5, padx=5)
        except Error as e:
            return e

    def auto_increase_payment_status(self):
        try:
            # Create the electric.db or connect to it
            conn = sqlite3.connect('electric.db')
            # Create cursor
            c = conn.cursor()
            c.execute("PRAGMA foreign_keys = ON")
            c.execute(f"""UPDATE households SET payment_status = payment_status + 1""")
            # Commit changes made by updating
            conn.commit()
            c.execute(f"""DELETE FROM households WHERE payment_status > 2""")
            # Commit changes made by deleting
            conn.commit()
            # Close connection
            conn.close()
        except Error as e:
            return e

    def list_paid_household(self, parent):
        try:
            sub = tk.Toplevel(master=parent)
            sub.title(f"Listing paid households:")
            sub.resizable(height=False, width=False)

            title_lbl = tk.Label(sub, text="All paid households:")
            title_lbl.grid(row=0, column=0, columnspan=7)
            self.c.execute("""SELECT * FROM households WHERE payment_status = 0""")
            results = self.c.fetchall()
            id_title_lbl = tk.Label(sub, text="ID", borderwidth=1, relief="solid")
            name_title_lbl = tk.Label(sub, text="Household Owner Name", borderwidth=1, relief="solid")
            address_title_lbl = tk.Label(sub, text="Address", borderwidth=1, relief="solid")
            phone_number_title_lbl = tk.Label(sub, text="Phone number", borderwidth=1, relief="solid")
            payment_status_title_lbl = tk.Label(sub, text="Payment Status", borderwidth=1, relief="solid")
            area_id_title_lbl = tk.Label(sub, text="Area ID", borderwidth=1, relief="solid")
            monthly_consumption_title_lbl = tk.Label(sub, text="Monthly consumption", borderwidth=1, relief="solid")
            id_title_lbl.grid(row=1, column=0, sticky="nsew")
            name_title_lbl.grid(row=1, column=1, sticky="nsew")
            address_title_lbl.grid(row=1, column=2, sticky="nsew")
            phone_number_title_lbl.grid(row=1, column=3, sticky="nsew")
            payment_status_title_lbl.grid(row=1, column=4, sticky="nsew")
            area_id_title_lbl.grid(row=1, column=5, sticky="nsew")
            monthly_consumption_title_lbl.grid(row=1, column=6, sticky="nsew")
            for i in range(len(results)):
                id_lbl = tk.Label(sub, text=f"{results[i][0]}", borderwidth=1, relief="solid")
                name_lbl = tk.Label(sub, text=f"{results[i][1]}", borderwidth=1, relief="solid")
                address_lbl = tk.Label(sub, text=f"{results[i][2]}", borderwidth=1, relief="solid")
                phone_number_lbl = tk.Label(sub, text=f"{results[i][3]}", borderwidth=1, relief="solid")
                payment_status_lbl = tk.Label(sub, text=f"{results[i][4]}", borderwidth=1, relief="solid")
                area_id_lbl = tk.Label(sub, text=f"{results[i][5]}", borderwidth=1, relief="solid")
                monthly_consumption_lbl = tk.Label(sub, text=f"{results[i][6]}", borderwidth=1, relief="solid")
                id_lbl.grid(row=i + 2, column=0, sticky="nsew")
                name_lbl.grid(row=i + 2, column=1, sticky="nsew")
                address_lbl.grid(row=i + 2, column=2, sticky="nsew")
                phone_number_lbl.grid(row=i + 2, column=3, sticky="nsew")
                payment_status_lbl.grid(row=i + 2, column=4, sticky="nsew")
                area_id_lbl.grid(row=i + 2, column=5, sticky="nsew")
                monthly_consumption_lbl.grid(row=i + 2, column=6, sticky="nsew")
        except Error as e:
            return e

    def list_not_yet_paid_household(self, parent):
        try:
            sub = tk.Toplevel(master=parent)
            sub.title(f"Listing paid households:")
            sub.resizable(height=False, width=False)

            title_lbl = tk.Label(sub, text="All paid households:")
            title_lbl.grid(row=0, column=0, columnspan=7)
            self.c.execute("""SELECT * FROM households WHERE payment_status > 0""")
            results = self.c.fetchall()
            id_title_lbl = tk.Label(sub, text="ID", borderwidth=1, relief="solid")
            name_title_lbl = tk.Label(sub, text="Household Owner Name", borderwidth=1, relief="solid")
            address_title_lbl = tk.Label(sub, text="Address", borderwidth=1, relief="solid")
            phone_number_title_lbl = tk.Label(sub, text="Phone number", borderwidth=1, relief="solid")
            payment_status_title_lbl = tk.Label(sub, text="Payment Status", borderwidth=1, relief="solid")
            area_id_title_lbl = tk.Label(sub, text="Area ID", borderwidth=1, relief="solid")
            monthly_consumption_title_lbl = tk.Label(sub, text="Monthly consumption", borderwidth=1, relief="solid")
            id_title_lbl.grid(row=1, column=0, sticky="nsew")
            name_title_lbl.grid(row=1, column=1, sticky="nsew")
            address_title_lbl.grid(row=1, column=2, sticky="nsew")
            phone_number_title_lbl.grid(row=1, column=3, sticky="nsew")
            payment_status_title_lbl.grid(row=1, column=4, sticky="nsew")
            area_id_title_lbl.grid(row=1, column=5, sticky="nsew")
            monthly_consumption_title_lbl.grid(row=1, column=6, sticky="nsew")
            for i in range(len(results)):
                id_lbl = tk.Label(sub, text=f"{results[i][0]}", borderwidth=1, relief="solid")
                name_lbl = tk.Label(sub, text=f"{results[i][1]}", borderwidth=1, relief="solid")
                address_lbl = tk.Label(sub, text=f"{results[i][2]}", borderwidth=1, relief="solid")
                phone_number_lbl = tk.Label(sub, text=f"{results[i][3]}", borderwidth=1, relief="solid")
                payment_status_lbl = tk.Label(sub, text=f"{results[i][4]}", borderwidth=1, relief="solid")
                area_id_lbl = tk.Label(sub, text=f"{results[i][5]}", borderwidth=1, relief="solid")
                monthly_consumption_lbl = tk.Label(sub, text=f"{results[i][6]}", borderwidth=1, relief="solid")
                id_lbl.grid(row=i + 2, column=0, sticky="nsew")
                name_lbl.grid(row=i + 2, column=1, sticky="nsew")
                address_lbl.grid(row=i + 2, column=2, sticky="nsew")
                phone_number_lbl.grid(row=i + 2, column=3, sticky="nsew")
                payment_status_lbl.grid(row=i + 2, column=4, sticky="nsew")
                area_id_lbl.grid(row=i + 2, column=5, sticky="nsew")
                monthly_consumption_lbl.grid(row=i + 2, column=6, sticky="nsew")
        except Error as e:
            return e

    def display_household_information_with_id(self, parent, household_id):
        try:
            sub = tk.Toplevel(master=parent)
            sub.title(f"Information of Household {household_id}:")
            sub.resizable(height=False, width=False)

            title_lbl = tk.Label(sub, text=f"Information of Household {household_id}:")
            title_lbl.grid(row=0, column=0, columnspan=7)
            self.c.execute(f"""SELECT * FROM households WHERE id = {household_id}""")
            results = self.c.fetchall()
            id_title_lbl = tk.Label(sub, text="ID", borderwidth=1, relief="solid")
            name_title_lbl = tk.Label(sub, text="Household Owner Name", borderwidth=1, relief="solid")
            address_title_lbl = tk.Label(sub, text="Address", borderwidth=1, relief="solid")
            phone_number_title_lbl = tk.Label(sub, text="Phone number", borderwidth=1, relief="solid")
            payment_status_title_lbl = tk.Label(sub, text="Payment Status", borderwidth=1, relief="solid")
            area_id_title_lbl = tk.Label(sub, text="Area ID", borderwidth=1, relief="solid")
            monthly_consumption_title_lbl = tk.Label(sub, text="Monthly consumption", borderwidth=1, relief="solid")
            id_title_lbl.grid(row=1, column=0, sticky="nsew")
            name_title_lbl.grid(row=1, column=1, sticky="nsew")
            address_title_lbl.grid(row=1, column=2, sticky="nsew")
            phone_number_title_lbl.grid(row=1, column=3, sticky="nsew")
            payment_status_title_lbl.grid(row=1, column=4, sticky="nsew")
            area_id_title_lbl.grid(row=1, column=5, sticky="nsew")
            monthly_consumption_title_lbl.grid(row=1, column=6, sticky="nsew")

            for i in range(len(results)):
                id_lbl = tk.Label(sub, text=f"{results[i][0]}", borderwidth=1, relief="solid")
                name_lbl = tk.Label(sub, text=f"{results[i][1]}", borderwidth=1, relief="solid")
                address_lbl = tk.Label(sub, text=f"{results[i][2]}", borderwidth=1, relief="solid")
                phone_number_lbl = tk.Label(sub, text=f"{results[i][3]}", borderwidth=1, relief="solid")
                payment_status_lbl = tk.Label(sub, text=f"{results[i][4]}", borderwidth=1, relief="solid")
                area_id_lbl = tk.Label(sub, text=f"{results[i][5]}", borderwidth=1, relief="solid")
                monthly_consumption_lbl = tk.Label(sub, text=f"{results[i][6]}", borderwidth=1, relief="solid")
                id_lbl.grid(row=i + 2, column=0, sticky="nsew")
                name_lbl.grid(row=i + 2, column=1, sticky="nsew")
                address_lbl.grid(row=i + 2, column=2, sticky="nsew")
                phone_number_lbl.grid(row=i + 2, column=3, sticky="nsew")
                payment_status_lbl.grid(row=i + 2, column=4, sticky="nsew")
                area_id_lbl.grid(row=i + 2, column=5, sticky="nsew")
                monthly_consumption_lbl.grid(row=i + 2, column=6, sticky="nsew")
        except Error as e:
            return e

    def display_household_information_using_id(self, parent):
        try:
            sub = tk.Toplevel(master=parent)
            sub.title(f"Search for household:")
            sub.resizable(height=False, width=False)

            # Create text entries
            id_ent = tk.Entry(sub, width=30)
            id_ent.grid(row=0, column=1, padx=20)

            # Create text labels
            id_lbl = tk.Label(sub, text="Enter the ID of the household to display information: ")
            id_lbl.grid(row=0, column=0)

            # Create Submit Function for Database:
            def submit():
                try:
                    # Create the electric.db or connect to it
                    conn = sqlite3.connect('electric.db')
                    # Create cursor
                    c = conn.cursor()
                    c.execute("PRAGMA foreign_keys = ON")
                    # Check if household_id exist:
                    c.execute("""SELECT id FROM households""")
                    results = c.fetchall()
                    household_ids = []
                    for result in results:
                        household_ids.append(result[0])
                    if int(id_ent.get()) not in household_ids:
                        messagebox.showerror(message="Household ID does not exist")
                        self.display_household_information_using_id(parent)
                        sub.destroy()
                    else:
                        self.display_household_information_with_id(parent, int(id_ent.get()))
                        sub.destroy()

                except Error as e:
                    return e

            # Create Submit Button
            submit_btn = tk.Button(sub, text="Submit", command=submit)
            submit_btn.grid(row=5, column=0, columnspan=2, ipadx=5, ipady=5, pady=5, padx=5)
        except Error as e:
            return e

    def display_household_information_with_name(self, parent, owner_name):
        try:
            sub = tk.Toplevel(master=parent)
            sub.title(f"Households with owner's name containing '{owner_name}':")
            sub.resizable(height=False, width=False)

            title_lbl = tk.Label(sub, text=f"Households with owner's name containing '{owner_name}':")
            title_lbl.grid(row=0, column=0, columnspan=7)
            self.c.execute("""PRAGMA case_sensitive_like = true""")
            self.c.execute(f"""SELECT * FROM households WHERE owner_name LIKE '%{owner_name}%'""")
            results = self.c.fetchall()
            id_title_lbl = tk.Label(sub, text="ID", borderwidth=1, relief="solid")
            name_title_lbl = tk.Label(sub, text="Household Owner Name", borderwidth=1, relief="solid")
            address_title_lbl = tk.Label(sub, text="Address", borderwidth=1, relief="solid")
            phone_number_title_lbl = tk.Label(sub, text="Phone number", borderwidth=1, relief="solid")
            payment_status_title_lbl = tk.Label(sub, text="Payment Status", borderwidth=1, relief="solid")
            area_id_title_lbl = tk.Label(sub, text="Area ID", borderwidth=1, relief="solid")
            monthly_consumption_title_lbl = tk.Label(sub, text="Monthly consumption", borderwidth=1, relief="solid")
            id_title_lbl.grid(row=1, column=0, sticky="nsew")
            name_title_lbl.grid(row=1, column=1, sticky="nsew")
            address_title_lbl.grid(row=1, column=2, sticky="nsew")
            phone_number_title_lbl.grid(row=1, column=3, sticky="nsew")
            payment_status_title_lbl.grid(row=1, column=4, sticky="nsew")
            area_id_title_lbl.grid(row=1, column=5, sticky="nsew")
            monthly_consumption_title_lbl.grid(row=1, column=6, sticky="nsew")

            for i in range(len(results)):
                id_lbl = tk.Label(sub, text=f"{results[i][0]}", borderwidth=1, relief="solid")
                name_lbl = tk.Label(sub, text=f"{results[i][1]}", borderwidth=1, relief="solid")
                address_lbl = tk.Label(sub, text=f"{results[i][2]}", borderwidth=1, relief="solid")
                phone_number_lbl = tk.Label(sub, text=f"{results[i][3]}", borderwidth=1, relief="solid")
                payment_status_lbl = tk.Label(sub, text=f"{results[i][4]}", borderwidth=1, relief="solid")
                area_id_lbl = tk.Label(sub, text=f"{results[i][5]}", borderwidth=1, relief="solid")
                monthly_consumption_lbl = tk.Label(sub, text=f"{results[i][6]}", borderwidth=1, relief="solid")
                id_lbl.grid(row=i + 2, column=0, sticky="nsew")
                name_lbl.grid(row=i + 2, column=1, sticky="nsew")
                address_lbl.grid(row=i + 2, column=2, sticky="nsew")
                phone_number_lbl.grid(row=i + 2, column=3, sticky="nsew")
                payment_status_lbl.grid(row=i + 2, column=4, sticky="nsew")
                area_id_lbl.grid(row=i + 2, column=5, sticky="nsew")
                monthly_consumption_lbl.grid(row=i + 2, column=6, sticky="nsew")
        except Error as e:
            return e

    def display_household_information_using_name(self, parent):
        try:
            sub = tk.Toplevel(master=parent)
            sub.title(f"Search for household:")
            sub.resizable(height=False, width=False)

            # Create text entries
            name_ent = tk.Entry(sub, width=30)
            name_ent.grid(row=0, column=1, padx=20)

            # Create text labels
            name_lbl = tk.Label(sub, text="Enter any part of the owner's name of the household to display information: ")
            name_lbl.grid(row=0, column=0)

            # Create Submit Function for Database:
            def submit():
                try:
                    # Create the electric.db or connect to it
                    conn = sqlite3.connect('electric.db')
                    # Create cursor
                    c = conn.cursor()
                    c.execute("PRAGMA foreign_keys = ON")
                    # Check if household_id exist:
                    self.display_household_information_with_name(parent, name_ent.get())
                    sub.destroy()

                except Error as e:
                    return e

            # Create Submit Button
            submit_btn = tk.Button(sub, text="Submit", command=submit)
            submit_btn.grid(row=5, column=0, columnspan=2, ipadx=5, ipady=5, pady=5, padx=5)
        except Error as e:
            return e

    def display_historical_record_with_id(self, parent, household_id):
        try:
            sub = tk.Toplevel(master=parent)
            sub.title(f"Information of Household {household_id}:")
            sub.resizable(height=False, width=False)

            title_lbl = tk.Label(sub, text=f"Information of Household {household_id}:")
            title_lbl.grid(row=0, column=0, columnspan=7)
            self.c.execute(f"""
                    SELECT households.id, households.owner_name, meters.month, meters.year, (meters.value * areas.price) as total
                    FROM households
                    INNER JOIN meters on households.id = meters.household_id
                    INNER JOIN areas on households.area_id = areas.id
                    WHERE households.id = {household_id}
                    """)
            results = self.c.fetchall()
            id_title_lbl = tk.Label(sub, text="ID", borderwidth=1, relief="solid")
            name_title_lbl = tk.Label(sub, text="Household Owner Name", borderwidth=1, relief="solid")
            month_title_lbl = tk.Label(sub, text="Payment month", borderwidth=1, relief="solid")
            year_title_lbl = tk.Label(sub, text="Payment year", borderwidth=1, relief="solid")
            payment_title_lbl = tk.Label(sub, text="Payment", borderwidth=1, relief="solid")
            id_title_lbl.grid(row=1, column=0, sticky="nsew")
            name_title_lbl.grid(row=1, column=1, sticky="nsew")
            month_title_lbl.grid(row=1, column=2, sticky="nsew")
            year_title_lbl.grid(row=1, column=3, sticky="nsew")
            payment_title_lbl.grid(row=1, column=4, sticky="nsew")

            for i in range(len(results)):
                id_lbl = tk.Label(sub, text=f"{results[i][0]}", borderwidth=1, relief="solid")
                name_lbl = tk.Label(sub, text=f"{results[i][1]}", borderwidth=1, relief="solid")
                month_lbl = tk.Label(sub, text=f"{results[i][2]}", borderwidth=1, relief="solid")
                year_lbl = tk.Label(sub, text=f"{results[i][3]}", borderwidth=1, relief="solid")
                payment_lbl = tk.Label(sub, text=f"{results[i][4]}", borderwidth=1, relief="solid")
                id_lbl.grid(row=i + 2, column=0, sticky="nsew")
                name_lbl.grid(row=i + 2, column=1, sticky="nsew")
                month_lbl.grid(row=i + 2, column=2, sticky="nsew")
                year_lbl.grid(row=i + 2, column=3, sticky="nsew")
                payment_lbl.grid(row=i + 2, column=4, sticky="nsew")
        except Error as e:
            return e

    def clear_window(self, window):
        widgets = window.winfo_children()
        for widget in widgets:
            widget.destroy()

    def create_loading_screen(self):
        init_window = tk.Tk()
        init_window.title("EIMS")
        init_window.resizable(height=False, width=False)
        init_window.eval('tk::PlaceWindow . center')
        init_lbl = tk.Label(text="Initializing engine: 0%", master=init_window)
        init_lbl.grid(row=0, column=0, padx=30, pady=10, sticky="s")
        style = ttk.Style()
        style.theme_use('default')
        style.configure("black.Horizontal.TProgressbar", background='cornflower blue')
        bar = Progressbar(master=init_window, length=200, style='black.Horizontal.TProgressbar')
        bar['value'] = 0
        bar.grid(column=0, row=1, padx=30, pady=10, sticky="n")
        init_window.after(2000, lambda: init_window.destroy())

        def update_progressbar(value):
            bar['value'] = value

        def update_process(value):
            init_lbl['text'] = f"Initializing engine: {value}%"

        for i in range(100):
            init_window.after(20 * i, update_progressbar, i)
            init_window.after(20 * i, update_process, i + 1)
        init_window.mainloop()

    def start_engine(self):

        # self.create_loading_screen()
        self.on_start()
        #
        root = tk.Tk()
        root.title("EIMS")
        root.resizable(width=False, height=False)
        root.geometry("500x709")
        background_img = tk.PhotoImage(file='new_background_img.png')
        background_label = tk.Label(master=root, image=background_img)
        background_label.place(relwidth=1, relheight=1)
        logo_lbl = tk.Label(text="EIMS", font="Fixedsys 60 bold", master=root, fg="white", bg="cornflower blue")
        logo_lbl.pack(pady=30, fill=tk.X)
        btn1 = tk.Button(text="Input data", master=root, font=("Arial", 16, "bold"), borderwidth=5, width=20,
                         fg="black", bg="light yellow")
        btn2 = tk.Button(text="Delete data", master=root, font=("Arial", 16, "bold"), borderwidth=5, width=20,
                         fg="black", bg="light yellow")
        btn3 = tk.Button(text="Update data", master=root, font=("Arial", 16, "bold"), borderwidth=5, width=20,
                         fg="black", bg="light yellow")
        btn4 = tk.Button(text="Display data", master=root, font=("Arial", 16, "bold"), borderwidth=5, width=20,
                         fg="black", bg="light yellow")
        btn5 = tk.Button(text="Plot figures", master=root, font=("Arial", 16, "bold"), borderwidth=5, width=20,
                         fg="black", bg="light yellow")
        btn6 = tk.Button(text="Print bill", font=("Arial", 16, "bold"), borderwidth=5, width=20, fg="black",
                         bg="light yellow")
        btn7 = tk.Button(text="Exit", master=root, font=("Arial", 16, "bold"), borderwidth=5, width=20, fg="black",
                         bg="light yellow")
        btn1.pack(pady=10, ipadx=5, ipady=5)
        btn2.pack(pady=10, ipadx=5, ipady=5)
        btn3.pack(pady=10, ipadx=5, ipady=5)
        btn4.pack(pady=10, ipadx=5, ipady=5)
        btn5.pack(pady=10, ipadx=5, ipady=5)
        btn6.pack(pady=10, ipadx=5, ipady=5)
        btn7.pack(pady=10, ipadx=5, ipady=5)

        # self.input_areas(root)
        # self.input_households(root)
        # self.update_household_information(root)
        # self.list_households(root)
        # self.list_areas(root)
        # self.delete_household(root)
        # self.update_meter_information(root)
        # self.update_payment_status(root)
        # self.auto_increase_payment_status()
        # self.list_paid_household(root)
        # self.list_not_yet_paid_household(root)
        # self.display_household_information_using_id(root)

        # self.c.execute("""
        # SELECT households.id, households.owner_name, meters.month, meters.year, (meters.value * areas.price) as total
        # FROM households
        # INNER JOIN meters on households.id = meters.household_id
        # INNER JOIN areas on households.area_id = areas.id
        # WHERE households.id = 1
        # """)
        # results = self.c.fetchall()
        # print(results)

        # self.display_household_information_using_name(root)

        root.mainloop()



if __name__ == '__main__':
    e = Engine()
    e.start_engine()
