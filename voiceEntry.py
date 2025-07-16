import vosk
import sounddevice as sd
import sys
import queue
import json
import pvporcupine
import struct
import threading
import time
from playsound import playsound

from commands.commandsList import execCommands

# === Globale Variablen ===
q = queue.Queue()
audio_buffer = []  # Puffer für Audio vor Wake Word
stt_active = False

ACCESKEY = "BkoLjs6Gz7fK4Xl2bMP7Xged91FrgJrJhi4AOsY1dMDVAuKMdhllRQ=="

# === Initialisiere Porcupine (Wake Word) ===
porcupine = pvporcupine.create(
    keywords=["computer"],
    access_key=ACCESKEY
)

# === Initialisiere Vosk-Modell ===
model = vosk.Model(
    "/Users/ben/home/programming/personal/HomeAssistant/vosk-modle")
recognizer = vosk.KaldiRecognizer(model, 16000)

# === Audio Callback für Wake Word + STT ===


def audio_callback(indata, frames, time_info, status):
    global stt_active, audio_buffer

    if status:
        print(status, file=sys.stderr)

    # Konvertiere cffi-Buffer zu Bytes
    pcm_data = bytes(indata)

    if not stt_active:
        # Nur Wake Word aktiv: analysiere Porcupine
        audio_buffer.append(pcm_data)
        if len(audio_buffer) > 5:  # ca. 200 ms Puffer
            audio_buffer.pop(0)

        # Umwandeln in Shorts für Porcupine
        pcm = struct.unpack_from("h" * frames, pcm_data)
        result = porcupine.process(pcm)

        if result >= 0:
            print("Wake Word erkannt!")
            stt_active = True
            playsound('Wakeup.mp3')

            # STT vorbereiten – vorherige Frames anhängen
            for b in audio_buffer:
                q.put(b)
            audio_buffer.clear()

    else:
        # STT aktiv: direkt an Vosk weiterleiten
        q.put(pcm_data)

# === Thread für STT-Verarbeitung ===


def stt_loop():
    global stt_active

    while True:
        if stt_active:
            try:
                data = q.get(timeout=5)
            except queue.Empty:
                continue

            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                text = json.loads(result).get("text", "")
                if text:
                    print("Erkannt:", text)
                    execCommands(text)
                    stt_active = False
                    recognizer.Reset()  # Setze den Recognizer zurück
                    while not q.empty():  # Leere die Warteschlange
                        q.get()
            else:
                partial = json.loads(
                    recognizer.PartialResult()).get("partial", "")
                if partial:
                    print("…", partial)

# === Startfunktion ===


def start():
    print("gestarted")
    stt_thread = threading.Thread(target=stt_loop, daemon=True)
    stt_thread.start()

    with sd.RawInputStream(
        samplerate=16000,
        blocksize=porcupine.frame_length,
        dtype='int16',
        channels=1,
        callback=audio_callback
    ):
        print("Warte auf Wake Word...")
        while True:
            time.sleep(0.1)
