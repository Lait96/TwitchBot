import config


def mess(sock, message):
    sock.send("PRIVMSG #{} :{}\r\n".format(config.CHAN, message).encode('UTF-8'))
