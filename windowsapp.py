# please reach out to Nathan Gee if there are questions regarding this code
# this is the code to be used only windows PC's. Do not use on pi

# region for imports
import time
import tkinter as tk
from tkinter import ttk
import sqlite3
import datetime
import urllib.request
# endregion

# dbloc = "C:/Users/ngee0/OneDrive - Textron GCC-H/Equipment/InventoryManager.db" #change to the path of the database
dbloc = "C:/Users/ngee0/OneDrive - Textron GCC-H/Flight_Test_Tools/Equipment/InventoryManager.db"
# dbloc = "/home/bellinv/Documents/Inventory_Management/InventoryManager.db"

# downloads the most up to date file and saves it to the onedrive
def downl():
    url = "https://raw.githubusercontent.com/ngee99/invmanager/a4cac61f04e9b8d1bcd637b35511ca8b5fa3eefd/InventoryManager.db"
    print("download start!")
    filename = urllib.request.urlretrieve(url, filename='C:/Users/ngee0/OneDrive - Textron GCC-H/Flight_Test_Tools/Equipment/InventoryManager.db')
    print("download complete")
    print("download location: ", filename)

downl()

class App():
    root = tk.Tk()
    def __init__(self):
        super().__init__()

        # root window config
        App.root.title("Inventory Manager")
        App.root.geometry('750x750')

        bg_image = tk.PhotoImage(file="C:/Users/ngee0/OneDrive - Textron GCC-H/Documents/Equipment Management/Inventory/Code_Inventory_Management/testimage.png")
        panel1 = tk.Label(App.root, image=bg_image)
        panel1.place(x=0, y=0)
        panel1.image=bg_image # sets background image for the top portion of the program


        def errorwindow(errortext): # creates a window displaying an error message
            openerrorwindow = tk.Toplevel() # creates top level window
            openerrorwindow.title("Error Found")
            openerrorwindow.geometry("300x100")
            openerror_label=tk.Label(openerrorwindow, text=errortext)
            openerror_label.place(x=50, y=50)

        def io_openwindow(): # opens a new window for checking in/out equipment
        
            openitemwindow = tk.Toplevel()
            openitemwindow.title("Item Input Window")
            openitemwindow.geometry("400x400")       
            
            newitemname = tk.StringVar()
            newusername = tk.StringVar()

            itemname_label= tk.Label(openitemwindow, text="Scan Item:")
            itemname_label.place(x=100, y=100)
            itemname_entry = tk.Entry(openitemwindow, textvariable=newitemname)
            itemname_entry.place(x=100, y=150)

            newusername_label = tk.Label(openitemwindow, text="Scan 10 digit Textron ID:")
            newusername_label.place(x=100, y=200)
            newusername_entry = tk.Entry(openitemwindow, textvariable=newusername)
            newusername_entry.place(x=100, y=250)
            
            def swapstate():  # creates function to swap state from in/out to out/in
                conn=sqlite3.connect(dbloc)
                c=conn.cursor()
                name23 = int(newitemname.get())
                searchitem = "SELECT Eq_ID from Equipment WHERE Eq_ID=?;"
                c.execute(searchitem, (name23,)) #searches for matches to item to be added
                rows = c.fetchone()
                if rows: 
                    swap = "UPDATE Equipment SET State = CASE State WHEN 'IN' THEN 'OUT' ELSE 'IN' END WHERE Eq_ID=?;" # updates the state to out if in and in if out
                    c.execute(swap, (name23,))
                else:
                    errortext = 'Invalid barcode/item does not exist' # if the item exists, skip the operation
                    errorwindow(errortext)
                    pass
                conn.commit()
                conn.close()

            def timeupdate(): # updates the time
                conn=sqlite3.connect(dbloc)
                c=conn.cursor()
                now = int(time.time())
                name23 = int(newitemname.get())
                update = "UPDATE Equipment SET Time = ? WHERE Eq_ID = ?;"
                c.execute(update, (now, name23,))
                conn.commit()
                conn.close()

            def scanbehavior():
                swapstate()
                timeupdate()

            def clear_text():
                itemname_entry.delete(0, tk.END)
                newusername_entry.delete(0, tk.END)

            newbutton = tk.Button(openitemwindow, text="Enter Values", command=lambda: [scanbehavior(), clear_text()])
            newbutton.place(x=100, y=350)

        def add_window(): # opens a new window for adding equipment
            
            openitemwindow = tk.Toplevel()
            openitemwindow.title("Add Item")
            openitemwindow.geometry("400x800")       
            
            # creates variables
            newitemname = tk.StringVar()
            eq_name = tk.StringVar()
            newusername = tk.StringVar()
            location = tk.StringVar()
            keywords = tk.StringVar()

            # creates the boxes and questions where users can input data
            itemname_label= tk.Label(openitemwindow, text="Scan Item:")
            itemname_label.place(x=100, y=100)
            itemname_entry = tk.Entry(openitemwindow, textvariable=newitemname)
            itemname_entry.place(x=100, y=150)

            neweq_name_label = tk.Label(openitemwindow, text="Enter name for equipment")
            neweq_name_label.place(x=100, y=200)
            neweq_name_entry = tk.Entry(openitemwindow, textvariable=eq_name)
            neweq_name_entry.place(x=100, y=250)

            newusername_label = tk.Label(openitemwindow, text="Scan 10 digit Textron ID:")
            newusername_label.place(x=100, y=300)
            newusername_entry = tk.Entry(openitemwindow, textvariable=newusername)
            newusername_entry.place(x=100, y=350)

            newloca = tk.Label(openitemwindow, text="Enter Location of Equipment")
            newloca.place(x=100, y=400)
            newloca_entry = tk.Entry(openitemwindow, textvariable=location)
            newloca_entry.place(x=100, y=450)

            newkey = tk.Label(openitemwindow, text="Enter keywords for equipment seperated by commas")
            newkey.place(x=100, y=500)
            newkey_entry = tk.Entry(openitemwindow, textvariable=keywords)
            newkey_entry.place(x=100, y=550)
            
            def addnew(): # adds new entry
                conn=sqlite3.connect(dbloc)
                c=conn.cursor()
                searchitem = "SELECT Eq_ID from Equipment WHERE Eq_ID=?;"
                name23 = int(newitemname.get()) # these get the information from the boxes and questions and sets it equal to variable
                eq_name23 = str(eq_name.get())
                username23 = int(newusername.get())
                loca23 = str(location.get())
                key23 = str(keywords.get())

                now = int(time.time())
                c.execute(searchitem, (name23,)) #searches for matches to item to be added
                rows = c.fetchone()
                if rows: 
                    errortext = 'Item already exists.' # if the item exists, skip the operation
                    errorwindow(errortext)
                    pass
                else:
                    ins = "INSERT INTO Equipment (Eq_ID, Eq_Name, Username, State, Time, Location, Keywords) VALUES (?, ?, ?, 'IN', ?, ?, ?);"
                    c.execute(ins, (name23, eq_name23, username23, now, loca23, key23))
                conn.commit()
                conn.close()
            
            def clear_text():
                itemname_entry.delete(0, tk.END)
                neweq_name_entry.delete(0, tk.END)
                newusername_entry.delete(0, tk.END)
                newloca_entry.delete(0, tk.END)
                newkey_entry.delete(0, tk.END)

            newbutton = tk.Button(openitemwindow, text="Enter Values", command=lambda: [addnew(), clear_text()])
            newbutton.place(x=100, y=650)

        def remove_window(): # opens a new window for removing equipment
            
            openitemwindow = tk.Toplevel()
            openitemwindow.title("Add Item")
            openitemwindow.geometry("400x400")       
            
            newitemname = tk.StringVar()

            itemname_label= tk.Label(openitemwindow, text="Scan Item:")
            itemname_label.place(x=100, y=100)
            itemname_entry = tk.Entry(openitemwindow, textvariable=newitemname)
            itemname_entry.place(x=100, y=150)
            
            def removeitem():
                conn=sqlite3.connect(dbloc)
                c=conn.cursor()
                name23 = int(newitemname.get())
                searchitem = "SELECT Eq_ID from Eq_list WHERE Eq_ID=?"
                c.execute(searchitem, (name23,))
                rows=c.fetchone()
                if rows:
                    remove = "DELETE FROM Eq_list WHERE Eq_ID=?;"
                    c.execute(remove, (name23,))
                else:
                    errortext = 'Item does not exist.'
                    errorwindow(errortext)
                conn.commit()
                conn.close()

            def clear_text():
                itemname_entry.delete(0, tk.END)

            newbutton = tk.Button(openitemwindow, text="Enter Value", command=lambda: [removeitem(), clear_text()])
            newbutton.place(x=100, y=350)

        def user_window(): # creates new window for adding user
            openuserwindow=tk.Toplevel()
            openuserwindow.title("Add User:")
            openuserwindow.geometry("400x500")

            newtexID=tk.StringVar()
            newfirstname=tk.StringVar()
            newlastname=tk.StringVar()

             # creates the boxes and questions where users can input data
            texID_label= tk.Label(openuserwindow, text="Scan 10 digit Textron ID:")
            texID_label.place(x=100, y=100)
            texID_entry = tk.Entry(openuserwindow, textvariable=newtexID)
            texID_entry.place(x=100, y=150)

            newfirst_name_label = tk.Label(openuserwindow, text="Enter First Name:")
            newfirst_name_label.place(x=100, y=200)
            newfirst_name_entry = tk.Entry(openuserwindow, textvariable=newfirstname)
            newfirst_name_entry.place(x=100, y=250)

            newlast_name_label = tk.Label(openuserwindow, text="Enter Last Name:")
            newlast_name_label.place(x=100, y=300) 
            newlast_name_entry = tk.Entry(openuserwindow, textvariable=newlastname)
            newlast_name_entry.place(x=100, y=350)
          
            def addnewuser(): # adds new entry to Users table
                conn=sqlite3.connect(dbloc)
                c=conn.cursor()
                searchname = "SELECT user_ID from Users WHERE user_ID=?;"
                username23 = int(newtexID.get()) # these get the information from the boxes and questions and sets it equal to variable
                first_name23 = str(newfirstname.get())
                last_name23 = str(newlastname.get())
                
                now = int(time.time())
                c.execute(searchname, (username23,)) #searches for matches to item to be added
                rows = c.fetchone()
                if rows: 
                    errortext = 'User already exists.' # if the item exists, skip the operation
                    errorwindow(errortext)
                    pass
                else:
                    ins = "INSERT INTO Users (user_ID, Last_Name, First_Name) VALUES (?, ?, ?);"
                    c.execute(ins, (username23, last_name23, first_name23))
                conn.commit()
                conn.close()

            newbutton = tk.Button(openuserwindow, text="Enter Values", command=lambda: [addnewuser(), openuserwindow.destroy()])
            newbutton.place(x=100, y=400)
        
        def remove_user_window(): # opens a new window for removing equipment
            
            openitemwindow = tk.Toplevel()
            openitemwindow.title("Remove User")
            openitemwindow.geometry("400x400")       
            
            removeusername = tk.StringVar()

            removeusername_label= tk.Label(openitemwindow, text="Enter User's Last Name:")
            removeusername_label.place(x=100, y=100)
            removeusername_entry = tk.Entry(openitemwindow, textvariable=removeusername)
            removeusername_entry.place(x=100, y=150)
            
            def removeuser():
                conn=sqlite3.connect(dbloc)
                c=conn.cursor()
                name23 = removeusername.get()
                searchitem = "SELECT Last_Name from Users WHERE Last_Name=?"
                c.execute(searchitem, (name23,))
                rows=c.fetchone()
                if rows:
                    remove = "DELETE FROM Users WHERE Last_Name=?;"
                    c.execute(remove, (name23,))
                else:
                    errortext = 'User does not exist.'
                    errorwindow(errortext)
                conn.commit()
                conn.close()

            newbutton = tk.Button(openitemwindow, text="Enter Value", command=lambda: [removeuser(), openitemwindow.destroy()])
            newbutton.place(x=100, y=350)

        
        # buttons for the main page
        # check = tk.Button(App.root, text="Check In/Out Item", activebackground='black', activeforeground='white', command=io_openwindow)
        # baddnew = tk.Button(App.root, text="Add New Item", activebackground='black', activeforeground='white' , command=add_window)
        # bremoveitem = tk.Button(App.root, text="Remove Item", activebackground='black', activeforeground='white', command=remove_window)
        # bnewuser = tk.Button(App.root, text="Add New User", activebackground='black',  activeforeground='white', command=user_window)
        # bremoveuser = tk.Button(App.root, text='Remove User', activebackground='black', activeforeground='white', command=remove_user_window)

        # baddnew.place(x=75, y=125)
        # bremoveitem.place(x=200, y=125)
        # check.place(x=325, y=125)
        # bnewuser.place(x=475,y=125)
        # bremoveuser.place(x=600,y=125)

        # search boxes to search for equipment based on keyword
        def itemsearch(): #defines the item search via keywords
            searchinput=tk.StringVar()

            searchinput_label=tk.Label(App.root, text="Search for item by Keyword")
            searchinput_label.place(x=75,y=600)
            searchinput_entry = tk.Entry(App.root, textvariable=searchinput)
            searchinput_entry.place(x=75, y=625)
          
            def searchitem(): # the actual SQL work for searching for the item as well as displaying it
                conn=sqlite3.connect(dbloc)
                c=conn.cursor()
                searchitem = "SELECT Eq_ID, Eq_Name, State, Username, Time, Location FROM Equipment WHERE Keywords LIKE ? ORDER BY Eq_ID;"
                key23 = str(searchinput.get())
                c.execute(searchitem, ('%'+key23+'%',)) #searches for matches to item to be added
                rows = c.fetchall()
                if rows:
                    columns = ('Equipment ID', 'Equipment Name', 'State', 'Last User', 'Time', 'Location')
                    tree = ttk.Treeview(App.root, columns=columns, show='headings')

                    tree.heading('Equipment ID', text='Equipment ID')
                    tree.heading('Equipment Name', text='Equipment Name')
                    tree.heading('State', text='State')
                    tree.heading('Last User', text='Last User')
                    tree.heading('Time', text='Time')
                    tree.heading('Location', text='Location')
                    
                    tree.column('Equipment ID', width=100,anchor=tk.CENTER)
                    tree.column('Equipment Name',width=200,anchor=tk.CENTER)
                    tree.column('State',width=75,anchor=tk.CENTER)
                    tree.column('Last User',width=100,anchor=tk.CENTER)
                    tree.column('Time',width=150,anchor=tk.CENTER)
                    tree.column('Location',width=75,anchor=tk.CENTER)
                    
                    # changes 10 digit ID to last, first name and unix time to cst
                    for row in rows:
                        use_ID = str(row[3])
                        unixtime = row[4]
                        getusernew = "SELECT Last_Name, First_Name FROM Users WHERE user_ID=?;"
                        gettimelast = "SELECT Time FROM Equipment WHERE Time=?;"
                        c.execute(getusernew, (use_ID, ))
                        new_use_ID = c.fetchone()
                        c.execute(gettimelast, (unixtime, ))
                        newunixtime = c.fetchone()
                        new_use_ID2 = new_use_ID[1] + ', ' + new_use_ID[0]
                        newtimenow = datetime.datetime.fromtimestamp(newunixtime[0])
                        rowlist = list(row)
                        rowlist[3] = new_use_ID2
                        rowlist[4] = newtimenow
                        rowtup = tuple(rowlist)
                        tree.insert('', tk.END, values=rowtup)

                    tree.place(x=25,y=350)


                else:
                    errortext="No Item Exists Please Refine Search"
                    errorwindow(errortext)

                conn.commit()
                conn.close()

            newbutton1 = tk.Button(App.root, text="Search", command=lambda: [searchitem()])
            newbutton1.place(x=75, y=650)

        #region -- FEATURE REMOVED IN FAVOR OF EQUIPMENT LOCATION FINDER. UNCOMMENT TO REIMPLEMENT NOTE IT WILL BE BELOW OF EQUIPMENT LOCATOR -- 
        # search box to search for what user has what equipment
        # def usersearch():
            # nameinput=tk.StringVar()
