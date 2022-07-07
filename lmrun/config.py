from pathlib import Path
import environs
import logging
import sys
##################
### Predefined ###
##################


###################
### Environment ###
###################

environment_file = Path(Path().absolute() / '.env')

# If environment file does not exist, exit
if environment_file.is_file() is False:
    sys.exit('Could not find .env file! ')

# Load the environment file
environment = environs.Env()
environment.read_env(environment_file, False)

# Environment file casting
discord_token = environment.str('DISCORD_TOKEN')
database_url = environment.str('DATABASE_URL')
log_level = getattr(logging, environment.str('LOG_LEVEL').upper())
debug_guilds = environment.list('DEBUG_GUILDS')