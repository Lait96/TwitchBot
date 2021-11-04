import requests
from random import choice
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
        users_list = set()
        for el in lst:
            if isinstance(el, list):
                for el_lst in el:
                    users_list.add(el_lst)
            else:
                users_list.add(el)
        users_list = users_list - BotSet
        print(users_list)
        return list(users_list), datetime.now()

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
            return f'@{biting} хотел меня укусить, но я успешно увернулась. ' \
                   f'@{biting} нельзя кусать бота!'
        phrases = [f'@{biting} кусает за жепку {victim}',
                   f'@{biting} внезапно кусает @{victim} за ухо',
                   f'@{biting} делает нежный кусь @{victim}',
                   f'@{biting} прыгает на @{victim} и кусает за шею',
                   f'@{biting} совершает мега кусь за локоть @{victim}',
                   f'@{biting} совершает множественный кусь @{victim}']
        print(f'Внимание хозяин!\n{biting} укусил {victim}')
        txt = choice(phrases)
        return txt
