import pandas as pd
import random
import string
from typing import Any

# TODO: optimize loadDF to only have the current accounts in memory, not the whole df
#TODO: normalize the csv, and txt initializations to match the new name format
class csv():
    def __init__(self, csv='data/accounts.csv') -> None:
        self.df = self.loadDF(name=csv)

    #TODO: normalize the loadDF calls, remove the default value
    def loadDF(self, name='data/accounts.csv') -> pd.DataFrame:
        data = pd.read_csv(name)
        # we should remove the columns we dont need
        if name == 'data/accounts.csv':
            return data.copy().set_index('email')# index the file in memory
        return data

    def saveDF(self, name='data/accounts.csv') -> None:
        self.df.to_csv(name)

    def updateDF(self, username: str, variable: str, value) -> None:
        if value is None:
            raise ValueError
        self.df.at[username, variable] = value
        self.saveDF()

    def removeIdx(self, i) -> None:
        self.df = self.df.drop(self.df.index[i])
        self.saveDF()

    def getDF(self, username: str, variable: str) -> Any:
        return self.df.loc[username, variable]
    
    def getColumn(self, column: string) -> list[Any]:
        return self.df[column].tolist()

    def isNone(self, element: str) -> bool:
        return pd.isna(element)

    def initAccount(self, df, username: str, password: str, proxy: str, bonded: bool, food: str) -> None:
        #this line is using the child class instead of self???
        if username in df.index:
            return None
        df.at[username, 'pass'] = password
        df.at[username, 'proxy'] = proxy
        df.at[username, 'running'] = False
        df.at[username, 'bonded'] = bonded
        df.at[username, 'food'] = food
        self.df = df
        self.saveDF()


class txt():
    @staticmethod
    def randomName() -> str:
        return ''.join(random.choice(string.ascii_lowercase) for i in range(8))

    def saveFile(self, data: list[str], path: str, txt=False, fileName=None):
        if fileName is None:
            fileName = self.randomName()
        name = path+fileName
        if txt:
            name += '.txt'
        with open(name, 'w') as file:
            for line in data:
                file.write(line+'\n')
        return fileName

    def loadFile(self, path: str, fileName: str) -> list[str]:
        try:
            with open(path+fileName, 'r') as file:
                lst = []
                for line in file.readlines():
                    lst.append(line.rstrip('\n'))
                return lst
        except FileNotFoundError:
            print(f'file not found: {path+fileName}')
            return []
