import logging
import os


def restart_tor():
    logging.info(f"Restarting tor: 'sudo killall -HUP tor'")
    res = os.system('sudo killall -HUP tor')
    logging.info(f'Restarted: {res}')
