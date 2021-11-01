import config
import utils
import socket
import re
import time


def main():
    s = socket.socket()
    s.connect((config.HOST, config.PORT))
    s.send("PASS {}\r\n".format(config.PASS).encode('UTF-8'))
    s.send("NICK {}\r\n".format(config.NICK).encode('UTF-8'))
    s.send("JOIN {}\r\n".format(config.CHAN).encode('UTF-8'))

    chat_message = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
    # utils.mess(s, 'Драсте')
    count = 0
    while True:
        count += 1
        print(count)
        response = s.recv(4096).decode('UTF-8')
        if response == 'PING :tmi.twitch.tv\r\n':
            print(response, 'in if')
            s.send('PONG :tmi.twitch.tv\r\n'.encode('UTF-8'))
        else:
            username = re.search(r"\w+", response).group(0)
            message = chat_message.sub("", response)
            print(username, response)
            if message.strip() == '!time':
                utils.mess(s, f"@{username} it's time to stop!")
        time.sleep(1)


if __name__ == "__main__":
    main()
