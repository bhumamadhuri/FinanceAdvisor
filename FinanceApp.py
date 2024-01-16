from tkinter import *
from tkinter import ttk
from tkinter import messagebox,filedialog
import sqlite3
import time
from PIL import ImageTk, Image
import datetime
from tkcalendar import DateEntry
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 
import seaborn as sns
import time


def show():
         hide_button = Button( lgn_frame, image= hide_image, command=hide, relief=FLAT,
                                  activebackground="white"
                                  , borderwidth=0, background="white", cursor="hand2")
         hide_button.place(x=860, y=420)
         password_entry.config(show='')
def hide():
         show_button = Button( lgn_frame, image= show_image, command=show, relief=FLAT,
                                  activebackground="white"
                                  , borderwidth=0, background="white", cursor="hand2")
         show_button.place(x=860, y=420)
         password_entry.config(show='*')

def connect():
    conn=sqlite3.connect("financeflow.db")
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY,name TEXT,username TEXT,password TEXT)")
    conn.commit()
    conn.close()
connect()

def adduser(name,username,password):
    conn=sqlite3.connect("financeflow.db")
    cur=conn.cursor()
    cur.execute("INSERT INTO users VALUES(NULL,?,?,?)",(name,username,password))
    conn.commit()
    conn.close()

def updateuser(name,username,password):
    conn=sqlite3.connect("financeflow.db")
    cur=conn.cursor()
    cur.execute("update users set password=? where name=? and username=?",(password,name,username))
    conn.commit()
    conn.close()

def checkuser(username,password):
    conn=sqlite3.connect("financeflow.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?",(str(username),str(password)))
    result=cur.fetchone()
    return result

def getusername(username,password):
    conn=sqlite3.connect("financeflow.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?",(username,password))
    result=cur.fetchone()
    global profilename
    global session_user_id
    global session_user_name
    if result!=None:
        profilename=result[1]
        session_user_id=result[0]
        session_user_name=result[1]


def login():
    a = login_username.get()
    b = login_password.get()
    print(a)
    print(b)
    getusername(a,b)
    result1 = checkuser(a,b)
    print(result1)
    if (checkuser(a,b))!=None:
        window.destroy()
        Maindashboardwindow()     
    else:
        username_entry.delete(0,END)
        password_entry.delete(0,END)
        messagebox.showinfo('oops something wrong', 'Invalid credentials')

profilename="" 
session_user_id = 0
session_user_name=None

activewindow=None
t = 11

