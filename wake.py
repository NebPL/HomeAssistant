from openai import OpenAI

client = OpenAI()  # nimm deinen OPENAI_API_KEY aus der Umwelt

resp = client.audio.speech.create(
    model="tts-1",
    voice="cove",
    input="Hallo, wie geht es dir heute?"
)

# raw audio bytes holen und abspeichern
with open("cove_output.wav", "wb") as f:
    f.write(resp.audio)
