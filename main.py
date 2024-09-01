import datetime

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

def get_time_of_day():
    # Get the current time
    now = datetime.datetime.now()

    # Extract the hour
    hour = now.hour

    # Determine the time of day
    if 5 <= hour < 12:
        return "Bom dia"
    elif 12 <= hour < 17:
        return "Boa tarde"
    elif 17 <= hour < 23:
        return "Boa noite"
    else:
        return "Madrugando..."

run(get_time_of_day(), "Pubzinho Season 7", rvc, driver, engine, use_audio)


