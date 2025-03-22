import os
import datetime
from PIL import Image, ImageDraw, ImageFont
from weatherapi.weatherapi import get_weather_emoji
from dotenv import load_dotenv

load_dotenv()

WIDTH = int(os.getenv("EPAPER_WIDTH"))
HEIGHT = int(os.getenv("EPAPER_HEIGHT"))

weather_emoji = get_weather_emoji(
    os.getenv("WEATHER_API_KEY"),
    os.getenv("WEATHER_API_LAT"),
    os.getenv("WEATHER_API_LON")
)

# Create a blank image (white background)
image = Image.new("1", (WIDTH, HEIGHT), 255)
draw = ImageDraw.Draw(image)

# Get current time
current_time = datetime.datetime.now().strftime("%H:%M")

# Load font (using DejaVu Sans)
try:
    font = ImageFont.truetype("fonts/DejaVuSans.ttf", 50)
    emoji_font = ImageFont.truetype("fonts/NotoEmoji-Regular.ttf", 50)
except IOError:
    font = ImageFont.load_default()
    emoji_font = ImageFont.load_default()

# Draw weather emoji on image
draw.text((15, 30), weather_emoji, font=emoji_font, fill=0)

# Draw time on image
draw.text((85, 30), current_time, font=font, fill=0)

# Save or show the image
image.save("./tmp/weather_display.png")