from _includes import config
config.create_listener = True

from _includes.listener import server_thread
server_thread.start()