# 
            # nameinput_label=tk.Label(App.root, text="Search User's Equipment by Last Name")
            # nameinput_label.place(x=475,y=600)
            # nameinput_entry = tk.Entry(App.root, textvariable=nameinput)
            # nameinput_entry.place(x=475, y=625)
          # 
            # def searchuser(): # the actual SQL work for searching for the users items as well as displaying them
            #     conn=sqlite3.connect(dbloc)
            #     c=conn.cursor()
            #     eyedee = str(nameinput.get())
            #     attachname = "SELECT user_ID FROM Users WHERE Last_Name LIKE ?;"
            #     c.execute(attachname, ('%'+eyedee+'%', ))
            #     uid_rows = c.fetchone()
            #     searchuser2 = "SELECT Eq_ID, Eq_Name, State, Time, Location FROM Equipment WHERE Username LIKE ? AND State='OUT' ORDER BY Eq_ID;"
            #     c.execute(searchuser2, (uid_rows[0],)) #searches for matches to item to be added
            #     rows = c.fetchall()
# 
            #     if rows:
            #         columns = ('Equipment ID', 'Equipment Name', 'State', 'Time', 'Location')
            #         tree = ttk.Treeview(App.root, columns=columns, show='headings')
# 
            #         tree.heading('Equipment ID', text='Equipment ID')
            #         tree.heading('Equipment Name', text='Equipment Name')
            #         tree.heading('State', text='State')
            #         tree.heading('Time', text='Time')
            #         tree.heading('Location', text='Location')
            #         
            #         tree.column('Equipment ID', width=100,anchor=tk.CENTER)
            #         tree.column('Equipment Name',width=200,anchor=tk.CENTER)
            #         tree.column('State',width=75,anchor=tk.CENTER)
            #         tree.column('Time',width=175,anchor=tk.CENTER)
            #         tree.column('Location',width=100,anchor=tk.CENTER)
            #         
            #         # changes 10 digit ID to last, first name and unix time to cst
            #         for row in rows:
            #             unixtime = row[3]
            #             gettimelast = "SELECT Time FROM Equipment WHERE Time=?;"
            #             c.execute(gettimelast, (unixtime, ))
            #             newunixtime = c.fetchone()
            #             newtimenow = datetime.datetime.fromtimestamp(newunixtime[0])
            #             rowlist = list(row)
            #             rowlist[3] = newtimenow
            #             rowtup = tuple(rowlist)
            #             tree.insert('', tk.END, values=rowtup)
