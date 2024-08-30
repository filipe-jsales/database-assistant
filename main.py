from lib.initialization.bot import init as run
from lib.initialization.session import init as session_initialization
from lib.initialization.audio import init as audio_initialization
from lib.initialization.driver import init as driver_initialization

use_audio = False

driver = driver_initialization()
session_initialization(driver)
engine = audio_initialization(use_audio)

run("Aê!", "Pubzinho Season 7", driver, engine, use_audio)