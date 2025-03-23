#!/usr/bin/env python3

import os
import datetime
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_image_blank(width: int = 250, height: int = 122) -> Image:
    return Image.new("1", (width, height), 255)  # bg 1-bit color (monochrome)


def get_image(width: int = 250,
              height: int = 122,
              rotation: int = 0,
              weather_emoji: str = "⛓️‍💥") -> Image:

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

    # Draw the text elements (x,y) on the background
    # Margins due to case and screen border differences
    x_margin = 10
    y_margin = 10
    draw.text((x_margin + 15, y_margin + 10),
              weather_emoji, font=emoji_font, fill=0)
    draw.text((x_margin + 85, y_margin + 10),
              current_time, font=time_font, fill=0)
    draw.text((x_margin + 55, y_margin + 70),
              current_date, font=date_font, fill=0)
    if rotation != 0:
        image = image.rotate(rotation, expand=True)

    return image


if __name__ == "__main__":
    # Rnning this script will generate an image file for testing
    image_file = os.path.join(BASE_DIR, "../../tmp/weather_display.png")
    print(f"Drawing to: {image_file}")
    image = get_image()
    image.save(image_file)
