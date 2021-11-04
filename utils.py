import requests
from random import choice, shuffle
from datetime import datetime
from BotList import BotSet


class Utils:
    def __init__(self, channel):
        self.channel = channel
        self.users_list, self.users_upload_time = self.get_users()
        self.in_duel = False
        self.duel_login = ''

    def get_users(self):
        lst = requests.get(f'https://tmi.twitch.tv/group/user/{self.channel}/chatters')
        lst = lst.json()['chatters'].values()
        users_list = []
        for el in lst:
            users_list.extend(el)
        users_list = list(set(users_list) - BotSet)
        print(f'Список пользователей чата обновлён\n{users_list}')
        return users_list, datetime.now()

    @staticmethod
    def get_login(ctx):
        info = dict(item.split("=") for item in ctx.message.raw_data.split(";"))
        print(info['user-type'][info['user-type'].find('PRIVMSG')::],
              info['badges'])
        return str(info['display-name']).lower()

    def get_random_user(self, user=None):
        if (datetime.now() - self.users_upload_time).seconds > 60:
            self.users_list, self.users_upload_time = self.get_users()
        users = list(set(self.users_list) - {user})
        random_user = choice(users)
        return random_user

    def bite(self, ctx):
        biting = self.get_login(ctx)
        victim = self.get_random_user(user=biting)
        if victim == 'madvaverkabot':
            txt = f'@{biting} хотел меня укусить, но я успешно увернулась. ' \
                  f'@{biting} нельзя кусать бота!'
        else:
            phrases = [f'@{biting} кусает за жепку {victim}',
                       f'@{biting} внезапно кусает @{victim} за ухо',
                       f'@{biting} делает нежный кусь @{victim}',
                       f'@{biting} прыгает на @{victim} и кусает за шею',
                       f'@{biting} совершает мега кусь за локоть @{victim}',
                       f'@{biting} совершает множественный кусь @{victim}']
            txt = choice(phrases)
        print(f'Внимание хозяин!\n{biting} укусил {victim}')
        return txt

    def duel(self, ctx):
        login = self.get_login(ctx)
        if self.duel_login == login:
            txt = f"@{login} вызов уже брошен! Ожидайте оппонента!"
        elif self.in_duel:
            duel_users = [login, self.duel_login]
            shuffle(duel_users)
            self.in_duel = False
            self.duel_login = ''
            phrases = [
                f'@{duel_users[0]} выхватывает свой орехомёт и стреляет в @{duel_users[1]}. Есть, точное попадание! @{duel_users[1]} повержен',
                f'{duel_users[0]} безжалостно расстрелял орехами {duel_users[1]}',
                f'@{duel_users[1]} промахивается. Тем временем @{duel_users[0]} делает точный выстрел, @{duel_users[1]} повержен',
                f'@{duel_users[0]} промахивается, чем же ответит @{duel_users[1]}? Тоже промах? Что же, в этой схватке нет победителей',
                f'Оба дуэлянта, @{duel_users[0]} и @{duel_users[1]}, выстрелили одновременно и поразили друг друга. В этой схватке проиграли оба участника!']
            txt = choice(phrases)
            if 'победителей' in txt or 'проиграли' in txt:
                print(f'Внимание хозяин!\n{duel_users[0]} и {duel_users[1]} стреляются\nУ них ничья!')
            else:
                print(f'Внимание хозяин!\n{duel_users[0]} застрелил {duel_users[1]}')
        else:
            self.duel_login = login
            self.in_duel = True
            txt = f"@{login} объявил дуэль на орехомётах. Напиши !дуэль чтобы принять его вызов"
        return txt
