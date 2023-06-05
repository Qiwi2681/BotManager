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

def unpackSettings(target: str) -> str:
    txt = FileInterfaces.txt()
    settings = txt.loadFile(path='', fileName='settings.txt')
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
cliStart = f"java -jar \"osbot 2.6.69.jar\" -login {unpackSettings('credentials')} -bot "
cliParams = ":0000 -allow lowcpu,norender,norandoms -proxy "

class SubFrame(tk.Frame):
    def __init__(self, parent, frame, title, path, filename):
        super().__init__(parent)
        self.csv = FileInterfaces.csv()
        self.txt = FileInterfaces.txt()

        self.configure(background='#333333')
        self.path = path
        self.filename = filename
        self.frame = frame
        self.subFrame = tk.Frame(self.frame, bg='#555555')

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

    @staticmethod
    def verifyStr(s) -> bool:
        if s != '':
            return True
        return False

    ### SubFrame Methods ###
    def populateList(self) -> None:
        items = self.txt.loadFile(self.path, self.filename)
        for item in items:
            self.activeList.insert(tk.END, item)

    def getItems(self) -> list:
        return list(self.activeList.get(0, tk.END))

    #TODO: remove/replace entries from CSV
    def removeStr(self, i) -> None:
        self.activeList.delete(i)
        items = self.getItems()
        items.pop(i-1)
        self.txt.saveFile(items, self.path, fileName=self.filename)

        items = self.getItems()

class Accounts(SubFrame):
    def __init__(self, parent):
        super().__init__(parent, parent.frame, 'Accounts', 'data/', 'accounts.csv')

    def populateList(self) -> None:
        accounts = self.csv.df.index.tolist()
        for account in accounts:
            self.activeList.insert(tk.END, account)

    def addStr(self, s:str, proxy: str, p2p: bool, food:str) -> bool:
        try:
            email, password = s.split(':')
            self.csv.initAccount(self.csv.df, email, password, proxy, p2p, food)
            self.activeList.delete(0, tk.END)
            self.populateList()
            return True
        except ValueError:
            messagebox.showerror(
                    'ValueError', 'Make sure logins are formatted\nex. user@mail.ca:password')
            return False

    def removeStr(self, i) -> None:
        self.activeList.delete(i)
        self.csv.removeIdx(i)

#TODO: proxy checking
class Proxy(SubFrame):
    def __init__(self, parent):
        super().__init__(parent, parent.frame, 'Proxies', 'data/', 'proxies.txt')

    @staticmethod
    def verifyStr(s: str) -> bool:
        fields = s.split(':')
        l = len(fields)
        if l == 2 or l == 4:
            return True
        messagebox.showerror('ProxyError', 'Make sure proxy is formatted\nip:port or ip:port:user:pass')
        return False
    
    def addStr(self, s: str) -> None:
        if not self.verifyStr(s): return

        self.activeList.insert(tk.END, s)
        self.activeList.see(tk.END)
        items = self.getItems()
        items.append(s)
        self.txt.saveFile(items, self.path, fileName=self.filename)

class Food(SubFrame):
    def __init__(self, parent):
        super().__init__(parent, parent.frame, 'Food', 'data/', 'food.txt')
        # Add/remove 
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
        if not self.verifyStr(s):
            return

        self.activeList.insert(tk.END, s)
        self.txt.saveFile(self.getItems(), self.path, fileName=self.filename)

        # redundant QOL
        self.addEntry.delete(0, tk.END)
        self.activeList.see(tk.END)

class IdleFrame(SubFrame):
    def __init__(self, parent):
        super().__init__(parent, parent.frame, 'Idle Accounts', 'data/', 'accounts.csv')

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
        self.df = FileInterfaces.csv()
        accounts = self.df.df.index.tolist()
        for account in accounts:
            if not self.csv.getDF(account, 'running'):
                self.activeList.insert(tk.END, account)

    def startAccount(self, account, script):
        defaultPath = os.getcwd()
        os.chdir(jarPath)
        password = self.csv.getDF(account, 'pass')
        proxy = self.csv.getDF(account, 'proxy')
        world = self.getWorld(account)
        os.system(cliStart+account+':'+password+cliParams+proxy+" -world "+str(world)+" -script 845:"+str(script))
        os.chdir(defaultPath)

    def runNext(self) -> None:
        idle = self.getItems()
        for account in idle:
            script = self.csv.getDF(account, 'f2pQuesting')
            if str(script) == 'nan':
                quester = Scripts.Questing(self.csv.getDF(account, 'food'))
                script = quester.script
                self.csv.updateDF(account, 'f2pQuesting', script)
            self.startAccount(account, script)
            #self.csv.updateDF(account, 'f2pQuesting', script)

    def runLast(self) -> None:
        idle = self.getItems()
        for account in idle:
            last = self.csv.getDF(account, 'lastran')
            if not str(last) == 'nan':
                self.startAccount(account, last)
                self.csv.updateDF(account, 'running', True)
            else:
                messagebox.showerror("Start Error", f"{account} has not ran a script yet")
                break
        self.activeList.delete(0, tk.END)

    def getWorld(self, account):
        world = self.csv.getDF(account, 'world')
        if str(world) == 'nan':
            bonded = self.csv.getDF(account, 'bonded')
            worldsCSV = FileInterfaces.csv(csv='data/worlds.csv')
            if bonded:
                worlds = worldsCSV.getColumn('p2pWorlds')
            else:
                worlds = worldsCSV.getColumn('f2pWorlds')
            print(worlds)
            #TODO: make dynamic world list
            world = worlds[random.randint(0, 53)]
            self.csv.updateDF(account, 'world', int(world))
        return int(world)
