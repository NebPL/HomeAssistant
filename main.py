from voiceEntry import start
from threading import Thread


def voiceAssitant():
    start()


if __name__ == '__main__':
    voiceAssitantThread = Thread(target=voiceAssitant)
    voiceAssitantThread.start()
