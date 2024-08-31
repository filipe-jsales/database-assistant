import os
try:
    import pyttsx3
    from rvc_python.infer import RVCInference
    from pygame import mixer
except ImportError:
    print("Bibliotecas de áudio não instaladas.")


from dotenv import load_dotenv

load_dotenv()

def init_pyttsx3():
    mixer.init(devicename=os.getenv("WINDOWS_AUDIO_VIRTUAL_MIC_NAME"))
    return pyttsx3.init()

def init_rvc():
    directory = os.getcwd() + os.getenv("AI_MODEL_DIRECTORY_PATH")
    rvc = RVCInference(device="cuda:0")
    rvc.set_models_dir(directory)
    return rvc