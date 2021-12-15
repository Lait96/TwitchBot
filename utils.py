import FileManager
from random import choice, shuffle, randint


class Utils:
    def __init__(self, channel):
        self.channel = channel
        self.in_duel = False
        self.duel_login = ''
        self.users_list = [channel]
        self.duel_top = FileManager.GetTop()

    @staticmethod
    def get_login(ctx, mess=False):
        nick = ctx.author.name
        if mess:
            message = ctx.message.content
            return nick, message
        return nick

    def get_random_user(self, user=None):
        users = list(set(self.users_list) - {user})
        random_user = choice(users)
        return random_user

    def bite(self, ctx):
        biting = self.get_login(ctx)
        victim = self.get_random_user(user=biting)

        phrases = [f'@{biting} кусает за жепку {victim}',
                   f'@{biting} внезапно кусает @{victim} за ухо',
                   f'@{biting} делает нежный кусь @{victim}',
                   f'@{biting} прыгает на @{victim} и кусает за шею',
                   f'@{biting} совершает мега кусь за локоть @{victim}',
                   f'@{biting} совершает множественный кусь @{victim}']
        txt = choice(phrases)

        print(f'Внимание хозяин!\n{biting} укусил {victim}')
        return txt

    def duel(self, login):
        if self.duel_login == login:
            txt = f"@{login} вызов уже брошен! Ожидайте оппонента!"
        elif self.in_duel:
            duel_users = [login, self.duel_login]
            shuffle(duel_users)
            self.in_duel = False
            self.duel_login = ''
            phrases_win = [
                f'@{duel_users[0]} выхватывает свой орехомёт и стреляет в @{duel_users[1]}. Есть, точное попадание! @{duel_users[1]} повержен',
                f'{duel_users[0]} безжалостно расстрелял орехами {duel_users[1]}',
                f'@{duel_users[1]} промахивается. Тем временем @{duel_users[0]} делает точный выстрел, @{duel_users[1]} повержен']
            phrases_draw = [
                f'@{duel_users[0]} промахивается, чем же ответит @{duel_users[1]}? Тоже промах? Что же, в этой схватке нет победителей',
                f'Оба дуэлянта, @{duel_users[0]} и @{duel_users[1]}, выстрелили одновременно и поразили друг друга. В этой схватке проиграли оба участника!']
            txt = choice(phrases_win if randint(0, 10) != 1 else phrases_draw)
            if 'победителей' in txt or 'проиграли' in txt:
                print(f'Внимание хозяин!\n{duel_users[0]} и {duel_users[1]} стреляются\nУ них ничья!')
                self.update_duel_top(duel_users, [1, 1, 0, 0])
            else:
                print(f'Внимание хозяин!\n{duel_users[0]} застрелил {duel_users[1]}')
                self.update_duel_top(duel_users, [1, 1, 1, 0])
        else:
            self.duel_login = login
            self.in_duel = True
            txt = f"@{login} объявил дуэль на орехомётах. Напиши !дуэль чтобы принять его вызов"
        return txt

    def update_duel_top(self, logins, score):
        if logins[0] not in self.duel_top:
            self.duel_top[logins[0]] = {'Дуэлей': 0, 'Побед': 0}
        if logins[1] not in self.duel_top:
            self.duel_top[logins[1]] = {'Дуэлей': 0, 'Побед': 0}
        for i in range(4):
            self.duel_top[logins[i % 2]]['Дуэлей' if i <= 1 else 'Побед'] += score[i]
        FileManager.WriteTop(self.duel_top)
        print('Топ дуэли обновлён')

    def duel_top3(self):
        top3 = sorted(self.duel_top, key=lambda x: (self.duel_top[x]['Побед'],
                                                    self.duel_top[x]['Дуэлей']),
                      reverse=True)[0:3]
        result = ''
        for i in top3:
            txt = f'@{i} - Дуэлей: {self.duel_top[i]["Дуэлей"]}, Побед - {self.duel_top[i]["Побед"]}\n'
            result += txt
        return result

    def duel_statistic(self, login):
        if login in self.duel_top:
            return f'@{login} - Дуэлей: {self.duel_top[login]["Дуэлей"]}, Побед: {self.duel_top[login]["Побед"]}'
        else:
            return f'@{login} Не участвовал в дуэлях'

    def duel_crossroads(self, ctx):
        login, message = self.get_login(ctx, mess=True)
        if 'топ3' in message:
            return self.duel_top3()
        elif 'статистика' in message:
            return self.duel_statistic(login)
        else:
            return self.duel(login)
