import pandas as pd
from typing import Any

class CSV:
    def __init__(self, csv: str):
        self.name = 'data/' + csv
        self.df = self.loadDF()

    def __repr__(self) -> dict:
        return self.name

    def __iter__(self) -> map:
        return iter(self.df.index)

    def __len__(self) -> int:
        return self.df.shape[0]

    def __getitem__(self, *indices: str) -> Any:
        try:
            return self.df.loc[indices[0]][indices[1]]
        except IndexError:
            return self.df.loc[indices]
        except KeyError:
            print(indices)
            if isinstance(indices[0], int):
                return self.df.iloc[indices[0]]
            self.addAccount(indices[0])

    def __setitem__(self, key: str, value: Any):
        end = len(self)
        self.df.at[end, key] = value
        self.df.to_csv(self.name, index=False)

    def loadDF(self) -> pd.DataFrame:
        if self.name == 'data/accounts.csv':
            return pd.read_csv(self.name, index_col='email')
        return pd.read_csv(self.name)

    def saveDF(self):
        self.df.to_csv(self.name)

    def removeIdx(self, idx: Any):
        self.df = self.df.drop(idx)
        if not isinstance(idx, int):
            self.saveDF()
            return
        self.df = self.df.reset_index(drop=True)
        self.df.to_csv(self.name, index=False)

    def getRow(self, index: str) -> list[Any]:
        rowData = []
        for column in self.df.columns:
            rowData.append(self[index, column])
        return rowData

    def addAccount(self, login: str):
        email, password = login.split(':')
        self.df.at[email, 'pass'] = password
        self.df.at[email, 'running'] = False
        self.saveDF()
        self.df = self.loadDF()



    # REDUNDANT, requires implementation
    def initAccount(self, email: str, password: str, proxy: str, bonded: bool, food: str):
        if email in self.df.index:
            return None
        self.df.at[email, 'proxy'] = proxy
        
        self.df.at[email, 'bonded'] = bonded
        self.df.at[email, 'food'] = food
        self.saveDF()



if __name__ == '__main__':
    newAccounts = ['gfg@gma.com:gad', 'gf1g312@gma.com:gad', 'gf554@gma.com:gad']
    csv = CSV('proxies.csv')

    #a = csv['proxies']
    for proxy in csv:
        print(csv[proxy][0])

    #for account in csv:
        #print(csv[account]['bonded'])

    #addAccouint
    #addAccouint = csv['a:111']
    
    #getData
    #a = csv['a']['pass']
    #print(a)

