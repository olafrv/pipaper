#!/usr/bin/python

import os
import sys
import signal
import logging
from time import sleep
from dotenv import load_dotenv   # type: ignore
from lib.waveshare.lib.waveshare_epd import epd2in13_V4
from lib.weatherapi import get_weather_emoji
from display_ws2in13_V4 import get_image

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


def main():
    load_dotenv()
    width = int(os.getenv("EPAPER_WIDTH"))
    height = int(os.getenv("EPAPER_HEIGHT"))

    weather_emoji = get_weather_emoji(
        os.getenv("WEATHER_API_KEY"),
        os.getenv("WEATHER_API_LAT"),
        os.getenv("WEATHER_API_LON")
    )

    try:
        epd = epd2in13_V4.EPD()
        epd.init()
        epd.clear()

        fast_count = 0
        while True:

            image = get_image(width, height, weather_emoji)

            if fast_count == 60:
                # Full refresh
                fast_count = 0
                epd.init()
                epd.clear()
                epd.display(epd.getbuffer(image))
            else:
                # Fast refresh
                fast_count += 1
                epd.init_fast()
                epd.display_fast(epd.getbuffer(image))

            epd.sleep()
            sleep(60)  # 1 minute

    except IOError as e:
        logging.info(e)


if __name__ == "__main__":
    main()
