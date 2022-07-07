#############
# Libraries #
#############
import asyncio
import traceback
import discord
import logging
import logging
import sys
import os
import pathlib
import argparse

###########
# Modules #
###########
from . database import insert_data, create_structure
from . config import log_level, debug_guilds, discord_token
from . cogs import NotSetup

#########
# Async #
#########

# Create an event loop
event_loop = asyncio.new_event_loop()

# Set the event loop as the default asyncio event loop
asyncio.set_event_loop(event_loop)

#################
# Key Variables #
#################

# File locations
logging_location = pathlib.Path(pathlib.Path(__file__).parent.resolve() / '../logs')

# Arguments
parser = argparse.ArgumentParser(description='LMRun')
parser.add_argument('-q', '--run-migration', action=argparse.BooleanOptionalAction)

###########
# Logging #
###########
# If logging directory does not exist, create it
if logging_location.is_dir() is False:
    os.mkdir(logging_location)

# Add the name of the log file to the variable
logging_location = pathlib.Path(pathlib.Path(logging_location / 'lmrun.log'))

# If logging file does not exist, create it
if logging_location.is_file() is False:
    logging_location.touch()

# Set logging config
logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s ',
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        logging.FileHandler(logging_location),
        logging.StreamHandler()
    ]
)

# Create the log file
logger = logging.getLogger('LMRun')
logging.getLogger('sqlalchemy.engine').setLevel(getattr(logging, os.getenv('LOG_LEVEL').upper()))

# Info log that the log is starting
logger.info('Logging starting')

#############
# Arguments #
#############

# If run_migration argument is set then run the migration
if parser.parse_args().run_migration is True:
    logger.info('Starting database migration!')

    logger.info('Creating database structure!')
    event_loop.run_until_complete(create_structure())

    logger.info('Inserting required data into the database!')
    event_loop.run_until_complete(insert_data())

    logger.info('Database migration complete!')
    sys.exit(0)

########
# Bot #
#######

# Setup intents
intents = discord.Intents(guilds=True,
                          messages=True,
                          reactions=True,
                          members=True)

# Create an instance of the Discord bot
bot = discord.Bot(debug_guilds=debug_guilds, intents=intents)

# Load cogs #
bot.load_extension('lmrun.cogs.administration')
bot.load_extension('lmrun.cogs.game')


##############
# On Ready ###
##############
@bot.event
async def on_ready():
    logging.info(f'{bot.user.name} has connected to Discord!')


#################################
# Application Command exception #
#################################
@bot.event
async def on_application_command_error(ctx, exception):
    if isinstance(exception, NotSetup):
        await ctx.interaction.response.send_message("Database record not found!")
    else:
        traceback.print_exception(
            type(exception), exception, exception.__traceback__, file=sys.stderr)
        await ctx.send(f':confused: An error was raised, ask the bot devs:\n```{exception}```')

#########
# Start #
#########
event_loop.run_until_complete(bot.start(discord_token))
