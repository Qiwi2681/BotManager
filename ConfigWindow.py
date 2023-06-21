import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random

import FileInterfaces
import Scripts

foodDict = {
    'Tuna': '361',
    'Salmon': '329',
    'Pike': '351'
}

#TODO: Integrate this into a class somewhere
def unpackSettings(target: str) -> str:
    with open('settings.txt', 'r') as f:
        settings = f.readlines()
        if target == 'path':
            parsed = ''
            path = settings[0].split(':')[1:]
            parsed += path[0][1:] + path[1]
            return parsed
        elif target == 'credentials':
            parsed = ''
            login = settings[1].split(':')[1:]
            parsed += login[0][1:] + ':' + login[1]
            return parsed


#TODO: stop being lazy and do this better
jarPath = f'{unpackSettings("path")}'
cliStart = f"java -jar \"osbot 2.6.67.jar\" -login {unpackSettings('credentials')} -bot "
cliParams = ":0000 -allow lowcpu,norender,norandoms -proxy "

class SubFrame(tk.Frame):
    def __init__(self, parent, title, filename):
        super().__init__(parent)
        self.csv = FileInterfaces.CSV(csv=filename)

        self.configure(background='#333333')
        self.filename = filename
        self.subFrame = tk.Frame(parent.frame, bg='#555555')

        # Title
        self.titleFrame = tk.Frame(self.subFrame, bg='#555555')
        self.titleLabel = tk.Label(self.titleFrame, text=title, fg='#F8F8F8', bg='#555555')
        self.titleLabel.pack(side='top', pady=5)

        # Listbox
        self.activeFrame = tk.Frame(self.subFrame, bg='#555555')
        self.activeList = tk.Listbox(self.activeFrame, bg='#555555', fg='#F8F8F8')
        self.activeScrollbar = tk.Scrollbar(self.activeFrame)
        self.activeList.pack(side='left', pady=8)
        self.activeScrollbar.pack(side='left', fill=tk.Y, pady=8)
        self.activeScrollbar.config(command=self.activeList.yview)
        self.activeList.config(yscrollcommand=self.activeScrollbar.set)

        # Pack frames
        self.titleFrame.pack()
        self.activeFrame.pack(padx=20)
        self.subFrame.pack(anchor='n', side='left')

        # Get stored values
        try:
            self.populateList()
        except TypeError:
            pass

    def __iadd__(self, s: str) -> None:
        if not self.verifyStr(s): return
        self.csv[self.column] = s
        self.populateList()

    @staticmethod
    def verifyStr(s) -> bool:
        if s != '':
            return True
        return False

    def populateList(self) -> None:
        self.activeList.delete(0, tk.END)
        for listItem in self.csv:
            itemStr = str(self.csv[listItem][0])
            if itemStr == 'nan': continue
            self.activeList.insert(tk.END, itemStr)

    ### SubFrame Methods ###
    ######THIS IS AN ISSUE########


    def getItems(self) -> list:
        return list(self.activeList.get(0, tk.END))

    def addStr(self, s: str) -> None:
        if not self.verifyStr(s): return
        self.csv[self.column] = s
        self.populateList()

    def removeStr(self) -> bool:
        i = self.activeList.curselection()
        if not i:
            return False
        self.csv.removeIdx(i[0])
        self.populateList()
        return True

class AccountFrame(SubFrame):
    def __init__(self, parent):
        super().__init__(parent, 'Accounts', 'accounts.csv')

    def __iadd__(self, account):
        try:
            self.csv.addAccount(account)
            self.populateList()
            return True
        except ValueError:
            messagebox.showerror(
                    'ValueError', 'Make sure logins are formatted\nex. user@mail.ca:password')
            return False

    def __getitem__(self, key: str):
        return self.csv.getDF(self, key)

    def populateList(self) -> None:
        self.activeList.delete(0, tk.END)
        for account in self.csv:
            self.activeList.insert(tk.END, account)

    def removeStr(self) -> bool:
        i = self.activeList.curselection()
        if not i:
            return False
        self.csv.removeIdx(self.csv[i[0]])
        self.populateList()
        return True

