import signal
import os
import sys
import dcdb
from config import configs
from pyclient import PyClient
from discord import Intents

TESTING_PRINT_TO_CONSOLE = True
DELETE_DATABASE = True 

def signal_handler(sig, frame):
    if TESTING_PRINT_TO_CONSOLE:
        print(f'Signal Recieved: {sig}')
        if DELETE_DATABASE: 
            dcdb.db_delete()
    else:
        if TESTING_PRINT_TO_CONSOLE:
            print('failed to destroy database')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

dcdb.sql_init_schema()

intents = Intents.default();
intents.message_content = True
intents.members = True
intents.dm_messages = True
intents.voice_states = True
intents.guilds = True

client = PyClient(command_prefix=";", intents=intents)

client.run(configs.get("BOT_TOKEN"))
