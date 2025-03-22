#!/usr/bin/env python3

# WaveShare 2.13inch e-Paper HAT (V4) display image generator
# https://www.waveshare.com/wiki/2.13inch_e-Paper_HAT_(B)

import os
import datetime
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_image(width: int = 250,
              height: int = 122,
              weather_emoji: str = "☀️") -> Image:

    image = Image.new("1", (width, height), 255)  # bg 1-bit color (monochrome)
    draw = ImageDraw.Draw(image)

    # Format the current date and time
    current_time = datetime.datetime.now().strftime("%H:%M")
    current_date = datetime.datetime.now().strftime("%a, %b %d")
    # Add suffix for the day (e.g., "1st", "2nd", "3rd")
    day = int(datetime.datetime.now().strftime("%d"))
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day % 10 - 1]
    current_date = current_date + suffix

    # Load fonts (using DejaVu Sans)
    try:
        time_font = ImageFont.truetype(
            os.path.join(BASE_DIR, "fonts/DejaVuSans.ttf"), 50)
        date_font = ImageFont.truetype(
            os.path.join(BASE_DIR, "fonts/DejaVuSans.ttf"), 20)
        if weather_emoji is not None:
            emoji_font = ImageFont.truetype(
                os.path.join(BASE_DIR, "fonts/NotoEmoji-Regular.ttf"), 50)
    except IOError:
        time_font = ImageFont.load_default()
        date_font = ImageFont.load_default()
        emoji_font = ImageFont.load_default()

    # Draw the text elements on the background
    draw.text((15, 30), weather_emoji, font=emoji_font, fill=0) 
    draw.text((85, 30), current_time, font=time_font, fill=0)
    draw.text((55, 90), current_date, font=date_font, fill=0)

    return image

if __name__ == "__main__":
    image_file = os.path.join(BASE_DIR, "tmp/weather_display.png")
    print("Drawing...")
    image = get_image()
    print("Saving... ", image_file)
    image.save(image_file)
