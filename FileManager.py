import pickle


def GetTop():
    with open('duel_top.pickle', 'rb') as f:
        return pickle.load(f)


def WriteTop(dct):
    with open('duel_top.pickle', 'wb') as f:
        pickle.dump(dct, f)