def Maindashboardwindow():

    def expensewindow1():

        def connect1():
            conn=sqlite3.connect("financeflow.db")
            cur=conn.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS expensetable(id INTEGER PRIMARY KEY,itemname TEXT,date TEXT,cost TEXT,optional_notes TEXT,user_id INTEGER)")
            conn.commit()
            conn.close()
        connect1()

        def insert(itemname,date,cost,optional_notes):
            conn=sqlite3.connect("financeflow.db")
            cur=conn.cursor()
            print(session_user_id)
            cur.execute("SELECT * FROM expensetable where user_id=? and itemname=? and date=? and cost=? and optional_notes=?",(session_user_id,itemname,date,cost,optional_notes))
            rows=cur.fetchall()
            if rows:
                pass
            else:
                cur.execute("SELECT budget FROM budgettable where user_id=? and category=? and year=? and month=?",(session_user_id,itemname,date[0:4],date[5:7]))
                budget_threshold = cur.fetchall()
                cur.execute("SELECT sum(cost) FROM expensetable where user_id=? and itemname=? and substring(date,1,7)=? group by itemname",(session_user_id,itemname,date[0:7]))
                expense_added=cur.fetchall()
                print(budget_threshold,expense_added)
                try:
                    if int(expense_added[0][0]):
                        expense_added=int(expense_added[0][0])
                except:
                    expense_added=0
                try:
                    if int(budget_threshold[0][0]):
                        budget_threshold=int(budget_threshold[0][0])
                except:
                    budget_threshold=0
                print(budget_threshold,expense_added)
                print(expense_added+int(cost))
                if expense_added+int(cost) > budget_threshold:
                    messagebox.showinfo("Out of Budget","Maximum "+str(int(budget_threshold)-int(expense_added))+" dollars left for this month under the "+itemname+" category",parent=gui)
                    
                else:
                    cur.execute("INSERT INTO expensetable VALUES(NULL,?,?,?,?,?)",(itemname,date,cost,optional_notes,session_user_id))
            conn.commit()
            conn.close()
        
        def updaterecord(serial_id,itemname,date,cost,optional_notes):
            conn=sqlite3.connect("financeflow.db")
            cur=conn.cursor()
            print(session_user_id)
            cur.execute("update expensetable set itemname=?,date=?,cost=?,optional_notes=? where user_id=? and id=?",(itemname,date,cost,optional_notes,session_user_id,serial_id))
            conn.commit()
            conn.close()
            

        def removerecord(serial_id):
            conn=sqlite3.connect("financeflow.db")
            cur=conn.cursor()
            print(session_user_id)
            cur.execute("delete from expensetable where user_id=? and id=?",(session_user_id,serial_id))
            conn.commit()
            conn.close()
        
        def insertitems():
            a=exp_itemname.get()
            b=exp_date.get()
            c=exp_cost.get()
            d=c.replace('.', '', 1)
            e=b.count('-')
            f=exp_optional_notes.get()    

            if a=="" or b=="" or c=="":
                messagebox.showinfo("oops something wrong","Field should not be empty",parent=gui)
            elif len(b)!=10 or e!=2:
                messagebox.showinfo("oops something wrong","DATE should be in format dd-mm-yyyy",parent=gui)
            elif (d.isdigit()==False):
                messagebox.showinfo("oops something wrong","Cost should be a number",parent=gui)
            else:
                insert(a,b,c,f)
                viewallitems()
                exp_itemname.set("choose categoty")
                e2.delete(0,END)
                e3.delete(0,END)
                e10.delete(0,END)
        
        def view():
            conn=sqlite3.connect("financeflow.db")
            cur=conn.cursor()
            cur.execute("SELECT * FROM expensetable where user_id=?",(session_user_id,))
            rows=cur.fetchall()
            conn.commit()
            conn.close()
            print(rows)
            return rows

        def viewallitems():
            rows=view()
            for item in table.get_children():
                table.delete(item)
            for row in rows:
                print(row)
                a=str(row[0])
                b=str(row[1])
                c=str(row[2])
                d=str(row[3])
                e=str(row[4])
                f= (a,b,c,d,e)
                table.insert(parent='',index=0,values=f)     
        

        def select_record(event):
            global selected_rowid
            selected = table.selection()    
            val = table.item(selected, 'values')
            print(val)
            try:
                selected_rowid = int(val[0])
                exp_itemname.set(val[1])
                exp_date.set(val[2])
                exp_cost.set(val[3])
                exp_optional_notes.set(val[4])
            except Exception as ep:
                pass

        def update_record():
            global selected_rowid

            selected = table.selection()
            # Update record
            a=exp_itemname.get()
            b=exp_date.get()
            c=exp_cost.get()
            d=c.replace('.', '', 1)
            e=b.count('-')
            f=exp_optional_notes.get()    

            if a=="" or b=="" or c=="":
                messagebox.showinfo("oops something wrong","Field should not be empty",parent=gui)
            elif len(b)!=10 or e!=2:
                messagebox.showinfo("oops something wrong","DATE should be in format dd-mm-yyyy",parent=gui)
            elif (d.isdigit()==False):
                messagebox.showinfo("oops something wrong","Cost should be a number",parent=gui)
            else:
                try:
                    updaterecord(selected_rowid,exp_itemname.get(),e2.get(),e3.get(),e10.get())
                except Exception as ep:
                    messagebox.showerror('Error',  ep)

            # Clear entry boxes
            exp_itemname.set("choose categoty")
            e2.delete(0,END)
            e3.delete(0,END)
            e10.delete(0,END)
            viewallitems()

        def deleteRow():
            global selected_rowid
            result = messagebox.askyesno("Confirmation", "Do you want delete this item?",parent=gui)
            if result:
                # User clicked 'Yes'
                print("Proceeding...")
                removerecord(selected_rowid)
                viewallitems()
            else:
                # User clicked 'No' or closed the messagebox
                print("Cancelled.")
            removerecord(selected_rowid)
        
       
        global gui
        #gui = Toplevel(activewindow)
        gui = Frame(activewindow)
        #gui.title("ADD EXPENSE")
        #gui.configure(bg='#1abeff')
        #gui.geometry("900x700")
        
        l8=Label(gui,width=60,height=7,font=("century",35),bg="#EDE4E4",text="")
        l8.place(x=450,y=60)
        l8.pack()
        l7=Label(gui,width=100,height=10,font=("century",35),bg="#EDE4E4",text="")
        l7.place(x=-455,y=410)
        l7.pack()
        l1=Label(gui,font=("cooper black",17),bg="#EDE4E4",text="Category",fg ="#755050").place(x=170,y=200)
        exp_itemname=StringVar()
        exp_itemname.set("choose categoty")
        e1=OptionMenu(gui, exp_itemname,"Housing", "Transportation","Food","Personal Care","Entertainment","Utilities","Debts and Loans","Insurance","Savings","Gifts and Donations","Miscellaneous")
        e1.place(x=420,y=205,height=27,width=165)
        l2=Label(gui,font=("cooper black",17),bg="#EDE4E4",text="Date(yyyy-mm-dd)",fg ="#755050").place(x=170,y=250)
        exp_date=StringVar()
        e2=DateEntry(gui,font=("adobe clean",15),textvariable=exp_date,selectmode='day',date_pattern="yyyy-mm-dd")
        e2.place(x=420,y=255,height=27,width=165)
        l3=Label(gui,font=("cooper black",17),bg="#EDE4E4",text="Amount",fg ="#755050").place(x=170,y=300)
        exp_cost=StringVar()
        e3=Entry(gui,font=("adobe clean",15),textvariable=exp_cost)
        e3.place(x=420,y=305,height=27,width=165)
        l10=Label(gui,font=("cooper black",17),bg="#EDE4E4",text="Optional Notes",fg ="#755050").place(x=170,y=350)
        exp_optional_notes=StringVar()
        e10=Entry(gui,font=("adobe clean",15),textvariable=exp_optional_notes)
        e10.place(x=420,y=355,height=27,width=165)
        b1=Button(gui,text="SUBMIT",bg='#8DC2B7', font=("", 17, "bold"), bd=0, fg='#000000',
                                  cursor='hand2', borderwidth=0,activebackground='#32cf8e',command=insertitems)
        b1.place(x=280,y=450)
        b2=Button(gui,text="UPDATE",bg='#8DC2B7', font=("", 17, "bold"), bd=0, fg='#000000',
                                  cursor='hand2',borderwidth=0, activebackground='#32cf8e',command=update_record).place(x=770,y=500)
        b3=Button(gui,text="DELETE",bg='#8DC2B7', font=("", 17, "bold"), bd=0, fg='#000000',
                                  cursor='hand2', borderwidth=0,activebackground='#32cf8e',command=deleteRow).place(x=970,y=500)
        l6=Label(gui,width=60,font=("Garamond",35),bg="#429181",fg="#E0F3EF",text="MANAGE YOUR EXPENSE").place(x=-200,y=0)
        name = "Welcome, " + profilename
        back_button=Button(gui,text=" Go Back",bg='#8DC2B7', font=("", 17, "bold"), bd=0, fg='#000000',
                                  cursor='hand2',borderwidth=0, activebackground='#32cf8e',command=dashboard_frame)
        back_button.place(x=0,y=80)
    
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11)) # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13,'bold')) # Modify the font of the headings
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders
        table = ttk.Treeview(gui,columns=('Serial No','Category','Date','Amount','Description'),show='headings',style="mystyle.Treeview")
        table.column("# 1",anchor=CENTER, stretch=NO, width=0)
        table.column("# 2",anchor=CENTER, stretch=NO, width=100)
        table.column("# 3",anchor=CENTER, stretch=NO, width=100)
        table.column("# 4",anchor=CENTER, stretch=NO, width=100)
        table.column("# 5",anchor=CENTER, stretch=NO, width=100)
        table.heading('Serial No',text='Serial No')
        table.heading('Category',text='Category')
        table.heading('Amount',text='Amount')
        table.heading('Description',text='Description')
        table.heading('Date',text='Date')
        table.pack(fill='both',expand=True)
        table.place(x=700,y=200)
        table.bind("<ButtonRelease-1>", select_record)
        viewallitems()

    def incomewindow():

        def connect1():
            conn=sqlite3.connect("financeflow.db")
            cur=conn.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS incometable(id INTEGER PRIMARY KEY,source TEXT,date TEXT,amount TEXT,optional_notes TEXT,user_id INTEGER)")
            conn.commit()
            conn.close()
        connect1()

        def insert(source,date,amount,optional_notes):
            conn=sqlite3.connect("financeflow.db")
            cur=conn.cursor()
            print(session_user_id)
            cur.execute("SELECT * FROM incometable where user_id=? and source=? and date=? and amount=? and optional_notes=?",(session_user_id,source,date,amount,optional_notes))
            rows=cur.fetchall()
            if rows:
                pass
            else:
                cur.execute("INSERT INTO incometable VALUES(NULL,?,?,?,?,?)",(source,date,amount,optional_notes,session_user_id))
            conn.commit()
            conn.close()

        def updaterecord(serial_id,itemname,date,cost,optional_notes):
            conn=sqlite3.connect("financeflow.db")
            cur=conn.cursor()
            print(session_user_id)
            cur.execute("update incometable set source=?,date=?,amount=?,optional_notes=? where user_id=? and id=?",(itemname,date,cost,optional_notes,session_user_id,serial_id))
            conn.commit()
            conn.close()
                

        def removerecord(serial_id):
            conn=sqlite3.connect("financeflow.db")
            cur=conn.cursor()
            print(session_user_id)
            cur.execute("delete from incometable where user_id=? and id=?",(session_user_id,serial_id))
            conn.commit()
            conn.close()
        
        def insertitems():
            a=exp_source.get()
            b=exp_date.get()
            c=exp_amount.get()
            d=c.replace('.', '', 1)
            e=b.count('-')
            f=exp_optional_notes.get()    

            if a=="" or b=="" or c=="":
                messagebox.showinfo("oops something wrong","Field should not be empty",parent=income_gui)
            elif len(b)!=10 or e!=2:
                messagebox.showinfo("oops something wrong","DATE should be in format dd-mm-yyyy",parent=income_gui)
            elif (d.isdigit()==False):
                messagebox.showinfo("oops something wrong","amount should be a number",parent=income_gui)
            else:
                insert(a,b,c,f)
                viewallitems()
                e1.delete(0,END)
                e2.delete(0,END)
                e3.delete(0,END)
                e10.delete(0,END)

        def view():
            conn=sqlite3.connect("financeflow.db")
            cur=conn.cursor()
            cur.execute("SELECT * FROM incometable where user_id=?",(session_user_id,))
            rows=cur.fetchall()
            conn.commit()
            conn.close()
            print(rows)
            return rows

        def viewallitems():
            rows=view()
            for item in table.get_children():
                table.delete(item)
            for row in rows:
                print(row)
                a=str(row[0])
                b=str(row[1])
                c=str(row[2])
                d=str(row[3])
                e=str(row[4])
                f= (a,b,c,d,e)
                table.insert(parent='',index=0,values=f)     
        

        def select_record(event):
            global selected_rowid
            selected = table.selection()    
            val = table.item(selected, 'values')
            print(val)
            try:
                selected_rowid = int(val[0])
                exp_source.set(val[1])
                exp_date.set(val[2])
                exp_amount.set(val[3])
                exp_optional_notes.set(val[4])
            except Exception as ep:
                pass

        def update_record():
            global selected_rowid

            selected = table.selection()
            # Update record
            a=exp_source.get()
            b=exp_date.get()
            c=exp_amount.get()
            d=c.replace('.', '', 1)
            e=b.count('-')
            f=exp_optional_notes.get()    

            if a=="" or b=="" or c=="":
                messagebox.showinfo("oops something wrong","Field should not be empty",parent=income_gui)
            elif len(b)!=10 or e!=2:
                messagebox.showinfo("oops something wrong","DATE should be in format dd-mm-yyyy",parent=income_gui)
            elif (d.isdigit()==False):
                messagebox.showinfo("oops something wrong","Cost should be a number",parent=income_gui)
            else:
                try:
                    updaterecord(selected_rowid,exp_source.get(),e2.get(),e3.get(),e10.get())
                except Exception as ep:
                    messagebox.showerror('Error',  ep)

            # Clear entry boxes
            e1.delete(0,END)
            e2.delete(0,END)
            e3.delete(0,END)
            e10.delete(0,END)
            viewallitems()

        def deleteRow():
            global selected_rowid
            result = messagebox.askyesno("Confirmation", "Do you want delete this item?",parent=income_gui)
            if result:
                # User clicked 'Yes'
                print("Proceeding...")
                removerecord(selected_rowid)
                viewallitems()
            else:
                # User clicked 'No' or closed the messagebox
                print("Cancelled.")
            removerecord(selected_rowid)
        
        global income_gui
        income_gui = Frame(activewindow)
        #income_gui.title("ADD INCOME")
        #income_gui.configure(bg='#1abeff')
        #income_gui.geometry("900x700")
        
        l8=Label(income_gui,width=60,height=7,font=("century",35),bg="#EDE4E4",text="")
        l8.place(x=450,y=60)
        l8.pack()
        l7=Label(income_gui,width=100,height=10,font=("century",35),bg="#EDE4E4",text="")
        l7.place(x=-455,y=410)
        l7.pack()
        l1=Label(income_gui,font=("cooper black",17),bg="#EDE4E4",text="Source",fg ="#755050").place(x=170,y=200)
        exp_source=StringVar()
        e1=Entry(income_gui,font=("adobe clean",15),textvariable=exp_source)
        e1.place(x=420,y=205,height=27,width=165)
        l2=Label(income_gui,font=("cooper black",17),bg="#EDE4E4",text="Date(yyyy-mm-dd)",fg ="#755050").place(x=170,y=250)
        exp_date=StringVar()
        e2=DateEntry(income_gui,font=("adobe clean",15),textvariable=exp_date,selectmode='day',date_pattern="yyyy-mm-dd")
        e2.place(x=420,y=255,height=27,width=165)
        l3=Label(income_gui,font=("cooper black",17),bg="#EDE4E4",text="Amount",fg ="#755050").place(x=170,y=300)
        exp_amount=StringVar()
        e3=Entry(income_gui,font=("adobe clean",15),textvariable=exp_amount)
        e3.place(x=420,y=305,height=27,width=165)
        l10=Label(income_gui,font=("cooper black",17),bg="#EDE4E4",text="Optional Notes",fg ="#755050").place(x=170,y=350)
        exp_optional_notes=StringVar()
        e10=Entry(income_gui,font=("adobe clean",15),textvariable=exp_optional_notes)
        e10.place(x=420,y=355,height=27,width=165)
        b1=Button(income_gui,text="SUBMIT",bg='#8DC2B7', font=("", 17, "bold"), bd=0, fg='#000000',
                                  cursor='hand2', borderwidth=0,activebackground='#32cf8e',command=insertitems)
        b1.place(x=280,y=450)
        b2=Button(income_gui,text="UPDATE",bg='#8DC2B7', font=("", 17, "bold"), bd=0, fg='#000000',
                                  cursor='hand2',borderwidth=0, activebackground='#32cf8e',command=update_record).place(x=770,y=500)
        b3=Button(income_gui,text="DELETE",bg='#8DC2B7', font=("", 17, "bold"), bd=0, fg='#000000',
                                  cursor='hand2', borderwidth=0,activebackground='#32cf8e',command=deleteRow).place(x=970,y=500)
        l6=Label(income_gui,width=60,font=("Garamond",35),bg="#429181",fg="#E0F3EF",text="MANAGE YOUR INCOME").place(x=-200,y=0)

        back_button=Button(income_gui,text=" Go Back",bg='#8DC2B7', font=("", 17, "bold"), bd=0, fg='#000000',
                                  cursor='hand2',borderwidth=0, activebackground='#32cf8e',command=dashboard_frame)
        back_button.place(x=0,y=80)


        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11)) # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13,'bold')) # Modify the font of the headings
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders
        table = ttk.Treeview(income_gui,columns=('Serial No','Source','Date','Amount','Description'),show='headings',style="mystyle.Treeview")
        table.column("# 1",anchor=CENTER, stretch=NO, width=0)
        table.column("# 2",anchor=CENTER, stretch=NO, width=100)
        table.column("# 3",anchor=CENTER, stretch=NO, width=100)
        table.column("# 4",anchor=CENTER, stretch=NO, width=100)
        table.column("# 5",anchor=CENTER, stretch=NO, width=100)
        table.heading('Serial No',text='Serial No')
        table.heading('Source',text='Source')
        table.heading('Amount',text='Amount')
        table.heading('Description',text='Description')
        table.heading('Date',text='Date')
        table.pack(fill='both',expand=True)
        table.place(x=700,y=200)
        table.bind("<ButtonRelease-1>", select_record)
        viewallitems()

    def budgetwindow():

        def connect1():
            conn=sqlite3.connect("financeflow.db")
            cur=conn.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS budgettable(budget_id INTEGER PRIMARY KEY,category TEXT, year INTEGER,month INTEGER,budget INTEGER,user_id INTEGER)")
            conn.commit()
            conn.close()
        connect1()

        def insert(category,year,month,budget):
            conn=sqlite3.connect("financeflow.db")
            cur=conn.cursor()
            print(session_user_id)
            cur.execute("select * from budgettable where category=? and year=? and month=? and user_id=?",(category,year,month,session_user_id))
            if cur.fetchall():
                cur.execute("update budgettable set budget=? where category=? and year=? and month=? and user_id=?",(budget,category,year,month,session_user_id))
                conn.commit()
                conn.close()
            else:
                cur.execute("INSERT INTO budgettable VALUES(NULL,?,?,?,?,?)",(category,year,month,budget,session_user_id))
                conn.commit()
                conn.close()
        

        def updaterecord(serial_id,category,year,month,budget):
            conn=sqlite3.connect("financeflow.db")
            cur=conn.cursor()
            print(session_user_id)
            cur.execute("update budgettable set category=?,year=?,month=?,budget=? where user_id=? and budget_id=?",(category,year,month,budget,session_user_id,serial_id))
            conn.commit()
            conn.close()
                

        def removerecord(serial_id):
            conn=sqlite3.connect("financeflow.db")
            cur=conn.cursor()
            print(session_user_id)
            cur.execute("delete from budgettable where user_id=? and budget_id=?",(session_user_id,serial_id))
            conn.commit()
            conn.close()

        def insertitems():
            a=exp_category.get()
            b=exp_year.get()
            c=exp_month.get().zfill(2)
            d=c.replace('.', '', 1)
            e=b.count('-')
            f=exp_amount.get()   

            if a=="" or b=="" or c=="":
                messagebox.showinfo("oops something wrong","Field should not be empty",parent=budget_gui)
            elif (f.isdigit()==False):
                messagebox.showinfo("oops something wrong","budget sholud be in number",parent=budget_gui)
            else:
                insert(a,b,c,f)
                viewallitems()
                exp_category.set("choose category")
                exp_year.set("choose year")
                exp_month.set("choose month")
                e10.delete(0,END)

        def view():
            conn=sqlite3.connect("financeflow.db")
            cur=conn.cursor()
            cur.execute("SELECT * FROM budgettable where user_id=?",(session_user_id,))
            rows=cur.fetchall()
            conn.commit()
            conn.close()
            print(rows)
            return rows

        def viewallitems():
            rows=view()
            for item in table.get_children():
                table.delete(item)
            for row in rows:
                print(row)
                a=str(row[0])
                b=str(row[1])
                c=str(row[2])
                d=str(row[3])
                e=str(row[4])
                f= (a,b,c,d,e)
                table.insert(parent='',index=0,values=f)     
        

        def select_record(event):
            global selected_rowid
            selected = table.selection()    
            val = table.item(selected, 'values')
            print(val)
            try:
                selected_rowid = int(val[0])
                exp_category.set(val[1])
                exp_year.set(val[2])
                exp_month.set(val[3])
                exp_amount.set(val[4])
            except Exception as ep:
                pass

        def update_record():
            global selected_rowid

            selected = table.selection()
            # Update record
            a=exp_category.get()
            b=exp_year.get()
            c=exp_month.get()
            #d=c.replace('.', '', 1)
           # e=b.count('-')
            f=exp_amount.get()    

            if a=="" or b=="" or c=="":
                messagebox.showinfo("oops something wrong","Field should not be empty",parent=budget_gui)
            elif (f.isdigit()==False):
                messagebox.showinfo("oops something wrong","Budget should be a number",parent=budget_gui)
            else:
                try:
                    updaterecord(selected_rowid,exp_category.get(),exp_year.get(),exp_month.get(),e10.get())
                except Exception as ep:
                    messagebox.showerror('Error',  ep)

            # Clear entry boxes
            exp_category.set("choose category")
            exp_year.set("choose year")
            exp_month.set("choose month")
            e10.delete(0,END)
            viewallitems()

        def deleteRow():
            global selected_rowid
            result = messagebox.askyesno("Confirmation", "Do you want delete this item?",parent=budget_gui)
            if result:
                # User clicked 'Yes'
                print("Proceeding...")
                removerecord(selected_rowid)
                viewallitems()
            else:
                # User clicked 'No' or closed the messagebox
                print("Cancelled.")
            removerecord(selected_rowid)

        global budget_gui
        budget_gui = Frame(activewindow)
        #budget_gui.title("ADD BUDGET")
        #budget_gui.configure(bg='#1abeff')
        #budget_gui.geometry("900x700")
        
        l8=Label(budget_gui,width=60,height=7,font=("century",35),bg="#EDE4E4",text="")
        l8.place(x=450,y=60)
        l8.pack()
        l7=Label(budget_gui,width=100,height=10,font=("century",35),bg="#EDE4E4",text="")
        l7.place(x=-455,y=410)
        l7.pack()
        l1=Label(budget_gui,font=("cooper black",17),bg="#EDE4E4",text="Category",fg ="#755050").place(x=170,y=200)
        exp_category=StringVar()
        exp_category.set("choose categoty")
        e1=OptionMenu(budget_gui, exp_category,"Housing","Transportation","Food","Personal Care","Entertainment","Utilities","Debts and Loans","Insurance","Savings","Gifts and Donations","Miscellaneous")
        e1.place(x=420,y=205,height=27,width=165)
        l2=Label(budget_gui,font=("cooper black",17),bg="#EDE4E4",text="Year",fg ="#755050").place(x=170,y=250)
        exp_year=StringVar()
        exp_year.set("choose year")
        year_list =[i for i in range(int(datetime.datetime.now().strftime("%Y")),int(datetime.datetime.now().strftime("%Y"))+1)]
        e2=OptionMenu(budget_gui, exp_year,*year_list)
        e2.place(x=420,y=255,height=27,width=165)
        l3=Label(budget_gui,font=("cooper black",17),bg="#EDE4E4",text="Month",fg ="#755050").place(x=170,y=300)
        exp_month=StringVar()
        exp_month.set("choose month")
        month_list = [i for i in range(int(datetime.datetime.now().strftime("%m")),13)]
        e3=OptionMenu(budget_gui, exp_month,*month_list)
        e3.place(x=420,y=305,height=27,width=165)
        l10=Label(budget_gui,font=("cooper black",17),bg="#EDE4E4",text="Budget",fg ="#755050").place(x=170,y=350)
        exp_amount=StringVar()
        e10=Entry(budget_gui,font=("adobe clean",15),textvariable=exp_amount)
        e10.place(x=420,y=355,height=27,width=165)
        b1=Button(budget_gui,text="SUBMIT",bg='#8DC2B7', font=("", 17, "bold"), bd=0, fg='#000000',
                                  cursor='hand2', borderwidth=0,activebackground='#32cf8e',command=insertitems)
        b1.place(x=280,y=450)
        b2=Button(budget_gui,text="UPDATE",bg='#8DC2B7', font=("", 17, "bold"), bd=0, fg='#000000',
                                  cursor='hand2',borderwidth=0, activebackground='#32cf8e',command=update_record).place(x=770,y=500)
        b3=Button(budget_gui,text="DELETE",bg='#8DC2B7', font=("", 17, "bold"), bd=0, fg='#000000',
                                  cursor='hand2', borderwidth=0,activebackground='#32cf8e',command=deleteRow).place(x=970,y=500)
        l6=Label(budget_gui,width=60,font=("Garamond",35),bg="#429181",fg="#E0F3EF",text="SET YOUR BUDGET").place(x=-200,y=0)

        back_button=Button(budget_gui,text=" Go Back",bg='#8DC2B7', font=("", 17, "bold"), bd=0, fg='#000000',
                                  cursor='hand2',borderwidth=0, activebackground='#32cf8e',command=dashboard_frame)
        back_button.place(x=0,y=80)


        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11)) # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13,'bold')) # Modify the font of the headings
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders
        table = ttk.Treeview(budget_gui,columns=('Serial No','Category','Year','Month','Budget'),show='headings',style="mystyle.Treeview")
        table.column("# 1",anchor=CENTER, stretch=NO, width=0)
        table.column("# 2",anchor=CENTER, stretch=NO, width=100)
        table.column("# 3",anchor=CENTER, stretch=NO, width=100)
        table.column("# 4",anchor=CENTER, stretch=NO, width=100)
        table.column("# 5",anchor=CENTER, stretch=NO, width=100)
        table.heading('Serial No',text='Serial No')
        table.heading('Category',text='Category')
        table.heading('Year',text='Year')
        table.heading('Month',text='Month')
        table.heading('Budget',text='Budget')
        table.pack(fill='both',expand=True)
        table.place(x=700,y=200)
        table.bind("<ButtonRelease-1>", select_record)
        viewallitems()

    def fetchexpensewindow():

        def view():
            print(exp_category.get())
            print(exp_startdate.get())
            print(exp_enddate.get())
            conn=sqlite3.connect("financeflow.db")
            cur=conn.cursor()
            if exp_category.get()  in ["Housing","Transportation","Food","Personal Care","Entertainment","Utilities","Debts and Loans","Insurance","Savings","Gifts and Donations","Miscellaneous"]:
                cur.execute("SELECT itemname,cost,optional_notes,date FROM expensetable where user_id=? and itemname=? and(date(date) between date(?) and date(?) or date(date)=date(?) or date(date)=date(?))",(session_user_id,exp_category.get(),exp_startdate.get(),exp_enddate.get(),exp_startdate.get(),exp_enddate.get()))
            else:
                cur.execute("SELECT itemname,cost,optional_notes,date FROM expensetable where user_id=? and (date(date) between date(?) and date(?) or date(date)=date(?) or date(date)=date(?))",(session_user_id,exp_startdate.get(),exp_enddate.get(),exp_startdate.get(),exp_enddate.get()))
            rows=cur.fetchall()
            conn.commit()
            conn.close()
            print(rows)
            return rows
        
        def graph(rows):
            print(rows)
            data = {'amount': [int(i[1]) for i in rows],
            'date': [datetime.datetime.strptime(i[3], '%Y-%m-%d').strftime('%Y-%m') for i in rows],
            'Category': [str(i[0]) for i in rows]
            }  
            df = pd.DataFrame(data)
            agg_data = df.groupby(['Category','date'])['amount'].sum().reset_index()
            agg_data=agg_data.sort_values(by=['date'])
            sns.set(style="whitegrid")  # Set the Seaborn style
            plt.figure(figsize=(6, 4))  # Set the figure size
            # Create the bar graph
            plt.title("Bar Graph")  # Add a title
            sns.barplot(data=agg_data, x='date', y='amount', hue='Category')
            canvas = FigureCanvasTkAgg(plt.gcf(), master=fetchexpense_gui)
            canvas.get_tk_widget().place(x=700,y=200)
            toolbar = NavigationToolbar2Tk(canvas, fetchexpense_gui) 
            toolbar.update()
            toolbar.place(x=800,y=630)
        
        def viewallitems():
            for item in table.get_children():
                table.delete(item)
            rows=view()
            for row in rows:
                print(row)
                a=str(row[0])
                b=str(row[1])
                c=str(row[2])
                d=str(row[3])
                f= (a,b,c,d)
                table.insert(parent='',index=0,values=f)
            e2.delete(0,END)
            e3.delete(0,END)
            exp_category.set("choose category")
            graph(rows)

        def export_to_excel():
            # Get data from TreeView
            data = []
            for item in table.get_children():
                values = table.item(item, 'values')
                data.append(values)

            # Create a Pandas DataFrame
            
            df = pd.DataFrame(data, columns=['Category','Amount','Description','Date'])
            

            # Export to Excel
            folder_path = filedialog.askdirectory(parent=fetchexpense_gui)
            excel_writer = pd.ExcelWriter(folder_path+'/'+'Expenditure.xlsx', engine='xlsxwriter')
            df.to_excel(excel_writer,sheet_name='Expense Report',startrow=2,index=False)

            # Get the xlsxwriter workbook and worksheet objects
            workbook = excel_writer.book
            worksheet = excel_writer.sheets['Expense Report']
            worksheet.merge_range('C1:G2', 'Expense Report of '+str(session_user_name), workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter','bg_color': '#FFFF00','font_color': 'red', 'font_size': 16}))
            excel_writer.close()
            print("Data exported to 'Expenditure.xlsx'")
            messagebox.showinfo("info","Report Downloaded Successfully",parent=fetchexpense_gui)

        global fetchexpense_gui
        fetchexpense_gui = Frame(activewindow)
        #fetchexpense_gui.title("Expense Details")
        #fetchexpense_gui.configure(bg='#000000')
        #fetchexpense_gui.geometry("900x700")

        l8=Label(fetchexpense_gui,width=60,height=7,font=("century",35),bg="#EDE4E4",text="")
        l8.place(x=450,y=60)
        l8.pack()
        l7=Label(fetchexpense_gui,width=100,height=10,font=("century",35),bg="#EDE4E4",text="")
        l7.place(x=-455,y=410)
        l7.pack()
        
        l1=Label(fetchexpense_gui,font=("cooper black",17),bg="#EDE4E4",fg="#755050",text="Enter Below Filter Values :")
        l1.place(x=70,y=150)
        #l1.pack()
        l2=Label(fetchexpense_gui,font=("adobe clean",15),bg="#EDE4E4",fg="#755050",text="Start Date( yyyy-mm-dd )")
        l2.place(x=90,y=200)
        #l2.pack()
        exp_startdate=StringVar()
        e2=DateEntry(fetchexpense_gui,font=("adobe clean",15),textvariable=exp_startdate,selectmode='day',date_pattern="yyyy-mm-dd")
        e2.place(x=350,y=200,height=27,width=165)
        l3=Label(fetchexpense_gui,font=("adobe clean",15),bg="#EDE4E4",fg="#755050",text="End Date( yyyy-mm-dd )")
        l3.place(x=90,y=250)
        exp_enddate=StringVar()
        e3=DateEntry(fetchexpense_gui,font=("adobe clean",15),textvariable=exp_enddate,date_pattern="yyyy-mm-dd",selectmode='day')
        e3.place(x=350,y=250,height=27,width=165)
        l4=Label(fetchexpense_gui,font=("adobe clean",15),bg="#EDE4E4",fg="#755050",text="Category")
        l4.place(x=90,y=300)
        exp_category=StringVar()
        exp_category.set("choose categoty")
        e4=OptionMenu(fetchexpense_gui, exp_category,"Housing", "Transportation","Food","Personal Care","Entertainment","Utilities","Debts and Loans","Insurance","Savings","Gifts and Donations","Miscellaneous")
        e4.place(x=350,y=300,height=27,width=165)
        
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11)) # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13,'bold')) # Modify the font of the headings
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders
        table = ttk.Treeview(fetchexpense_gui,columns=('Category','Amount','Description','Date'),show='headings',style="mystyle.Treeview")
        table.column("# 1",anchor=CENTER, stretch=NO, width=100)
        table.column("# 2",anchor=CENTER, stretch=NO, width=100)
        table.column("# 3",anchor=CENTER, stretch=NO, width=100)
        table.column("# 4",anchor=CENTER, stretch=NO, width=100)
        table.heading('Category',text='Category')
        table.heading('Amount',text='Amount')
        table.heading('Description',text='Description')
        table.heading('Date',text='Date')
        table.pack(fill='both',expand=True)
        table.place(x=100,y=410)
       
        b8=Button(fetchexpense_gui,text="Proceed",bg='#8DC2B7', font=("", 17, "bold"), bd=0, fg='#000000',
                                  cursor='hand2', borderwidth=0,activebackground='#32cf8e',command=viewallitems)
        b8.place(x=100,y=350)
        b9=Button(fetchexpense_gui,text="Download",bg='#8DC2B7', font=("", 17, "bold"), bd=0, fg='#000000',
                                  cursor='hand2', borderwidth=0,activebackground='#32cf8e',command=export_to_excel)
        b9.place(x=550,y=650)
        l6=Label(fetchexpense_gui,width=60,font=("Garamond",35),bg="#429181",fg="#E0F3EF",text="FILTER YOUR EXPENSE").place(x=-200,y=0)
        
        back_button=Button(fetchexpense_gui,text=" Go Back",bg='#8DC2B7', font=("", 17, "bold"), bd=0, fg='#000000',
                                  cursor='hand2',borderwidth=0, activebackground='#32cf8e',command=dashboard_frame)
        back_button.place(x=0,y=80)
    
    def fetchincomewindow():

        def view():
            print(exp_source.get())
            print(exp_startdate.get())
            print(exp_enddate.get())
            conn=sqlite3.connect("financeflow.db")
            cur=conn.cursor()
            if exp_source.get():
                cur.execute("SELECT source,amount,optional_notes,date FROM incometable where user_id=? and source=? and(date(date) between date(?) and date(?) or date(date)=date(?) or date(date)=date(?))",(session_user_id,exp_source.get(),exp_startdate.get(),exp_enddate.get(),exp_startdate.get(),exp_enddate.get()))
            else:
                cur.execute("SELECT source,amount,optional_notes,date FROM incometable where user_id=? and (date(date) between date(?) and date(?) or date(date)=date(?) or date(date)=date(?))",(session_user_id,exp_startdate.get(),exp_enddate.get(),exp_startdate.get(),exp_enddate.get()))
            rows=cur.fetchall()
            conn.commit()
            conn.close()
            print(rows)
            return rows
        
        def graph(rows):
            print(rows)
            data = {'amount': [int(i[1]) for i in rows],
            'date': [datetime.datetime.strptime(i[3], '%Y-%m-%d').strftime('%Y-%m') for i in rows],
            'Category': [str(i[0]) for i in rows]
            }  
            df = pd.DataFrame(data)
            agg_data = df.groupby(['Category','date'])['amount'].sum().reset_index()
            agg_data=agg_data.sort_values(by=['date'])
            sns.set(style="whitegrid")  # Set the Seaborn style
            plt.figure(figsize=(6, 4))  # Set the figure size
            # Create the bar graph
            plt.title("Bar Graph")  # Add a title
            sns.barplot(data=agg_data, x='date', y='amount', hue='Category')
            canvas = FigureCanvasTkAgg(plt.gcf(), master=fetchincome_gui)
            canvas.get_tk_widget().place(x=700,y=200)
            toolbar = NavigationToolbar2Tk(canvas, fetchincome_gui) 
            toolbar.update()
            toolbar.place(x=800,y=630)
        
        def viewallitems():
            for item in table.get_children():
                table.delete(item)
            rows=view()
            if rows:
                for row in rows:
                    print(row)
                    a=str(row[0])
                    b=str(row[1])
                    c=str(row[2])
                    d=str(row[3])
                    f= (a,b,c,d)
                    table.insert(parent='',index=0,values=f)
            else:
                messagebox.showinfo("No Data","There is no data for the applied filters",parent=fetchincome_gui)
            e2.delete(0,END)
            e3.delete(0,END)
            e4.delete(0,END)
            graph(rows)

        def export_to_excel():
            # Get data from TreeView
            data = []
            for item in table.get_children():
                values = table.item(item, 'values')
                data.append(values)

            # Create a Pandas DataFrame
            
            df = pd.DataFrame(data, columns=['Source','Amount','Description','Date'])
            

            # Export to Excel
            folder_path = filedialog.askdirectory(parent=fetchincome_gui)
            excel_writer = pd.ExcelWriter(folder_path+'/'+'Income.xlsx', engine='xlsxwriter')
            df.to_excel(excel_writer,sheet_name='Income Report',startrow=3,index=False)

            # Get the xlsxwriter workbook and worksheet objects
            workbook = excel_writer.book
            worksheet = excel_writer.sheets['Income Report']
            worksheet.merge_range('C1:G3', 'Income Report of '+str(session_user_name), workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter','bg_color': '#FFFF00','font_color': '#008000', 'font_size': 16}))
            excel_writer.close()
            print("Data exported to 'income.xlsx'")
            messagebox.showinfo("info","Report Downloaded Successfully",parent=fetchincome_gui)

        global fetchincome_gui
        fetchincome_gui = Frame(activewindow)
        #fetchincome_gui.title("Expense Details")
        #fetchincome_gui.configure(bg='#000000')
        #fetchincome_gui.geometry("900x700")

        l8=Label(fetchincome_gui,width=60,height=7,font=("century",35),bg="#EDE4E4",text="")
        l8.place(x=450,y=60)
        l8.pack()
        l7=Label(fetchincome_gui,width=100,height=10,font=("century",35),bg="#EDE4E4",text="")
        l7.place(x=-455,y=410)
        l7.pack()
        
        l1=Label(fetchincome_gui,font=("cooper black",17),bg="#EDE4E4",fg="#755050",text="Enter Below Filter Values :")
        l1.place(x=70,y=150)
        #l1.pack()
        l2=Label(fetchincome_gui,font=("adobe clean",15),bg="#EDE4E4",fg="#755050",text="Start Date( yyyy-mm-dd )")
        l2.place(x=90,y=200)
        #l2.pack()
        exp_startdate=StringVar()
        e2=DateEntry(fetchincome_gui,font=("adobe clean",15),textvariable=exp_startdate,selectmode='day',date_pattern="yyyy-mm-dd")
        e2.place(x=350,y=200,height=27,width=165)
        l3=Label(fetchincome_gui,font=("adobe clean",15),bg="#EDE4E4",fg="#755050",text="End Date( yyyy-mm-dd )")
        l3.place(x=90,y=250)
        exp_enddate=StringVar()
        e3=DateEntry(fetchincome_gui,font=("adobe clean",15),textvariable=exp_enddate,date_pattern="yyyy-mm-dd",selectmode='day')
        e3.place(x=350,y=250,height=27,width=165)
        l4=Label(fetchincome_gui,font=("adobe clean",15),bg="#EDE4E4",fg="#755050",text="Source")
        l4.place(x=90,y=300)
        exp_source=StringVar()
        e4=Entry(fetchincome_gui,font=("adobe clean",15),textvariable=exp_source)
        e4.place(x=350,y=300,height=27,width=165)
        
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11)) # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13,'bold')) # Modify the font of the headings
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders
        table = ttk.Treeview(fetchincome_gui,columns=('Source','Amount','Description','Date'),show='headings',style="mystyle.Treeview")
        table.column("# 1",anchor=CENTER, stretch=NO, width=100)
        table.column("# 2",anchor=CENTER, stretch=NO, width=100)
        table.column("# 3",anchor=CENTER, stretch=NO, width=100)
        table.column("# 4",anchor=CENTER, stretch=NO, width=100)
        table.heading('Source',text='Source')
        table.heading('Amount',text='Amount')
        table.heading('Description',text='Description')
        table.heading('Date',text='Date')
        table.pack(fill='both',expand=True)
        table.place(x=100,y=410)
        
        
        b8=Button(fetchincome_gui,text="Proceed",bg='#8DC2B7', font=("", 17, "bold"), bd=0, fg='#000000',
                                  cursor='hand2', borderwidth=0,activebackground='#32cf8e',command=viewallitems)
        b8.place(x=100,y=350)
        b9=Button(fetchincome_gui,text="Download",bg='#8DC2B7', font=("", 17, "bold"), bd=0, fg='#000000',
                                  cursor='hand2', borderwidth=0,activebackground='#32cf8e',command=export_to_excel)
        b9.place(x=550,y=650)
        l6=Label(fetchincome_gui,width=60,font=("Garamond",35),bg="#429181",fg="#E0F3EF",text="FILTER YOUR INCOME").place(x=-200,y=0)
        
        back_button=Button(fetchincome_gui,text=" Go Back",bg='#8DC2B7', font=("", 17, "bold"), bd=0, fg='#000000',
                                  cursor='hand2',borderwidth=0, activebackground='#32cf8e',command=dashboard_frame)
        back_button.place(x=0,y=80)

    def dahboardwindow1():
    
        def connect1():
            conn=sqlite3.connect("financeflow.db")
            cur=conn.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS expensetable(id INTEGER PRIMARY KEY,itemname TEXT,date TEXT,cost TEXT,optional_notes TEXT,user_id INTEGER)")
            conn.commit()
            cur.execute("CREATE TABLE IF NOT EXISTS incometable(id INTEGER PRIMARY KEY,source TEXT,date TEXT,amount TEXT,optional_notes TEXT,user_id INTEGER)")
            conn.commit()
            cur.execute("CREATE TABLE IF NOT EXISTS budgettable(budget_id INTEGER PRIMARY KEY,category TEXT, year INTEGER,month INTEGER,budget INTEGER,user_id INTEGER)")
            conn.commit()
            conn.close()
        connect1()
         
        def totalexpense():
            conn=sqlite3.connect("financeflow.db")
            cur=conn.cursor()
            cur.execute("SELECT sum(cost) FROM expensetable where user_id =?",(session_user_id,))
            row=cur.fetchone()
            conn.commit()
            conn.close()
            return row
        
        def totalmonthlyexpense():
            month = datetime.datetime.now().strftime("%m")
            conn=sqlite3.connect("financeflow.db")
            cur=conn.cursor()
            lastmonth = str(int(datetime.datetime.now().strftime("%m"))-1).zfill(2)
            cur.execute("SELECT sum(cost) FROM expensetable where user_id =? and strftime(?,date)=? and strftime(?,date)=strftime(?,date('now'))",(session_user_id,"%m",lastmonth,"%Y","%Y"))
            row=cur.fetchone()
            conn.commit()
            conn.close()
            return row

        def totalincome():
            conn=sqlite3.connect("financeflow.db")
            cur=conn.cursor()
            cur.execute("SELECT sum(amount) FROM incometable where user_id =?",(session_user_id,))
            row=cur.fetchone()
            conn.commit()
            conn.close()
            return row
        
        def totalmonthlyincome():
            month = datetime.datetime.now().strftime("%m")
            conn=sqlite3.connect("financeflow.db")
            cur=conn.cursor()
            lastmonth = str(int(datetime.datetime.now().strftime("%m"))-1).zfill(2)
            cur.execute("SELECT sum(amount) FROM incometable where user_id =? and strftime(?,date)=? and strftime(?,date)=strftime(?,date('now'))",(session_user_id,"%m",lastmonth,"%Y","%Y"))
            row=cur.fetchone()
            conn.commit()
            conn.close()
            return row
        
        def connect1():
            conn=sqlite3.connect("financeflow.db")
            cur=conn.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS budgettable(budget_id INTEGER PRIMARY KEY,category TEXT, year INTEGER,month INTEGER,budget INTEGER,user_id INTEGER)")
            conn.commit()
            conn.close()
        #connect1()

        def view():
            conn=sqlite3.connect("financeflow.db")
            cur=conn.cursor()
            currentyear = str(int(datetime.datetime.now().strftime("%Y"))).zfill(4)
            cur.execute("SELECT category,year,month,budget FROM budgettable where user_id=? and year =?",(session_user_id,currentyear))
            rows=cur.fetchall()
            conn.commit()
            conn.close()
            return rows
        
        def viewallitems():
            for item in table.get_children():
                table.delete(item)
            rows= view()
            for row in rows:
                a=str(row[0])
                b=str(row[1])
                c=str(row[2])
                d=str(row[3])
                f= (a,b,c,d)
                table.insert(parent='',index=0,values=f)
            graph(rows)

        def graph(rows):
            print(rows)
            data = {'budget': [int(i[3]) for i in rows],
            'date': [str(i[1])+"-"+str(i[2]).zfill(2) for i in rows],
            'Category': [str(i[0]) for i in rows]
            }  
            df = pd.DataFrame(data)
            agg_data = df.groupby(['Category','date'])['budget'].sum().reset_index()
            agg_data=agg_data.sort_values(by=['date'])
            sns.set(style="whitegrid")  # Set the Seaborn style
            plt.figure(figsize=(5, 3))  # Set the figure size
            # Create the bar graph
            plt.title("Bar Graph")  # Add a title
            sns.barplot(data=agg_data, x='date', y='budget', hue='Category')
            canvas = FigureCanvasTkAgg(plt.gcf(), master=bodyFrame5)
            canvas.get_tk_widget().place(x=510,y=0)
            #toolbar = NavigationToolbar2Tk(canvas, bodyFrame5)
            #toolbar.update()
            #toolbar.place(x=800,y=630)
        
        def refresh():
            viewallitems()
            total_expense,lastmonth_expense,total_income,lastmonth_income=None,None,None,None
            total_expense = Label(bodyFrame1,bg='#e21f26', font=("", 25, "bold"),text="$"+str(totalexpense()[0]) if totalexpense()[0]!=None else "$0")
            total_expense.place(x=250, y=45)
            lastmonth_expense = Label(bodyFrame2,bg='#e21f26', font=("", 25, "bold"),text="$"+str(totalmonthlyexpense()[0]) if totalmonthlyexpense()[0]!=None else "$0")
            lastmonth_expense.place(x=250, y=45)
            total_income = Label(bodyFrame3, bg='#009aa5', font=("", 25, "bold"),text="$"+str(totalincome()[0]) if totalincome()[0]!=None else "$0")
            total_income.place(x=250, y=45)
            lastmonth_income = Label(bodyFrame4, bg='#009aa5', font=("", 25, "bold"),text="$"+str(totalmonthlyincome()[0]) if totalmonthlyincome()[0]!=None else "$0")
            lastmonth_income.place(x=250, y=45)

        def close_window():
             activewindow.destroy()

        global dashboard_gui
        dashboard_gui = Frame(activewindow)
        #dashboard_gui.place(x=0, y=0, width=1366, height=768)
        

        
        #activewindow=dashboard_gui
        #dashboard_gui.title("Finance Dashboard")
        #dashboard_gui.configure(bg='#1abeff')
        #dashboard_gui.geometry("900x700")
        
        # ==============================================================================
        # ================== HEADER ====================================================
        # ==============================================================================
        header = Frame(activewindow, bg='#009df4')
        header.place(x=300, y=0, width=1070, height=60)
        #header.pack()
        

        logout_text = Button(header, text="Logout", bg='#32cf8e', font=("", 13, "bold"), bd=0, fg='white',
                                  cursor='hand2', activebackground='#32cf8e',command=close_window)
        logout_text.place(x=950, y=15)
        #logout_text.pack()



        # ==============================================================================
        # ================== SIDEBAR ===================================================
        # ==============================================================================
        sidebar = Frame(activewindow, bg='#ffffff')
        sidebar.place(x=0, y=0, width=300, height=750)
        #sidebar.pack()

        refresh_text = Button(sidebar, text="Refresh", bg='#32cf8e', font=("", 13, "bold"), bd=0, fg='white',
                                  cursor='hand2', activebackground='#32cf8e',command=refresh)
        refresh_text.place(x=55, y=600)
        #refresh_text.pack()
        
        # =============================================================================
        # ============= BODY ==========================================================
        # =============================================================================
        heading = Label(activewindow, text='Dashboard', font=("", 15, "bold"), fg='#0064d3', bg='#eff5f6')
        heading.place(x=325, y=70)
        #heading.pack()
        

        # body frame 1
        bodyFrame5 = Frame(activewindow, bg='#ffffff')
        bodyFrame5.place(x=328, y=400, width=1040, height=350)
        #bodyFrame5.pack()
        

        # body frame 2
        bodyFrame1 = Frame(activewindow, bg='#e21f26')
        bodyFrame1.place(x=328, y=110, width=510, height=110)
        #bodyFrame1.pack()

         # body frame 2
        bodyFrame2 = Frame(activewindow, bg='#e21f26')
        bodyFrame2.place(x=328, y=240, width=510, height=110)
        #bodyFrame2.pack()
        

        # body frame 3
        bodyFrame3 = Frame(activewindow, bg='#009aa5')
        bodyFrame3.place(x=880, y=110, width=510, height=110)
        #bodyFrame3.pack()

        # body frame 3
        bodyFrame4 = Frame(activewindow, bg='#009aa5')
        bodyFrame4.place(x=880, y=240, width=510, height=110)
        #bodyFrame4.pack()

        # ==============================================================================
        # ================== SIDEBAR ===================================================
        # ==============================================================================

        # logo
        logoImage = PhotoImage(file='images/hyy.png')
        logo = Label(sidebar, image=logoImage, bg='#ffffff')
        logo.image=logoImage
        logo.place(x=70, y=30)
        
        

       


        name = "Hello, " + profilename
        brandName = Label(sidebar, text=name, bg='#ffffff', font=("", 15, "bold"))
        brandName.place(x=80, y=150)

       
        dashboardImage = ImageTk.PhotoImage(file='images/dashboard-icon.png')
        dashboard = Label(sidebar, image=dashboardImage, bg='#ffffff')
        dashboard.image=dashboardImage
        dashboard.place(x=35, y=239)
       


        dashboard_text = Button(sidebar, text="Dashboard", bg='#ffffff', font=("", 13, "bold"), bd=0,
                                     cursor='hand2', activebackground='#ffffff')
        dashboard_text.place(x=80, y=237)


        # expense
        expenseImage = ImageTk.PhotoImage(file='images/expense.png')
        expense = Label(sidebar, image=expenseImage, bg='#ffffff')
        expense.image=expenseImage
        expense.place(x=35, y=290)


        expense_text = Button(sidebar, text="Expenses", bg='#ffffff', font=("", 13, "bold"), bd=0,
                                  cursor='hand2', activebackground='#ffffff',command=expense_frame)
        expense_text.place(x=80, y=295)

        # income
        incomeImage = ImageTk.PhotoImage(file='images/income.png')
        income = Label(sidebar, image=incomeImage, bg='#ffffff')
        income.image=incomeImage
        income.place(x=35, y=352)

        income_text = Button(sidebar, text="Income", bg='#ffffff', font=("", 13, "bold"), bd=0,
                                    cursor='hand2', activebackground='#ffffff',command=income_frame)
        income_text.place(x=80, y=352)

        # budget
        BudgetImage = ImageTk.PhotoImage(file='images/budget.png')
        Budget = Label(sidebar, image=BudgetImage, bg='#ffffff')
        Budget.image=BudgetImage
        Budget.place(x=25, y=402)

        Budget_text = Button(sidebar, text="Budget", bg='#ffffff', font=("", 13, "bold"), bd=0,
                                cursor='hand2', activebackground='#ffffff',command=budget_frame)
        Budget_text.place(x=85, y=412)

        # Filter expense
        BudgetImage = ImageTk.PhotoImage(file='images/budget.png')
        Budget = Label(sidebar, image=BudgetImage, bg='#ffffff')
        Budget.image=BudgetImage
        Budget.place(x=25, y=452)

        Budget_text = Button(sidebar, text="Filter Expenses", bg='#ffffff', font=("", 13, "bold"), bd=0,
                                cursor='hand2', activebackground='#ffffff',command=fetchexpense_frame)
        Budget_text.place(x=85, y=462)


        # Filter income
        BudgetImage = ImageTk.PhotoImage(file='images/budget.png')
        Budget = Label(sidebar, image=BudgetImage, bg='#ffffff')
        Budget.image=BudgetImage
        Budget.place(x=25, y=502)

        Budget_text = Button(sidebar, text="Filter Income", bg='#ffffff', font=("", 13, "bold"), bd=0,
                                cursor='hand2', activebackground='#ffffff',command=fetchincome_frame)
        Budget_text.place(x=85, y=512)

        # =============================================================================
        # ============= BODY ==========================================================
        # =============================================================================

        # Body Frame 5
    

        # Body Frame 1
        total_expense = Label(bodyFrame1,bg='#e21f26', font=("", 25, "bold"),text="$"+str(totalexpense()[0]) if totalexpense()[0]!=None else "$0")
        total_expense.place(x=250, y=45)

        totalExpenseImage = ImageTk.PhotoImage(file='images/earn3.png')
        totalExpense = Label(bodyFrame1, image=totalExpenseImage, bg='#e21f26')
        totalExpense.image=totalExpenseImage
        totalExpense.place(x=440, y=0)

        totalExpense_label = Label(bodyFrame1, text="Total Expenses", bg='#e21f26', font=("", 12, "bold"),
                                       fg='white')
        totalExpense_label.place(x=5, y=5)

         # Body Frame 2
        lastmonth_expense = Label(bodyFrame2,bg='#e21f26', font=("", 25, "bold"),text="$"+str(totalmonthlyexpense()[0]) if totalmonthlyexpense()[0]!=None else "$0")
        lastmonth_expense.place(x=250, y=45)

        lastmonth_ExpenseImage = ImageTk.PhotoImage(file='images/earn3.png')
        lastmonth_Expense = Label(bodyFrame2, image=totalExpenseImage, bg='#e21f26')
        lastmonth_Expense.image=lastmonth_ExpenseImage
        lastmonth_Expense.place(x=440, y=0)

        lastmonth_expense_label = Label(bodyFrame2, text="Last Month Expense", bg='#e21f26', font=("", 12, "bold"),
                                       fg='white')
        lastmonth_expense_label.place(x=5, y=5)

        # Body Frame 3
        total_income = Label(bodyFrame3, bg='#009aa5', font=("", 25, "bold"),text="$"+str(totalincome()[0]) if totalincome()[0]!=None else "$0")
        total_income.place(x=250, y=45)

        #  icon
        total_incomeImage = ImageTk.PhotoImage(file='images/earn3.png')
        total_income_Image = Label(bodyFrame3, image=total_incomeImage, bg='#009aa5')
        total_income_Image.image=total_incomeImage
        total_income_Image.place(x=415, y=0)

        total_income_label = Label(bodyFrame3, text="Total Income", bg='#009aa5', font=("", 12, "bold"),
                                      fg='white')
        total_income_label.place(x=5, y=5)

         # Body Frame 4
        lastmonth_income = Label(bodyFrame4, bg='#009aa5', font=("", 25, "bold"),text="$"+str(totalmonthlyincome()[0]) if totalmonthlyincome()[0]!=None else "$0")
        lastmonth_income.place(x=250, y=45)

        #  icon
        lastmonth_incomeImage = ImageTk.PhotoImage(file='images/earn3.png')
        lastmonth_income_Image = Label(bodyFrame4, image= lastmonth_incomeImage, bg='#009aa5')
        lastmonth_income_Image.image= lastmonth_incomeImage
        lastmonth_income_Image.place(x=415, y=0)

        lastmonth_income_label = Label(bodyFrame4, text="Last Month Income", bg='#009aa5', font=("", 12, "bold"),
                                      fg='white')
        lastmonth_income_label.place(x=5, y=5)


        style = ttk.Style()
        #style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11)) # Modify the font of the body
        #style.configure("mystyle.Treeview.Heading", font=('Calibri', 13,'bold')) # Modify the font of the headings
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders
        style.configure("Treeview",background="#D3D3D3", foreground="black", borderwidth=2, relief="solid", rowheight=25,fieldbackground="#D3D3D3")

        # Change selected row color
        style.map("Treeview", background=[('selected', '#347083')])

        # Configure the Treeview columns
        #style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'), foreground="white",background="#2E5266")

        # Change heading border color
        style.map("Treeview.Heading",relief=[('active', 'groove')])
        table = ttk.Treeview(bodyFrame5,columns=('Category','Year','Month','Budget'),show='headings',style="mystyle.Treeview")
        table.column("# 1",anchor=CENTER, stretch=NO, width=100)
        table.column("# 2",anchor=CENTER, stretch=NO, width=100)
        table.column("# 3",anchor=CENTER, stretch=NO, width=100)
        table.column("# 4",anchor=CENTER, stretch=NO, width=100)
        table.heading('Category',text='Category')
        table.heading('Year',text='Year')
        table.heading('Month',text='Month')
        table.heading('Budget',text='Budget')
        table.pack(fill='both',expand=True)
        table.place(x=20,y=20)
        viewallitems()

        
           



    def dashboard_frame():
            gui.pack_forget()
            income_gui.pack_forget()
            budget_gui.pack_forget()
            fetchexpense_gui.pack_forget()
            fetchincome_gui.pack_forget()
            dashboard_gui.pack()
            

    def income_frame():
            dashboard_gui.pack_forget()
            income_gui.pack()

    def expense_frame():
            dashboard_gui.pack_forget()
            gui.pack()

    def budget_frame():
            dashboard_gui.pack_forget()
            budget_gui.pack()

    def fetchexpense_frame():
            dashboard_gui.pack_forget()
            fetchexpense_gui.pack()

    def fetchincome_frame():
            dashboard_gui.pack_forget()
            fetchincome_gui.pack()

    global activewindow
    root= Tk()
    activewindow=root
    root.geometry("1366x768")
    root.config(background='#eff5f6')
    # Window Icon Photo
    icon = PhotoImage(file='images\\pic-icon.png')
    root.iconphoto(True, icon)
    root.title("Finance Flow")
    
    dahboardwindow1()
    expensewindow1()
    incomewindow()
    budgetwindow()
    fetchexpensewindow()
    fetchincomewindow()
    dashboard_frame()
    root.mainloop()

