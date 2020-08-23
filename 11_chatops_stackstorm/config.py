import logging

# This is a minimal configuration to get you started with the Text mode.
# If you want to connect Errbot to chat services, checkout
# the options in the more complete config-template.py from here:
# https://raw.githubusercontent.com/errbotio/errbot/master/errbot/config-template.py

BACKEND = 'Slack'  # Errbot will start in text mode (console only mode) and will answer commands from there.
BOT_IDENTITY = {
    'token': '<token>'
}
BOT_DATA_DIR = r'/home/michal/temp/11_chatops_stackstorm/data'
BOT_EXTRA_PLUGIN_DIR = r'/home/michal/temp/11_chatops_stackstorm/plugins'
BOT_PLUGIN_INDEXES = r'/home/michal/temp/11_chatops_stackstorm/repos.json'
#BOT_PLUGIN_INDEXES = r'https://errbot.readthedocs.io/en/latest/repos.json'
BOT_LOG_FILE = r'/home/michal/temp/11_chatops_stackstorm/errbot.log'
BOT_LOG_LEVEL = logging.DEBUG

BOT_ADMINS = ('@CHANGE_ME', )  # !! Don't leave that to "@CHANGE_ME" if you connect your errbot to a chat system !!

STACKSTORM = {
    'auth_url': 'http://localhost/auth/v1',
    'api_url': 'http://localhost/api/v1',
    'stream_url': 'http://localhost/stream/v1',
    'route_key': 'errbot',
    'plugin_prefix': 'st2',
    'verify_cert': True,
    'secrets_store': 'cleartext',
    'api_auth': {
        'user': {
            'name': 'st2admin',
            'password': "Ch@ngeMe",
        },
    },
    'rbac_auth': {
        'standalone': {},
    },
    'timer_update': 900, #  Unit: second.  Interval to check the user token is still valid.
}
