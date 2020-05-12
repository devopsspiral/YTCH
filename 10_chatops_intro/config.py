import logging

# This is a minimal configuration to get you started with the Text mode.
# If you want to connect Errbot to chat services, checkout
# the options in the more complete config-template.py from here:
# https://raw.githubusercontent.com/errbotio/errbot/master/errbot/config-template.py

BACKEND = 'Slack'
BOT_IDENTITY = {
    'token': '<bot token>'
}
BOT_DATA_DIR = r'/home/michal/temp/chatops/data'
BOT_EXTRA_PLUGIN_DIR = r'/home/michal/temp/chatops/plugins'
BOT_PLUGIN_INDEXES = r'/home/michal/temp/chatops/repos.json'
BOT_LOG_FILE = r'/home/michal/temp/chatops/errbot.log'
BOT_LOG_LEVEL = logging.DEBUG

BOT_ADMINS = ('@CHANGE_ME', )  # !! Don't leave that to "@CHANGE_ME" if you connect your errbot to a chat system !!