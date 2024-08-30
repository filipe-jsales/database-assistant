from lib.initialization.bot import init as run
from lib.initialization.session import init as session_initialization
from lib.initialization.audio import init_rvc, init_pyttsx3
from lib.initialization.driver import init as driver_initialization

use_audio = False

driver = driver_initialization()
session_initialization(driver)
engine = None
rvc = None
if use_audio:
    engine = init_pyttsx3()
    rvc = init_rvc()

run("Boa tarde", "Pubzinho Season 7", rvc, driver, engine, use_audio)