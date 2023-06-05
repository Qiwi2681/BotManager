import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random

import Config



class MainWindow(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.geometry("563x587+614+76")
        self.title("Bot Manager By Qiwi")

        #self.debug = tk.Button(self, text="Debug", command=self.debug)
        #self.debug.pack()

        # Intermediate frame for DeployFrame and ConfigFrame
        self.mainFrame = tk.Frame(self, bg='#333333')
        self.mainFrame.pack()

        # DeployFrame
        self.accounts = DeployFrame(self.mainFrame)
        self.accounts.grid(row=0, column=0, padx=10, pady=10)

        # ConfigFrame
        self.config = ConfigFrame(self.mainFrame)
        self.config.grid(row=1, column=0, padx=10, pady=10)

    def run(self) -> None:
        self.mainloop()

    # def debug(self) -> None:
        #print(self.winfo_geometry())

class DeployFrame(tk.Frame):
    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.frame = tk.Frame(self, bg='#555555')
        self.frame.pack()

        self.subFrame = Config.IdleFrame(self)
        self.subFrame.pack(fill='both')

class ConfigFrame(tk.Frame):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.am_i = 'disabled'

        #config frame
        self.frame = tk.Frame(self, bg='#555555')
        self.frame.pack(anchor='center', side='top')

        # config title
        self.configTitle = tk.Frame(self.frame, bg='#555555')
        self.titleLabel = tk.Label(self.configTitle, text='Configuration', fg='#F8F8F8', bg='#555555')
        self.titleLabel.pack(pady=10)
        self.configTitle.pack()

        # config buttons
        self.buttonFrame = tk.Frame(self.frame, bg='#555555')
        self.addConfig = tk.Button(self.buttonFrame, text='Import from Clipboard', command=self.clipboard)
        self.remove = tk.Button(self.buttonFrame, text='Remove', command=self.removeEntry)
        self.addConfig.pack(side='left', padx=10, pady=10)
        self.remove.pack(side='left', padx=10, pady=10)
        self.buttonFrame.pack(anchor='w', side='bottom')

        # config sub frames
        self.accountFrame = Config.Accounts(self)
        self.proxyFrame = Config.Proxy(self)
        self.foodFrame = Config.Food(self)

        # account frame
        self.isBonded = tk.BooleanVar()
        self.configButtonsFrame = tk.Frame(self.accountFrame.subFrame, bg='#555555')
        self.bondedBox = tk.Checkbutton(self.configButtonsFrame, text='Members?', variable=self.isBonded)
        self.bondedBox.pack(pady=5)
        self.configButtonsFrame.pack(anchor='w', padx=40)

        # proxy frame
        self.modeCombobox = ttk.Combobox(self.proxyFrame.subFrame, textvariable='Proxy Mode', values=['Proxy Mode', 'One to One', 'Randomize'], state='readonly', width=15)
        self.modeCombobox.current(0)
        self.modeCombobox.pack(anchor='w', padx=26, pady=7)

    def removeEntry(self) -> None:
        a_index = self.accountFrame.activeList.curselection()[0] if self.accountFrame.activeList.curselection() else None
        p_index = self.proxyFrame.activeList.curselection()[0] if self.proxyFrame.activeList.curselection() else None
        f_index = self.foodFrame.activeList.curselection()[0] if self.foodFrame.activeList.curselection() else None
        if a_index is not None:
            self.accountFrame.removeStr(a_index)
        elif p_index is not None:
            self.proxyFrame.removeStr(p_index)
        elif f_index is not None:
            self.foodFrame.removeStr(f_index)

    def clipboard(self) -> None:
        data = self.clipboard_get().splitlines()
        for item in data:
            if '@' in item:
                mode = self.modeCombobox.get()
                proxies = self.proxyFrame.getItems()
                foods = self.foodFrame.getItems()
                init = self.initAccounts(item, mode, proxies, foods)
                if not init:
                    break
            else:
                self.proxyFrame.addStr(item)

    def getProxy(self, mode, proxies, used) -> str:
        if mode == 'One to One':
            for proxy in proxies:
                if proxy not in used:
                    used.append(proxy)
                    return proxy
                elif proxy == proxies[-1]:
                    messagebox.showerror('Proxy Error', 'All available proxies are used')
                    return ''
        elif mode == 'Randomize':
            return proxies[random.randint(0, len(proxies)-1)]
        messagebox.showerror('Proxy Error', 'Select a proxy mode')
        return ''
    
    def initAccounts(self, account: str, mode: str, proxies: list, foods: list) -> bool:
        usedProxies = self.loadFile('data/', 'proxies.txt')
        food = foods[random.randint(0, len(foods)-1)]
        validProxy = self.getProxy(mode, proxies, usedProxies)
        if validProxy == '':
            messagebox.showerror('Proxy Error', 'All available proxies are used')
            return False
        return self.accountFrame.addStr(account, validProxy, self.isBonded.get(), food)



instance = MainWindow()
instance.run()