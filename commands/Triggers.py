import threading
from time import sleep
import requests
from aiohttp import client
from . import commandsUtil
from datetime import datetime
import pyttsx3
from playsound import playsound


def hallo():
    commandsUtil.say("Hallo zusammen. Ich bin der Computer")


def Uhr():
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    text = f"Die aktuelle Uhrzeit ist {current_time}"
    commandsUtil.say(text)


def Timer(stunden, stunde, minuten, minute, sekunden, sekunde):

    if stunden < 0:
        stunden += 1
    if stunde < 0:
        stunde += 1

    if minuten < 0:
        minuten += 1
    if minute < 0:
        minute += 1

    if sekunden < 0:
        sekunden += 1
    if sekunde < 0:
        sekunde += 1

    stunden = stunden+stunde
    minuten = minuten+minute
    sekunden = sekunden+sekunde

    sekunden = stunden*3600+minuten*60+sekunden
    if sekunden <= 0:
        commandsUtil.say(
            "Du musst eine anzahl sekunden, minuten oder Stunden sagen!")
        return

    TimerThread = threading.Thread(target=setTimer, args=(sekunden,))
    commandsUtil.say("Timer gestartet")
    TimerThread.start()


def setTimer(sekunden):

    for i in range(sekunden):
        print(i)
        sleep(1)

    playsound("TimerAlarm.mp3")
    commandsUtil.say("Timer fertig")
    sleep(4)
    return True


def weather():
    lat, lon = 47.3769, 8.5417

# Anfrage an Open-Meteo
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&hourly=temperature_2m"
        f"&timezone=auto"
    )

    response = requests.get(url)
    data = response.json()

# Heutiges Datum (z. B. '2025-06-29')
    heute = datetime.now().date().isoformat()

# Liste der Temperaturen von heute
    temperaturen = [
        temp for time, temp in zip(data["hourly"]["time"], data["hourly"]["temperature_2m"])
        if time.startswith(heute)
    ]

# Durchschnitt berechnen
    if temperaturen:
        avg_temp = sum(temperaturen) / len(temperaturen)
    text = f"Durchschnittstemperatur heute: {avg_temp:.1f}°C"
    commandsUtil.say(text)
    return True