def registration_page():
        def show1():
            hide_button1 = Button( lgn_frame, image= hide_image1, command=hide1, relief=FLAT,
                                    activebackground="white"
                                    , borderwidth=0, background="white", cursor="hand1")
            hide_button1.place(x=860, y=378)
            password_entry.config(show='')
        def hide1():
            show_button1 = Button( lgn_frame, image= show_image1, command=show1, relief=FLAT,
                                    activebackground="white"
                                    , borderwidth=0, background="white", cursor="hand1")
            show_button1.place(x=860, y=378)
            password_entry.config(show='*')
        def show2():
            hide_button2 = Button( lgn_frame, image= hide_image2, command=hide2, relief=FLAT,
                                    activebackground="white"
                                    , borderwidth=0, background="white", cursor="hand2")
            hide_button2.place(x=860, y=447)
            confirm_password_entry.config(show='')
        def hide2():
            show_button2 = Button( lgn_frame, image= show_image2, command=show2, relief=FLAT,
                                    activebackground="white"
                                    , borderwidth=0, background="white", cursor="hand2")
            show_button2.place(x=860, y=447)
            confirm_password_entry.config(show='*')
        
        def register():
            a = login_name.get()
            b = login_username.get()
            c = login_password.get()
            d = login_confirm_password.get()
            if c==d and c!="" and len(c)>5 and a!="" and b!="":
                conn=sqlite3.connect("financeflow.db")
                cur=conn.cursor()
                cur.execute("SELECT name,username FROM users where name=? and username=?",(a,b))
                rows=cur.fetchall()
                conn.commit()
                conn.close()
                if rows:
                    messagebox.showinfo(':)', 'Username already taken',parent=register_window)
                else:
                    adduser(a,b,c)
                    messagebox.showinfo(':)', 'Registration Successful',parent=register_window)
                    register_window.destroy() 
            else :
                if(a=="" or b=="" or c=="" or d==""):
                    messagebox.showinfo('oops something wrong', 'Field should not be empty',parent=register_window)
                else:
                    messagebox.showinfo('oops something wrong', 'Both passwords should be same! \nPassword should contain atleast 6 characters',parent=register_window)
            name_entry.delete(0,END)
            username_entry.delete(0,END)
            password_entry.delete(0,END)
            confirm_password_entry.delete(0,END)
            

        register_window = Toplevel(window)
        register_window.geometry('1166x718')
        register_window.resizable(0, 0)
        register_window.state('zoomed')
        register_window.title('SignUp Page')

        # ========================================================================
        # ============================background image============================
        # ========================================================================
        bg_frame = Image.open('images\\background1.png')
        photo = ImageTk.PhotoImage( bg_frame)
        bg_panel = Label(register_window, image=photo)
        bg_panel.image = photo
        bg_panel.pack(fill='both', expand='yes')

        # ====== Login Frame =========================
        lgn_frame = Frame(register_window, bg='#040405', width=950, height=600)
        lgn_frame.place(x=200, y=70)

        # ========================================================================
        # ========================================================
        # ========================================================================
        txt = "WELCOME"
        heading = Label( lgn_frame, text= txt, font=('cooper black', 25, "bold"), bg="#040405",
                            fg='white',
                            bd=5,
                            relief=FLAT)
        heading.place(x=80, y=30, width=300, height=30)

        # ========================================================================
        # ============ Left Side Image ================================================
        # ========================================================================
        side_image = Image.open('images\\vector.png')
        photo = ImageTk.PhotoImage( side_image)
        side_image_label = Label( lgn_frame, image=photo, bg='#040405')
        side_image_label.image = photo
        side_image_label.place(x=5, y=200)

        # ========================================================================
        # ============ Sign In Image =============================================
        # ========================================================================
        sign_in_image = Image.open('images\\hyy.png')
        photo = ImageTk.PhotoImage( sign_in_image)
        sign_in_image_label = Label( lgn_frame, image=photo, bg='#040405')
        sign_in_image_label.image = photo
        sign_in_image_label.place(x=650, y=50)

        # ========================================================================
        # ============ Sign Up label =============================================
        # ========================================================================
        sign_in_label = Label(lgn_frame, text="Sign Up", bg="#040405", fg="white",
                                    font=("yu gothic ui", 17, "bold"))
        sign_in_label.place(x=650, y=150)

        # ========================================================================
        # ============================name====================================
        # ========================================================================
        name_label = Label( lgn_frame, text="name", bg="#040405", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        name_label.place(x=550, y=210)
        login_name=StringVar()
        name_entry = Entry( lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#6b6a69",
                                    font=("yu gothic ui ", 12, "bold"),textvariable=login_name,insertbackground = '#6b6a69')
        name_entry.place(x=580, y=245, width=270)

        name_line = Canvas( lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        name_line.place(x=550, y=269)
        # ===== Username icon =========
        name_icon = Image.open('images\\username_icon.png')
        photo = ImageTk.PhotoImage(name_icon)
        name_icon_label = Label( lgn_frame, image=photo, bg='#040405')
        name_icon_label.image = photo
        name_icon_label.place(x=550, y=242)

        # ========================================================================
        # ============================username====================================
        # ========================================================================
        username_label = Label( lgn_frame, text="Username", bg="#040405", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        username_label.place(x=550, y=272)
        login_username=StringVar()
        username_entry = Entry( lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#6b6a69",
                                    font=("yu gothic ui ", 12, "bold"),textvariable=login_username,insertbackground = '#6b6a69')
        username_entry.place(x=580, y=307, width=270)

        username_line = Canvas( lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        username_line.place(x=550, y=334)
        # ===== Username icon =========
        username_icon = Image.open('images\\username_icon.png')
        photo = ImageTk.PhotoImage( username_icon)
        username_icon_label = Label( lgn_frame, image=photo, bg='#040405')
        username_icon_label.image = photo
        username_icon_label.place(x=550, y=307)

        # ========================================================================
        # ============================login button================================
        # ========================================================================
        lgn_button = Image.open('images\\btn1.png')
        photo = ImageTk.PhotoImage( lgn_button)
        lgn_button_label = Label( lgn_frame, image=photo, bg='#040405')
        lgn_button_label.image = photo
        lgn_button_label.place(x=550, y=510)
        login = Button( lgn_button_label, text='SIGNUP', font=("yu gothic ui", 13, "bold"), width=25, bd=0,
                            bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white',command=register)
        login.place(x=20, y=10)

        
        
        # ========================================================================
        # ============================password====================================
        # ========================================================================
        password_label = Label( lgn_frame, text="Password", bg="#040405", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        password_label.place(x=550, y=338)
        login_password = StringVar()
        password_entry = Entry( lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#6b6a69",
                                    font=("yu gothic ui", 12, "bold"),textvariable= login_password,show='*',insertbackground = '#6b6a69')
        password_entry.place(x=580, y=374, width=244)

        password_line = Canvas( lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        password_line.place(x=550, y=398)
        # ======== Password icon ================
        password_icon = Image.open('images\\password_icon.png')
        photo = ImageTk.PhotoImage( password_icon)
        password_icon_label = Label( lgn_frame, image=photo, bg='#040405')
        password_icon_label.image = photo
        password_icon_label.place(x=550, y=372)
        # ========= show/hide password ==================================================================
        show_image1 = ImageTk.PhotoImage \
        (file='images\\show.png')

        hide_image1 = ImageTk.PhotoImage \
            (file='images\\hide.png')

        show_button1 = Button( lgn_frame, image= show_image1, command= show1, relief=FLAT,
                                activebackground="white"
                                , borderwidth=0, background="white", cursor="hand1")
        show_button1.place(x=860, y=378)


        # ========================================================================
        # ============================confirm_password====================================
        # ========================================================================
        confirm_password_label = Label( lgn_frame, text="confirm_password", bg="#040405", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        confirm_password_label.place(x=550, y=405)
        login_confirm_password = StringVar()
        confirm_password_entry = Entry( lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#6b6a69",
                                    font=("yu gothic ui", 12, "bold"),textvariable= login_confirm_password,show='*',insertbackground = '#6b6a69')
        confirm_password_entry.place(x=580, y=441, width=244)

        confirm_password_line = Canvas( lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        confirm_password_line.place(x=550, y=467)
        # ======== confirm_password icon ================
        confirm_password_icon = Image.open('images\\password_icon.png')
        photo = ImageTk.PhotoImage( confirm_password_icon)
        confirm_password_icon_label = Label( lgn_frame, image=photo, bg='#040405')
        confirm_password_icon_label.image = photo
        confirm_password_icon_label.place(x=550, y=439)

        show_image2 = ImageTk.PhotoImage \
        (file='images\\show.png')

        hide_image2 = ImageTk.PhotoImage \
            (file='images\\hide.png')

        show_button2 = Button( lgn_frame, image= show_image2, command= show2,relief=FLAT,
                                activebackground="white"
                                , borderwidth=0, background="white", cursor="hand2")
        show_button2.place(x=860, y=447)

def forgot_password_page():
        def show1():
            hide_button1 = Button( lgn_frame, image= hide_image1, command=hide1, relief=FLAT,
                                    activebackground="white"
                                    , borderwidth=0, background="white", cursor="hand1")
            hide_button1.place(x=860, y=378)
            password_entry.config(show='')
        def hide1():
            show_button1 = Button( lgn_frame, image= show_image1, command=show1, relief=FLAT,
                                    activebackground="white"
                                    , borderwidth=0, background="white", cursor="hand1")
            show_button1.place(x=860, y=378)
            password_entry.config(show='*')
        def show2():
            hide_button2 = Button( lgn_frame, image= hide_image2, command=hide2, relief=FLAT,
                                    activebackground="white"
                                    , borderwidth=0, background="white", cursor="hand2")
            hide_button2.place(x=860, y=447)
            confirm_password_entry.config(show='')
        def hide2():
            show_button2 = Button( lgn_frame, image= show_image2, command=show2, relief=FLAT,
                                    activebackground="white"
                                    , borderwidth=0, background="white", cursor="hand2")
            show_button2.place(x=860, y=447)
            confirm_password_entry.config(show='*')
        
        def forgot_password():
            a = login_name.get()
            b = login_username.get()
            c = login_password.get()
            d = login_confirm_password.get()
            if c==d and c!="" and len(c)>5 and a!="" and b!="":
                conn=sqlite3.connect("financeflow.db")
                cur=conn.cursor()
                cur.execute("SELECT name,username FROM users where name=? and username=?",(a,b))
                rows=cur.fetchall()
                conn.commit()
                conn.close()
                if rows:
                    updateuser(a,b,c)
                    messagebox.showinfo(':)', 'Password Successfully Updated',parent=register1_window)
                    register1_window.destroy() 
                else:
                    messagebox.showinfo(':)', 'Please Enter correct name and username',parent=register1_window)
                
                     
            else :
                if(a=="" or b=="" or c=="" or d==""):
                    messagebox.showinfo('oops something wrong', 'Field should not be empty',parent=register1_window)
                else:
                    messagebox.showinfo('oops something wrong', 'Both passwords should be same! \nPassword should contain atleast 6 characters',parent=register1_window)
            name_entry.delete(0,END)
            username_entry.delete(0,END)
            password_entry.delete(0,END)
            confirm_password_entry.delete(0,END)

        register1_window = Toplevel(window)
        register1_window.geometry('1166x718')
        register1_window.resizable(0, 0)
        register1_window.state('zoomed')
        register1_window.title('Update Password')

        # ========================================================================
        # ============================background image============================
        # ========================================================================
        bg_frame = Image.open('images\\background1.png')
        photo = ImageTk.PhotoImage( bg_frame)
        bg_panel = Label(register1_window, image=photo)
        bg_panel.image = photo
        bg_panel.pack(fill='both', expand='yes')

        # ====== Login Frame =========================
        lgn_frame = Frame(register1_window, bg='#040405', width=950, height=600)
        lgn_frame.place(x=200, y=70)

        # ========================================================================
        # ========================================================
        # ========================================================================
        txt = "WELCOME"
        heading = Label( lgn_frame, text= txt, font=('cooper black', 25, "bold"), bg="#040405",
                            fg='white',
                            bd=5,
                            relief=FLAT)
        heading.place(x=80, y=30, width=300, height=30)

        # ========================================================================
        # ============ Left Side Image ================================================
        # ========================================================================
        side_image = Image.open('images\\fgt_pwd.jpg')
        photo = ImageTk.PhotoImage( side_image)
        side_image_label = Label( lgn_frame, image=photo, bg='#040405')
        side_image_label.image = photo
        side_image_label.place(x=5, y=200)

        # ========================================================================
        # ============ Sign In Image =============================================
        # ========================================================================
        sign_in_image = Image.open('images\\reset_pwd.png')
        photo = ImageTk.PhotoImage( sign_in_image)
        sign_in_image_label = Label( lgn_frame, image=photo, bg='#040405')
        sign_in_image_label.image = photo
        sign_in_image_label.place(x=650, y=50)

        # ========================================================================
        # ============ Sign Up label =============================================
        # ========================================================================
        sign_in_label = Label(lgn_frame, text="Update Password", bg="#040405", fg="white",
                                    font=("yu gothic ui", 17, "bold"))
        sign_in_label.place(x=600, y=150)

        # ========================================================================
        # ============================name====================================
        # ========================================================================
        name_label = Label( lgn_frame, text="name", bg="#040405", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        name_label.place(x=550, y=210)
        login_name=StringVar()
        name_entry = Entry( lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#6b6a69",
                                    font=("yu gothic ui ", 12, "bold"),textvariable=login_name,insertbackground = '#6b6a69')
        name_entry.place(x=580, y=245, width=270)

        name_line = Canvas( lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        name_line.place(x=550, y=269)
        # ===== Username icon =========
        name_icon = Image.open('images\\username_icon.png')
        photo = ImageTk.PhotoImage(name_icon)
        name_icon_label = Label( lgn_frame, image=photo, bg='#040405')
        name_icon_label.image = photo
        name_icon_label.place(x=550, y=242)

        # ========================================================================
        # ============================username====================================
        # ========================================================================
        username_label = Label( lgn_frame, text="Username", bg="#040405", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        username_label.place(x=550, y=272)
        login_username=StringVar()
        username_entry = Entry( lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#6b6a69",
                                    font=("yu gothic ui ", 12, "bold"),textvariable=login_username,insertbackground = '#6b6a69')
        username_entry.place(x=580, y=307, width=270)

        username_line = Canvas( lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        username_line.place(x=550, y=334)
        # ===== Username icon =========
        username_icon = Image.open('images\\username_icon.png')
        photo = ImageTk.PhotoImage( username_icon)
        username_icon_label = Label( lgn_frame, image=photo, bg='#040405')
        username_icon_label.image = photo
        username_icon_label.place(x=550, y=307)

        # ========================================================================
        # ============================login button================================
        # ========================================================================
        lgn_button = Image.open('images\\btn1.png')
        photo = ImageTk.PhotoImage( lgn_button)
        lgn_button_label = Label( lgn_frame, image=photo, bg='#040405')
        lgn_button_label.image = photo
        lgn_button_label.place(x=550, y=510)
        login = Button( lgn_button_label, text='SUBMIT', font=("yu gothic ui", 13, "bold"), width=25, bd=0,
                            bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white',command=forgot_password)
        login.place(x=20, y=10)

        
        
        # ========================================================================
        # ============================password====================================
        # ========================================================================
        password_label = Label( lgn_frame, text="New Password", bg="#040405", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        password_label.place(x=550, y=338)
        login_password = StringVar()
        password_entry = Entry( lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#6b6a69",
                                    font=("yu gothic ui", 12, "bold"),textvariable= login_password,show="*", insertbackground = '#6b6a69')
        password_entry.place(x=580, y=374, width=244)

        password_line = Canvas( lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        password_line.place(x=550, y=398)
        # ======== Password icon ================
        password_icon = Image.open('images\\password_icon.png')
        photo = ImageTk.PhotoImage( password_icon)
        password_icon_label = Label( lgn_frame, image=photo, bg='#040405')
        password_icon_label.image = photo
        password_icon_label.place(x=550, y=372)
        # ========= show/hide password ==================================================================
        show_image1 = ImageTk.PhotoImage \
        (file='images\\show.png')

        hide_image1 = ImageTk.PhotoImage \
            (file='images\\hide.png')

        show_button1 = Button( lgn_frame, image= show_image1, command= show1, relief=FLAT,
                                activebackground="white"
                                , borderwidth=0, background="white", cursor="hand1")
        show_button1.place(x=860, y=378)


        # ========================================================================
        # ============================confirm_password====================================
        # ========================================================================
        confirm_password_label = Label( lgn_frame, text="confirm_new_password", bg="#040405", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        confirm_password_label.place(x=550, y=405)
        login_confirm_password = StringVar()
        confirm_password_entry = Entry( lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#6b6a69",
                                    font=("yu gothic ui", 12, "bold"),textvariable= login_confirm_password,show="*", insertbackground = '#6b6a69')
        confirm_password_entry.place(x=580, y=441, width=244)

        confirm_password_line = Canvas( lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        confirm_password_line.place(x=550, y=467)
        # ======== confirm_password icon ================
        confirm_password_icon = Image.open('images\\password_icon.png')
        photo = ImageTk.PhotoImage( confirm_password_icon)
        confirm_password_icon_label = Label( lgn_frame, image=photo, bg='#040405')
        confirm_password_icon_label.image = photo
        confirm_password_icon_label.place(x=550, y=439)

        show_image2 = ImageTk.PhotoImage \
        (file='images\\show.png')

        hide_image2 = ImageTk.PhotoImage \
            (file='images\\hide.png')

        show_button2 = Button( lgn_frame, image= show_image2, command= show2, relief=FLAT,
                                activebackground="white"
                                , borderwidth=0, background="white", cursor="hand2")
        show_button2.place(x=860, y=447)


window = Tk()
window.geometry('1166x718')
window.resizable(0, 0)
window.state('zoomed')
window.title('Login Page')

# ========================================================================
# ============================background image============================
# ========================================================================
bg_frame = Image.open('images\\background1.png')
photo = ImageTk.PhotoImage( bg_frame)
bg_panel = Label( window, image=photo)
bg_panel.image = photo
bg_panel.pack(fill='both', expand='yes')
# ====== Login Frame =========================
lgn_frame = Frame( window, bg='#040405', width=950, height=600)
lgn_frame.place(x=200, y=70)

# ========================================================================
# ========================================================
# ========================================================================
txt = "WELCOME"
heading = Label( lgn_frame, text= txt, font=('cooper black', 25, "bold"), bg="#040405",
                    fg='white',
                    bd=5,
                    relief=FLAT)
heading.place(x=80, y=30, width=300, height=30)

# ========================================================================
# ============ Left Side Image ================================================
# ========================================================================
side_image = Image.open('images\\vector.png')
photo = ImageTk.PhotoImage( side_image)
side_image_label = Label( lgn_frame, image=photo, bg='#040405')
side_image_label.image = photo
side_image_label.place(x=5, y=200)

# ========================================================================
# ============ Sign In Image =============================================
# ========================================================================
sign_in_image = Image.open('images\\hyy.png')
photo = ImageTk.PhotoImage( sign_in_image)
sign_in_image_label = Label( lgn_frame, image=photo, bg='#040405')
sign_in_image_label.image = photo
sign_in_image_label.place(x=650, y=80)

# ========================================================================
# ============ Sign In label =============================================
# ========================================================================
sign_in_label = Label( lgn_frame, text="Sign In", bg="#040405", fg="white",
                            font=("yu gothic ui", 17, "bold"))
sign_in_label.place(x=650, y=240)

# ========================================================================
# ============================username====================================
# ========================================================================
username_label = Label( lgn_frame, text="Username", bg="#040405", fg="#4f4e4d",
                            font=("yu gothic ui", 13, "bold"))
username_label.place(x=550, y=300)
login_username=StringVar()
username_entry = Entry( lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#6b6a69",
                            font=("yu gothic ui ", 12, "bold"),textvariable=login_username,insertbackground = '#6b6a69')
username_entry.place(x=580, y=335, width=270)

username_line = Canvas( lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
username_line.place(x=550, y=359)
# ===== Username icon =========
username_icon = Image.open('images\\username_icon.png')
photo = ImageTk.PhotoImage( username_icon)
username_icon_label = Label( lgn_frame, image=photo, bg='#040405')
username_icon_label.image = photo
username_icon_label.place(x=550, y=332)

# ========================================================================
# ============================login button================================
# ========================================================================
lgn_button = Image.open('images\\btn1.png')
photo = ImageTk.PhotoImage( lgn_button)
lgn_button_label = Label( lgn_frame, image=photo, bg='#040405')
lgn_button_label.image = photo
lgn_button_label.place(x=550, y=450)
login = Button( lgn_button_label, text='LOGIN', font=("yu gothic ui", 13, "bold"), width=25, bd=0,
                    bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white',command = login)
login.place(x=20, y=10)
# ========================================================================
# ============================Forgot password=============================
# ========================================================================
forgot_button = Button( lgn_frame, text="Forgot Password ?",
                            font=("yu gothic ui", 13, "bold underline"), fg="white", relief=FLAT,
                            activebackground="#040405"
                            , borderwidth=0, background="#040405", cursor="hand2",command=forgot_password_page)
forgot_button.place(x=630, y=510)
# =========== Sign Up ==================================================
sign_label = Label( lgn_frame, text='No account yet?', font=("yu gothic ui", 11, "bold"),
                        relief=FLAT, borderwidth=0, background="#040405", fg='white')
sign_label.place(x=550, y=560)

signup_img = ImageTk.PhotoImage(file='images\\register.png')
signup_button_label = Button( lgn_frame, image= signup_img, bg='#98a65d', cursor="hand2",command=registration_page,
                                borderwidth=0, background="#040405", activebackground="#040405")
signup_button_label.place(x=670, y=555, width=111, height=35)

# ========================================================================
# ============================password====================================
# ========================================================================
password_label = Label( lgn_frame, text="Password", bg="#040405", fg="#4f4e4d",
                            font=("yu gothic ui", 13, "bold"))
password_label.place(x=550, y=380)
login_password = StringVar()
password_entry = Entry( lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#6b6a69",
                            font=("yu gothic ui", 12, "bold"),textvariable= login_password,show="*", insertbackground = '#6b6a69')
password_entry.place(x=580, y=416, width=244)

password_line = Canvas( lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
password_line.place(x=550, y=440)
# ======== Password icon ================
password_icon = Image.open('images\\password_icon.png')
photo = ImageTk.PhotoImage( password_icon)
password_icon_label = Label( lgn_frame, image=photo, bg='#040405')
password_icon_label.image = photo
password_icon_label.place(x=550, y=414)
# ========= show/hide password ==================================================================
show_image = ImageTk.PhotoImage \
    (file='images\\show.png')

hide_image = ImageTk.PhotoImage \
    (file='images\\hide.png')

show_button = Button( lgn_frame, image= show_image, command= show, relief=FLAT,
                        activebackground="white"
                        , borderwidth=0, background="white", cursor="hand2")
show_button.place(x=860, y=420)
window.mainloop()