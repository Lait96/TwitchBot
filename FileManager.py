import pickle


def GetTop():
    with open('duel_top.pickle', 'rb') as f:
        return pickle.load(f)


def WriteTop(dct):
    with open('duel_top.pickle', 'wb') as f:
        pickle.dump(dct, f)


def GetBotSet():
    with open('BotSet.pickle', 'rb') as f:
        return pickle.load(f)


def WriteBotSet(st):
    with open('BotSet.pickle', 'wb') as f:
        pickle.dump(st, f)
