import pyaudio
import wave
import whisper
import keyboard

def record_audio(whisper_model):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "output.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    #for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        #data = stream.read(CHUNK)
        #frames.append(data)

    while True:
        data = stream.read(CHUNK)
        frames.append(data)
        if keyboard.is_pressed("a"):
            break
        if keyboard.is_pressed("q"):
            quit()

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    audio = whisper.load_audio("output.wav")
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(whisper_model.device)
    options = whisper.DecodingOptions(language="en")
    result = whisper.decode(whisper_model, mel, options)

    return result.text