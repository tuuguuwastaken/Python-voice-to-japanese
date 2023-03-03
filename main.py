import speech_recognition as sr
from voicevox import Client
import asyncio
import os
import pyaudio
import wave
import keyboard
from google.cloud import translate_v2 as translate
r = sr.Recognizer()

path_to_cred = "path to json credentials for Google api"

def return_transcript():
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
    results = r.recognize_google(audio, show_all=True)
    try:
        text = r.recognize_google(audio)
        print("You said: ", text)
    except sr.UnknownValueError:
        text = "Hello it could not recognize my voice";
    except sr.RequestError as e:
        text = e
    return text

def get_translation(get):
    client = translate.Client()
    text=str(get)
    target_language = 'ja'
    result = client.translate(text, target_language=target_language)
    print(result['input'])
    print(result['translatedText'])
    return result['translatedText']

def play_audio(path):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=26000,
                    input=True,
                    input_device_index=3,
                    output=True)

    # open the audio file
    wf = wave.open('voice.wav', 'rb')

    chunk_size = 1024
    data = wf.readframes(chunk_size)
    while data:
        stream.write(data)
        data = wf.readframes(chunk_size)

    wf.close()
    stream.stop_stream()
    stream.close()
    p.terminate()



async def main(text):
    async with Client() as client:
        audio_query = await client.create_audio_query(
            text, speaker=1
        )
        with open("voice.wav", "wb") as f:
            f.write(await audio_query.synthesis())






if __name__ == "__main__":
    os.environ['GOOGLE_APPLICATION_CREDENTIALS']= path_to_cred
    while(True):
        if(keyboard.is_pressed("a")):  
            transcribed_text = return_transcript()
            yeet = get_translation(transcribed_text)
            asyncio.run(main(yeet))
            play_audio('./voice.wav')