# -*- coding: utf-8 -*-
"""
See application comment
"""

from tkinter import *
from tkinter.ttk import *
from datetime import date

class Application(Frame):
    """A GUI app that provides interaction with a text file.
    The user queries the text file to know whos birthday it is today
    They can provide a date and will receive all people who have their birthdays on that day.
    The user can manually add birthdays to the text file, but not remove them.
    Birthday data in the text file is in the following format: mmddFNAME LNAME (example: 1603John Doe)
    """


    def __init__(self, master):
        """Initialize the frame"""
        Frame.__init__(self,master)
        self.grid()
        self.createWidgets()
        self.todaysBirthdays()

    def createWidgets(self):
        """BEGIN Creating the Add Birthday widgets"""
        #creates label instructing entry format for adding date
        self.labelAddDate = Label(self)
        self.labelAddDate["text"] = "Enter the birthday date (format: ddmm, example: 20 june -> 2006)"
        self.labelAddDate.grid(row = 0 , column = 0, sticky = W)
        #user text entry with the 4 digit bday
        self.entryAddDate = Entry(self)
        self.entryAddDate.grid(row = 0, column = 2, sticky = W)
        #creates label instructing entry format for adding name
        self.labelAddName = Label(self)
        self.labelAddName["text"] = "Enter the persons name (format: FName LName, example: John Doe)"
        self.labelAddName.grid(row = 1 , column = 0, sticky = W)
        #user text entry with the full name
        self.entryAddName = Entry(self)
        self.entryAddName.grid(row = 1, column = 2, sticky = W)
        #button that collects entries and creates the bday in the text file(with method)
        self.buttonAdd = Button(self)
        self.buttonAdd["text"] = "Add birthday"
        self.buttonAdd["command"] = self.addBday
        self.buttonAdd.grid(row = 2, column = 2, sticky = W)
        """END Creating the Add Birthday widgets"""

        """BEGIN Creating the whos Birthday on date widgets"""
        #creates label instructing format for birthday query
        self.labelAskDate = Label(self)
        self.labelAskDate["text"] = "Enter the date you wish to check (format: ddmm, example: 20 june -> 2006):"
        self.labelAskDate.grid(row = 3 , column = 0, sticky = W)
        #user text entry with the 4 digit birthday
        self.entryAskDate = Entry(self)
        self.entryAskDate.grid(row = 3, column = 2, sticky = W)
        #button that collects entry and checks the text file for the bdays.
        self.buttonAsk = Button(self)
        self.buttonAsk["text"] = "Check birthdays on given date."
        self.buttonAsk["command"] = self.askBday
        self.buttonAsk.grid(row = 4, column = 2, sticky = W)
        """END Creating the whos Birthday on date widgets"""

        self.buttonToday = Button(self)
        self.buttonToday["text"] = "Todays birthdays"
        self.buttonToday["command"] = self.todaysBirthdays
        self.buttonToday.grid(row = 9, column = 2, sticky = W)


        """BEGIN Widget for displaying names of birthday boys/girls"""
        self.results = Text(self, wrap = WORD)
        self.results.grid(row = 8, columnspan = 3)
        """END Widget for displaying names of birthday boys/girls"""

    def addBday(self):
        """"add entered data into the text file and clears the fields afterwards"""
        #retreive user input
        dateToAdd = self.entryAddDate.get()
        nameToAdd = self.entryAddName.get()
        #print(str(dateToAdd)+nameToAdd,"\n\n")
        if dateToAdd != "" and nameToAdd !="": #avoids empty lines being created in text file.
            tfw = open("birthday_file.txt","a")
            tfw.write(str("\n"+dateToAdd)+nameToAdd)
            tfw.close()
            self.entryAddDate.delete(0, END)#emptues the fields after the button is clicked.
            self.entryAddName.delete(0, END)

    def createDict(self):
        bdayDictionary = {}
        try:
            tfr = open("birthday_file.txt", "r")
            bdList = tfr.readlines()
            for entry in bdList:
                date = entry[0:4]
                name = entry[4:]
                if date in bdayDictionary:
                    bdayDictionary[date] += name
                else:
                    bdayDictionary.update({date: name})
                    tfr.close()
            return bdayDictionary
        except:
            print("There is no birthday file yet.")


    def askBday(self):
        """"checks the text file to see whos birthday it is on the entered date"""
        dateToAsk = self.entryAskDate.get()
        bdayDictionary = self.createDict()
        #print(bdayDictionary)
        if dateToAsk in bdayDictionary:
            #print(bdayDictionary[dateToAsk])
            message = "The birthday celebrants on "
            message += dateToAsk
            message += " are:\n\n"
            message += bdayDictionary[dateToAsk]
            self.results.delete(0.0,END)
            self.results.insert(0.0,message)

    def todaysBirthdays(self):
        bdayDictionary = self.createDict()
        todaysDate = date.today()
        formattedDate = date.strftime(todaysDate,"%d%m")
        if bdayDictionary != None:
            if formattedDate in bdayDictionary:
                message = "Today's birthday celebrants are:\n\n"
                message += bdayDictionary[formattedDate]
                self.results.delete(0.0,END)
                self.results.insert(0.0,message)


root = Tk()
root.title("bDaYs")
#oot.geometry("800x500")
root.resizable(width=False, height=False)
app = Application(root)
root.mainloop()
