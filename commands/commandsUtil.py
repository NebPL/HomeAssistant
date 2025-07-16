from text_to_num import text2num
from TTS.api import TTS
import sounddevice as sd
import numpy as np
import subprocess
import tempfile
import os
import platform
from pydub import AudioSegment


# def say(text: str):
#    model_path = "models/de_DE-pavoque-low.onnx"
#    config_path = "models/de_DE-pavoque-low.onnx.json"
#
#    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_wav:
#        wav_path = tmp_wav.name
#
#    cmd = [
#        "piper",
#        "-m", model_path,
#        "-c", config_path,
#        "-t", text,
#        "-f", wav_path
#    ]
#
#    subprocess.run(cmd, check=True)
#
#    audio = AudioSegment.from_wav(wav_path)
#
#    # Stimme etwas höher und schneller (5% schneller)
#    new_frame_rate = int(audio.frame_rate * 0.95)
#    pitched_audio = audio._spawn(audio.raw_data, overrides={
#                                 "frame_rate": new_frame_rate})
#
#    pitched_audio.export(wav_path, format="wav")
#
#    system = platform.system()
#    try:
#        if system == "Windows":
#            subprocess.run(
#                ["powershell", "-c", f"(New-Object Media.SoundPlayer '{wav_path}').PlaySync();"], check=True)
#        elif system == "Darwin":
#            subprocess.run(["afplay", wav_path], check=True)
#        else:
#            for player in (["aplay"], ["paplay"], ["ffplay", "-autoexit", "-nodisp"]):
#                try:
#                    subprocess.run(player + [wav_path], check=True)
#                    break
#                except Exception:
#                    continue
#    except Exception as e:
#        print(f"Fehler beim Abspielen: {e}")
#
#    os.remove(wav_path)


import subprocess


def say(text: str):
    cmd = [
        "espeak",
        "-v", "de",       # deutsche Stimme
        "-s", "175",      # Geschwindigkeit etwas langsamer
        "-p", "0",       # mittlere Tonhöhe
        "-a", "150",      # etwas lauter
        text
    ]
    subprocess.run(cmd, check=True)


def SimpleCommand(Trigger, Input, Keywords):
    if not Keywords:
        print("Add Keywords!")
        pass

    for keyword in Keywords:
        if keyword in Input:
            if keyword == Keywords[-1]:
                Trigger()
                return True
        else:
            # print("Keyword " + keyword + " ist nicht im Input!")
            break


def Command(Trigger, Input, Keywords, Infos=[]):
    if not Keywords:
        print("Add Keywords!")
        return

    if not Infos:
        retrunVal = SimpleCommand(Trigger, Input, Keywords)
        return retrunVal

    for keyword in Keywords:
        if keyword not in Input:
            print(f"Keyword '{keyword}' nicht im Input.")
            return

    args = []
    words = Input.split()

    for _type, arg1, arg2 in Infos:
        if _type == "s":
            try:
                if arg2 == " ":
                    start = words.index(arg1) + 1
                    zwischen = words[start:len(words)]
                    args.append(" ".join(zwischen))
                else:
                    start = words.index(arg1) + 1
                    end = words.index(arg2)
                    zwischen = words[start:end]
                    args.append(" ".join(zwischen))
            except ValueError as e:
                args.append("__nothing__")
                # print(
                #    f"[Fehler - 's'] Wort '{arg1}' oder '{arg2}' nicht im Input gefunden.")
                # return

        elif _type == "n":
            try:
                index = words.index(arg1)
                if arg2 == "Left":
                    if index > 0:
                        leftNum = words[index - 1]
                        num = int(leftNum)
                        args.append(num)
                    else:
                        print(f"[Fehler - 'n'] Kein Wort links von '{arg1}'.")
                        return

                elif arg2 == "Right":
                    if index + 1 < len(words):
                        rightNum = words[index + 1]
                        num = int(rightNum)
                        args.append(num)
                    else:
                        print(f"[Fehler - 'n'] Kein Wort rechts von '{arg1}'.")
                        return
            except ValueError:
                args.append(-1)
                # print(f"[Fehler - 'n'] Wort '{arg1}' nicht im Input gefunden.")
                # return
            except Exception as e:
                print(f"[Fehler - 'n'] {e}")
                return
        else:
            print(f"Unbekannter Info-Typ: {_type}")
            return

    print("Argumente:", args)
    if len(args) == len(Infos):
        Trigger(*args)
        return True
    else:
        print("Fehler: Argumentanzahl stimmt nicht mit Infos überein.")
        return False