#TODO: proxy checking
class ProxyFrame(SubFrame):
    def __init__(self, parent):
        self.column = 'proxies'
        super().__init__(parent, 'Proxies', 'proxies.csv')

    @staticmethod
    def verifyStr(s: str) -> bool:
        fields = s.split(':')
        l = len(fields)
        if l == 2 or l == 4:
            return True
        messagebox.showerror('ProxyError', 'Make sure proxy is formatted\nip:port or ip:port:user:pass')
        return False

class FoodFrame(SubFrame):
    def __init__(self, parent):
        self.column = 'food'
        super().__init__(parent, 'Food', 'food.csv')

        self.entryFrame = tk.Frame(self.subFrame, bg='#555555', bd=3, pady=3)
        self.addEntry = ttk.Entry(self.entryFrame, width=15)
        self.addEntry.pack(side='left', padx=3)
        self.add = ttk.Button(self.entryFrame, text='Add', command=self.addStr, width=4)
        self.add.pack(side='left')
        self.entryFrame.pack()

    @staticmethod
    def verifyStr(s:str) -> bool:
        try:
            foodDict[s]
        except KeyError:
            messagebox.showerror('Food Error', 'Food ID can\'t be found')
            return False
        return True
    
    def addStr(self) -> None:
        s = self.addEntry.get().strip()
        if not self.verifyStr(s): return

        self.csv[self.column] = s
        self.populateList()

class IdleFrame(SubFrame):
    def __init__(self, parent):
        super().__init__(parent, 'Idle Accounts', 'accounts.csv')

        #TODO:  make this work
        #self.modeCombobox = ttk.Combobox(self.activeFrame, textvariable='Script Mode', values=['Script Preset', '13qp'], state='readonly', width=15)
        #self.modeCombobox.current(0)
        #self.modeCombobox.pack(anchor='nw', padx=10, pady=5)

        self.lastRan = tk.Button(self.activeFrame, text='Start Quests', command=self.runNext)
        self.lastRan.pack(anchor='nw', padx=10, pady=5)

        self.refresh = tk.Button(self.activeFrame, text='Refresh List', command=self.populateList)
        self.refresh.pack(anchor='nw', padx=10, pady=5)

        #self.lastRan = tk.Button(self.activeFrame, text='Restart last script', command=self.runLast)
        #self.lastRan.pack(anchor='nw', padx=10, pady=5)

    def populateList(self) -> None:
        self.activeList.delete(0, tk.END)
        for account in self.csv:
            if self.csv[account]['running']:
                continue
            self.activeList.insert(tk.END, account)

    def startAccount(self, account, script):
        defaultPath = os.getcwd()
        os.chdir(jarPath)
        password = self.csv[account]['pass']
        proxy = self.csv[account]['proxy']
        world = self.getWorld(account)
        os.system(cliStart+account+':'+password+cliParams+proxy+" -world "+str(world)+" -script 845:"+str(script))
        os.chdir(defaultPath)

    def runNext(self) -> None:
        idle = self.getItems()
        for account in idle:
            script = self.csv[account]['f2pQuesting']
            if str(script) == 'nan':
                food = self.csv[account]['food']
                quester = Scripts.Questing(food)
                script = quester.script
                self.csv[account]['f2pQuesting'] = script
            self.startAccount(account, script)

    def runLast(self) -> None:
        idle = self.getItems()
        for account in idle:
            last = self.csv[account]['lastran']
            if not str(last) == 'nan':
                self.startAccount(account, last)
                self.csv[account]['running'] = True
            else:
                messagebox.showerror("Start Error", f"{account} has not ran a script yet")
                break
        self.activeList.delete(0, tk.END)

    def getWorld(self, account):
        world = self.csv[account]['world']
        if str(world) == 'nan':
            bonded = self.csv[account]['bonded']
            worldsCSV = FileInterfaces.csv(csv='data/worlds.csv')
            if bonded:
                worlds = worldsCSV['p2pWorlds']
            else:
                worlds = worldsCSV['f2pWorlds']
            print(worlds)
            #TODO: make dynamic world list
            world = worlds[random.randint(0, 53)]
            self.csv[account]['world'] = int(world)
        return int(world)