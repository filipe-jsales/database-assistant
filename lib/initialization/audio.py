import os

import pyttsx3
from dotenv import load_dotenv
from pygame import mixer
from rvc_python.infer import RVCInference

load_dotenv()

def init_pyttsx3():
    mixer.init(devicename=os.getenv("WINDOWS_AUDIO_VIRTUAL_MIC_NAME"))
    return pyttsx3.init()

def init_rvc():
    directory = os.getcwd() + os.getenv("AI_MODEL_DIRECTORY_PATH")
    rvc = RVCInference(device="cuda:0")
    rvc.set_models_dir(directory)
    return rvc