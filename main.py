import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random

import ConfigWindow



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

        self.subFrame = ConfigWindow.IdleFrame(self)
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
        self.accountFrame = ConfigWindow.AccountFrame(self)
        self.proxyFrame = ConfigWindow.ProxyFrame(self)
        self.foodFrame = ConfigWindow.FoodFrame(self)

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

    #TODO:this
    def removeEntry(self) -> None:
        if self.accountFrame.removeStr():
            return
        elif self.proxyFrame.removeStr():
            return
        elif self.foodFrame.removeStr():
            return

    def clipboard(self) -> None:
        data = self.clipboard_get().splitlines()
        for item in data:
            if '@' in item:
                self.accountFrame += item
            else:
                self.proxyFrame += item

if __name__ == '__main__':
    instance = MainWindow()
    instance.run()