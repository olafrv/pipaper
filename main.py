#!/usr/bin/python

import os
import sys
import signal
import logging
from time import sleep, localtime
from dotenv import load_dotenv   # type: ignore
from lib.waveshare.lib.waveshare_epd import epd2in13_V4
from lib.image_generator.image_generator import get_image, get_image_blank
from lib.weatherapi import get_weather_emoji


EXIT_SUCCESS = 0
EXIT_FAILURE = 1
SECOND = 1            # 1 second
MINUTE = 60 * SECOND  # 60 seconds
HOUR = 60 * MINUTE    # 60 minutes
DAY = 24 * HOUR       # 24 hours


def sleep_until_next_minute():
    current_seconds = localtime().tm_sec
    seconds_to_next_minute = MINUTE - current_seconds
    sleep(seconds_to_next_minute)


def main():

    logging.basicConfig(level=logging.WARN)

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
                    os.getenv("WEATHER_API_LAT"),
                    os.getenv("WEATHER_API_LON"),
                    os.getenv("WEATHER_API_KEY"),
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
            sleep_until_next_minute()  # refresh only minute changes

    except Exception as e:
        logging.error(e, exc_info=True)
        safe_exit(EXIT_FAILURE)


if __name__ == "__main__":
    main()
