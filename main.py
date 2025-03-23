#!/usr/bin/python

import os
import sys
import signal
import logging
from time import sleep
from dotenv import load_dotenv   # type: ignore
from lib.waveshare.lib.waveshare_epd import epd2in13_V4
from lib.weatherapi import get_weather_emoji
from display_ws2in13_V4 import get_image, get_image_blank

logging.basicConfig(level=logging.INFO)

EXIT_SUCCESS = 0
EXIT_FAILURE = 1
SECOND = 1            # 1 second
MINUTE = 60 * SECOND  # 60 seconds
HOUR = 60 * MINUTE    # 60 minutes
DAY = 24 * HOUR       # 24 hours


epd = epd2in13_V4.EPD()


def safe_exit(code):
    logging.info("Exiting safely...")
    blank_image = get_image_blank()
    epd.init_fast()
    epd.display_fast(epd.getbuffer(blank_image))
    epd.sleep()
    epd2in13_V4.epdconfig.module_exit(cleanup=True)
    sys.exit(code)


def handle_signal(signum, frame):
    logging.info(f"Received signal {signum} ...")
    safe_exit(EXIT_SUCCESS)


signal.signal(signal.SIGINT, handle_signal)   # Ctrl + C
signal.signal(signal.SIGTERM, handle_signal)  # Termination


def main():

    load_dotenv()
    width = int(os.getenv("EPAPER_WIDTH"))
    height = int(os.getenv("EPAPER_HEIGHT"))

    try:
        logging.info("Initializing display...")
        epd.init()
        epd.Clear(0xFF)

        seconds_since_last_refresh = 0

        while True:

            logging.info("Seconds since last refresh: %d",
                         seconds_since_last_refresh)

            try:
                logging.info("Checking the weather...")
                weather_emoji = get_weather_emoji(
                    os.getenv("WEATHER_API_KEY"),
                    os.getenv("WEATHER_API_LAT"),
                    os.getenv("WEATHER_API_LON"),
                )
            except Exception as e:
                logging.error(e, exc_info=True)

            logging.info("Generating image...")
            image = get_image(width, height, 180, weather_emoji)

            if seconds_since_last_refresh >= HOUR:
                logging.info("Full refresh...")
                seconds_since_last_refresh = 0
                epd.init()
                epd.display(epd.getbuffer(image))
            else:
                logging.info("Partial refresh...")
                seconds_since_last_refresh += MINUTE
                epd.init_fast()
                epd.display_fast(epd.getbuffer(image))

            logging.info(f"Sleeping {MINUTE}s...")
            epd.sleep()  # avoid high voltage (risk of damage)!
            sleep(MINUTE)

    except Exception as e:
        logging.error(e, exc_info=True)
        safe_exit(EXIT_FAILURE)


if __name__ == "__main__":
    main()