# 
            #         tree.place(x=50,y=350)
# 
# 
            #     else:
            #         errortext="User Has No Equipment Checked Out"
            #         errorwindow(errortext)
# 
            #     conn.commit()
            #     conn.close()
# 
            # newbutton2 = tk.Button(App.root, text="Search", command=lambda: [searchuser()])
            # newbutton2.place(x=475, y=650)
            #endregion
        
        def seeall():
            conn=sqlite3.connect(dbloc)
            c=conn.cursor()
            searchitem = "SELECT Eq_ID, Eq_Name, State, Username, Time, Location FROM Equipment ORDER BY Eq_ID;"
            c.execute(searchitem) #searches for matches to item to be added
            rows = c.fetchall()
        
            if rows:
                columns = ('Equipment ID', 'Equipment Name', 'State', 'Last User', 'Time', 'Location')
                tree = ttk.Treeview(App.root, columns=columns, show='headings')
                tree.heading('Equipment ID', text='Equipment ID')
                tree.heading('Equipment Name', text='Equipment Name')
                tree.heading('State', text='State')
                tree.heading('Last User', text='Last User')
                tree.heading('Time', text='Time')
                tree.heading('Location', text='Location')
                
                tree.column('Equipment ID', width=100,anchor=tk.CENTER)
                tree.column('Equipment Name',width=200,anchor=tk.CENTER)
                tree.column('State',width=75,anchor=tk.CENTER)
                tree.column('Last User',width=100,anchor=tk.CENTER)
                tree.column('Time',width=150,anchor=tk.CENTER)
                tree.column('Location',width=75,anchor=tk.CENTER)
                
                # changes 10 digit ID to last, first name and unix time to cst
                for row in rows:
                    use_ID = str(row[3])
                    unixtime = row[4]
                    getusernew = "SELECT Last_Name, First_Name FROM Users WHERE user_ID=?;"
                    gettimelast = "SELECT Time FROM Equipment WHERE Time=?;"
                    c.execute(getusernew, (use_ID, ))
                    new_use_ID = c.fetchone()
                    c.execute(gettimelast, (unixtime, ))
                    newunixtime = c.fetchone()
                    new_use_ID2 = new_use_ID[1] + ', ' + new_use_ID[0]
                    newtimenow = datetime.datetime.fromtimestamp(newunixtime[0])
                    rowlist = list(row) #changes tuple to row to change the information
                    rowlist[3] = new_use_ID2
                    rowlist[4] = newtimenow
                    rowtup = tuple(rowlist) # changes back to tuple to use with tkinter
                    tree.insert('', tk.END, values=rowtup) #adds the items to a treeview

                tree.place(x=25,y=350)
                scrlbr = tk.Scrollbar(App.root, orient='vertical', command=tree.yview)
                scrlbr.place(x=5,y=350)
                tree.configure(yscrollcommand=scrlbr.set)

        bseeall = tk.Button(App.root, text="See all equipment", command=lambda: [seeall()])
        bseeall.place(x=300, y=650)

        # search box to search for what location the equipment is supposed to be at 
        def equipsearch():
            eqinput=tk.StringVar()

            eqinput_label=tk.Label(App.root, text="Search Equipment's Assigned Location")
            eqinput_label.place(x=475,y=600)
            eqinput_entry = tk.Entry(App.root, textvariable=eqinput)
            eqinput_entry.place(x=475, y=625)
          
            def searchloc(): # the actual SQL work for searching for the users items as well as displaying them
                conn=sqlite3.connect(dbloc)
                c=conn.cursor()
                eyedee = str(eqinput.get())
                attachname = "SELECT Eq_ID FROM Equipment WHERE Eq_ID=?;"
                c.execute(attachname, (eyedee, ))
                uid_rows = c.fetchone()
                searchuser2 = "SELECT Eq_ID, Eq_Name, State, Time, Location FROM Equipment WHERE Eq_ID=? ORDER BY Eq_ID;"
                c.execute(searchuser2, (uid_rows[0],)) #searches for matches to item to be added
                rows = c.fetchall()

                if rows:
                    columns = ('Equipment ID', 'Equipment Name', 'State', 'Time', 'Location')
                    tree = ttk.Treeview(App.root, columns=columns, show='headings')

                    tree.heading('Equipment ID', text='Equipment ID')
                    tree.heading('Equipment Name', text='Equipment Name')
                    tree.heading('State', text='State')
                    tree.heading('Time', text='Time')
                    tree.heading('Location', text='Location')
                    
                    tree.column('Equipment ID', width=100,anchor=tk.CENTER)
                    tree.column('Equipment Name',width=200,anchor=tk.CENTER)
                    tree.column('State',width=75,anchor=tk.CENTER)
                    tree.column('Time',width=175,anchor=tk.CENTER)
                    tree.column('Location',width=100,anchor=tk.CENTER)
                    
                    # changes 10 digit ID to last, first name and unix time to cst
                    for row in rows:
                        unixtime = row[3]
                        gettimelast = "SELECT Time FROM Equipment WHERE Time=?;"
                        c.execute(gettimelast, (unixtime, ))
                        newunixtime = c.fetchone()
                        newtimenow = datetime.datetime.fromtimestamp(newunixtime[0])
                        rowlist = list(row)
                        rowlist[3] = newtimenow
                        rowtup = tuple(rowlist)
                        tree.insert('', tk.END, values=rowtup)

                    tree.place(x=50,y=350)


                else:
                    errortext="User Has No Equipment Checked Out"
                    errorwindow(errortext)

                conn.commit()
                conn.close()

            newbutton2 = tk.Button(App.root, text="Search", command=lambda: [searchloc()])
            newbutton2.place(x=475, y=650)

        itemsearch()
        equipsearch()

    # def on_closing():
    #     delete_file()
    #     upload_file()
    #     app.root.destroy()

        

if __name__ == "__main__":
    app = App()
    # app.root.protocol("WM_DELETE_WINDOW", App.on_closing)
    app.root.mainloop()



# region for roadmap
# FIXME roadmap
# DONE Add user adding/removal
# DONE make it convert from unix time to CST
# DONE Convert username to first/last name
# DONE add a way to search items
# DONE add a way to search based on keywords
# DONE swap order of first/last name in new user adder
# FIXME make it resize with window size
# DONE make a way to find location by scanning item
# DONE when any action done upload to github
# endregion