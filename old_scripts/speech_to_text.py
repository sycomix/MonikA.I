import io
from pydub import AudioSegment
import speech_recognition as sr
import whisper
import tempfile
import os
import torch
import numpy as np


def stt(model="base", english=True, verbose=False, energy=300, pause=1, dynamic_energy=False, save_file=False):
    if save_file:
        temp_dir = tempfile.mkdtemp()
        save_path = os.path.join(temp_dir, "temp.wav")
    #there are no english models for large
    if model != "large" and english:
        model = f"{model}.en"
    audio_model = whisper.load_model(model)    

    #load the speech recognizer and set the initial energy threshold and pause threshold
    r = sr.Recognizer()
    r.energy_threshold = energy
    r.pause_threshold = pause
    r.dynamic_energy_threshold = dynamic_energy

    with sr.Microphone(sample_rate=16000) as source:
        #get and save audio to wav file
        audio = r.listen(source)
        if save_file:
            data = io.BytesIO(audio.get_wav_data())
            audio_clip = AudioSegment.from_file(data)
            audio_clip.export(save_path, format="wav") 
            audio_data = save_path               
        else:
            torch_audio = torch.from_numpy(np.frombuffer(audio.get_raw_data(), np.int16).flatten().astype(np.float32) / 32768.0)
            audio_data = torch_audio

        if english:
            result = audio_model.transcribe(audio_data,language='english')
        else:
            result = audio_model.transcribe(audio_data)

        return result['text']
