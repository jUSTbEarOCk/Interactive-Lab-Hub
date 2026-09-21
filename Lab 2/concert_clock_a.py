import time
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789


# ---------- Set up the screen ----------
cs_pin = digitalio.DigitalInOut(board.D5)
dc_pin = digitalio.DigitalInOut(board.D25)

spi = board.SPI()

disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=None,
    baudrate=64000000,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Landscape screen
height = disp.width
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

draw = ImageDraw.Draw(image)

# Font
font = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    24
)

# Turn on backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True


# ---------- Set up buttons ----------
# Upper button
buttonA = digitalio.DigitalInOut(board.D23)
buttonA.switch_to_input()

# Lower button
buttonB = digitalio.DigitalInOut(board.D24)
buttonB.switch_to_input()


# ---------- Events ----------
events = [
    {
        "name": "Jay Park & LNGSHOT",
        "date": "Sep 11, 2026"
    },
    {
        "name": "aespa",
        "date": "Sep 18, 2026"
    }
]

# Start with the first event
current_event = 0


# ---------- Main loop ----------
while True:

    # Upper button -> first event
    if not buttonA.value:
        current_event = 0

    # Lower button -> second event
    elif not buttonB.value:
        current_event = 1

    # Clear the screen
    draw.rectangle((0, 0, width, height), fill="#000000")

    # Get current event
    event = events[current_event]

    # First line: artist/event name
    draw.text(
        (10, 25),
        event["name"],
        font=font,
        fill="#FFFFFF"
    )

    # Second line: date
    draw.text(
        (10, 70),
        event["date"],
        font=font,
        fill="#FFFFFF"
    )

    # Display on physical screen
    disp.image(image, rotation)

    time.sleep(0.1)