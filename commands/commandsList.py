from . import commandsUtil
from . import Triggers
from playsound import playsound
from text_to_num import text2num


def convert_text2num(text):
    try:
        # Versuche den gesamten Text als Zahl zu interpretieren
        zahl = text2num(text, "de")
        return str(zahl)
    except Exception:
        # Falls nicht ganze Zahl, dann splitten und Wort für Wort wandeln
        wörter = text.split()
        neu = []
        for w in wörter:
            try:
                neu.append(str(text2num(w, "de")))
            except Exception:
                neu.append(w)
        return " ".join(neu)


def execCommands(Rawinput):
    input = convert_text2num(Rawinput)
    gefunden = 0
    helpReturn = commandsUtil.SimpleCommand(
        Keywords=["sag", "hallo"], Input=input, Trigger=Triggers.hallo)
    if helpReturn == True:
        gefunden += 1

    uhrReturn = commandsUtil.SimpleCommand(
        Keywords=["uhr"], Input=input, Trigger=Triggers.Uhr)
    if uhrReturn == True:
        gefunden += 1

    timerReturn = commandsUtil.Command(
        Trigger=Triggers.Timer,
        Input=input,
        Keywords=["timer"],
        Infos=[("n", "stunden", "Left"),
               ("n", "stunde", "Left"),
               ("n", "minuten", "Left"),
               ("n", "minute", "Left"),
               ("n", "sekunden", "Left"),
               ("n", "sekunde", "Left"),
               ])
    if timerReturn == True:
        gefunden += 1

    # lichanReturn = commandsUtil.Command(
    #    Keywords=["licht", "an"], Input=input, Trigger=Triggers.lichtan)
    # if lichanReturn is not None:
    #    print("lich an")
    #    return lichanReturn

    # lichausReturn = commandsUtil.Command(
    #    Keywords=["licht", "aus"], Input=input, Trigger=Triggers.lichtaus)
    # if lichausReturn is not None:
    #    print("lich aus")
    #    return lichausReturn
    # return "Invalid Command: " + input

    if gefunden == 0:
        playsound("error.mp3")
        return
    else:
        #        playsound("success.mp3")
        return
