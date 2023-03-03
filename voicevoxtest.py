import pyaudio
import wave

# set up PyAudio
p = pyaudio.PyAudio()

# open a stream with the desired audio parameters
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=26000,
                input=True,
                input_device_index=3,
                output=True)

# open the audio file
wf = wave.open('voice.wav', 'rb')

# read the audio data in chunks and write it to the stream
chunk_size = 1024
data = wf.readframes(chunk_size)
while data:
    stream.write(data)
    data = wf.readframes(chunk_size)

# close the audio file and the PyAudio stream
wf.close()
stream.stop_stream()
stream.close()
p.terminate()
