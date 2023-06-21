import FileInterfaces
import random

import ConfigWindow

class Script():
    def __init__(self):
        self.csv = FileInterfaces.csv('data/scripts.csv')
        self.txt = FileInterfaces.txt()
        #TODO: add settings.txt for paths
        self.OSBpath = ConfigWindow.jarPath

    @staticmethod
    def dataParser(line: str, delimiter: list[str], food: str) -> str:
        for i, char in enumerate(line):
            for delim in delimiter:
                if char == delim:
                    value = ''.join(line[i+1:])
                    line = line[:i]
                    break
        # if we have a range of numbers, get a random one
        try:
            lower, upper = value.split('-')
            value = random.randrange(int(lower), int(upper)+1)
            return line+str(value)
        # if we have a food value, get food
        except ValueError:
            return line+food
        # normal line
        except UnboundLocalError:
            return line

#this might do better as a function instead of a class
class Questing(Script):
    def __init__(self, food):
        super().__init__()
        self.path = 'StealthQuester/QuestPresets/'
        self.cli = " -script 845:"
        self.food = food
        #if mode == 'f2p':
        self.data = self.getData()
        self.quests = self.csv['f2pQuests']
        self.rewards = self.parseRewards(self.csv['rewards'])
        self.script = self.createProfile()

    @staticmethod
    def parseRewards(rewards: list[str]):
        dict = {}
        for reward in rewards:
            if not isinstance(reward, float):
                key, value = reward.split('@')
                if '%' in value:
                    value = value.replace('%','\n')
                dict[key] = value
        return dict

    def getData(self):
        parsedData = []
        lines = self.csv['questDataF2p']
        for line in lines:
            parsedData.append(self.dataParser(line, ['@', '$'], self.food))
        return '\n'.join(parsedData)
    
    def createProfile(self):
        questFile = []
        randomOrder = [self.quests[x] for x in random.sample(range(0,len(self.quests)),len(self.quests))]
        for quest in randomOrder:
            if isinstance(quest,float):
                continue
            try:
                reward = self.rewards[quest]
                questFile.append(quest + '\n' + self.data + '\n' + reward)
            except KeyError:
                questFile.append(quest + '\n' + self.data)
        return self.txt.saveFile(questFile, self.OSBpath+self.path)

if __name__ == '__main__':
    quest = Questing('Tuna')
    print(quest.createProfile())