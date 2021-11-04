import requests
import config
from random import shuffle, choice


def get_random_users(channel, login):
    users = requests.get(f'https://tmi.twitch.tv/group/user/{channel}/chatters')
    print(users)
    users = users.json()

    def flatten(x):
        result = []
        for el in x:
            if hasattr(el, "__iter__") and not isinstance(el, str):
                result.extend(flatten(el))
            else:
                result.append(el)
        return result

    lis = []
    lis.extend(users['chatters'].values())
    users_list = list(flatten(lis))
    shuffle(users_list)
    while True:
        if users_list[0] == login:
            shuffle(users_list)
        else:
            break
    return users_list[0]


def get_login(ctx):
    info = dict(item.split("=") for item in ctx.message.raw_data.split(";"))
    print(info)
    return str(info['display-name']).lower()


def random_bite(ctx):
    login = get_login(ctx)
    while True:
        random_login = get_random_users(config.CHAN[0], login)
        if random_login != login:
            break
    speak = [f'@{login} кусает за жепку {random_login}',
             f'@{login} внезапно кусает @{random_login} за ухо',
             f'@{login} делает нежный кусь @{random_login}',
             f'@{login} прыгает на @{random_login} и кусает за шею',
             f'@{login} совершает мега кусь за локоть @{random_login}',
             f'@{login} совершает множественный кусь @{random_login}']
    log = f'Внимание хозяин!\n{login} укусил {random_login}'
    txt = choice(speak)
    return txt, log


def get_random_duel(lst):
    shuffle(lst)
    win, lus = lst
    speak = [f'@{win} выхватывает свой орехомёт и стреляет в @{lus}. Есть, точное попадание! @{lus} повержен',
             f'{win} безжалостно расстрелял орехами {lus}',
             f'@{lus} промахивается. Тем временем @{win} делает точный выстрел, @{lus} повержен',
             f'@{win} промахивается, чем же ответит @{lus}? Тоже промах? Что же, в этой схватке нет победителей',
             f'Оба дуэлянта,@{win} и @{lus}, выстрелили одновременно и поразили друг друга. В этой схватке проиграли оба участника!']
    txt = choice(speak)
    if 'победителей' in txt or 'проиграли' in txt:
        log = f'Внимание хозяин!\n{win} и {lus} стреляются\nУ них ничья!'
    else:
        log = f'Внимание хозяин!\n{win} застрелил {lus}'
    return txt, log
