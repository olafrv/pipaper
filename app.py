#!/usr/bin/python

import sys
import signal
import logging
import time
from waveshare.lib.waveshare_epd import epd2in13_V4

logging.basicConfig(level=logging.DEBUG)

# https://www.waveshare.com/wiki/2.13inch_e-Paper_HAT_Manual#Working_With_Raspberry_Pi
# Power On
# Cycle:
#   Init & Clear
#   Partial Refresh <= Max. 5
#     Init & Clear (Full)
#     Full Refresh <= Min. 180s, Max. 24h
# Init & Clear
# Sleep
# Power Off
# Border Color <= VCOM AND DATA INTERVAL SETTING

epd = None


def handle_signal(signum, frame):
    logging.info(f"Received signal {signum}, cleaning up...")
    epd2in13_V4.epdconfig.module_exit(cleanup=True)
    sys.exit(0)


signal.signal(signal.SIGINT, handle_signal)  # Ctrl+C
signal.signal(signal.SIGTERM, handle_signal)  # Termination


def get_image():
    return None


def __main__():
    try:
        epd = epd2in13_V4.EPD()
        epd.init()
        epd.clear()

        fast_count = 0
        while True:

            if fast_count == 60:
                # Full refresh
                fast_count = 0
                epd.init()
                epd.clear()
                epd.display(epd.getbuffer(get_image()))
            else:
                # Fast refresh
                fast_count += 1
                epd.init_fast()
                epd.display_fast(epd.getbuffer(get_image()))

            epd.sleep()
            time.sleep(60)  # 1 minute

    except IOError as e:
        logging.info(e)
