import time
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789


# ---------- Set up screen ----------
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

# Portrait orientation
width = 135
height = 240
rotation = 0

# ---------- Backlight ----------
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True


# ---------- Buttons ----------
# Upper button = previous event
buttonA = digitalio.DigitalInOut(board.D23)
buttonA.switch_to_input()

# Lower button = next event
buttonB = digitalio.DigitalInOut(board.D24)
buttonB.switch_to_input()


# ---------- Fonts ----------
name_font = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    15
)

date_font = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    13
)


# ---------- Events ----------
events = [
    {
        "name": "YENA",
        "date": "Apr 25, 2026",
        "image": "yena1.jpg"
    },
    {
        "name": "YENA",
        "date": "May 23, 2026",
        "image": "yena2.jpg"
    },
    {
        "name": "Jay Park & LNGSHOT",
        "date": "Sep 11, 2026",
        "image": "jaypark&lngshot.jpg"
    },
    {
        "name": "aespa",
        "date": "Sep 18, 2026",
        "image": "aespa.jpg"
    },
    {
        "name": "BOYNEXTDOOR",
        "date": "Nov 1, 2026",
        "image": "boynextdoor.jpg"
    },
    {
        "name": "BOYNEXTDOOR",
        "date": "Nov 7, 2026",
        "image": "boynextdoor.jpg"
    }
]


# Start with first event
current_event = 0


# ---------- Function to display an event ----------
def show_event(index):

    event = events[index]

    # Black background
    screen = Image.new("RGB", (width, height), "black")
    draw = ImageDraw.Draw(screen)

    # Load poster
    poster = Image.open(event["image"]).convert("RGB")

    # Resize poster while keeping aspect ratio
    poster.thumbnail((125, 175))

    # Center poster
    poster_x = (width - poster.width) // 2
    poster_y = 5

    screen.paste(poster, (poster_x, poster_y))

    # Event name
    draw.text(
        (7, 185),
        event["name"],
        font=name_font,
        fill="white"
    )

    # Date
    draw.text(
        (7, 210),
        event["date"],
        font=date_font,
        fill="white"
    )

    # Send image to screen
    disp.image(screen, rotation)


# ---------- Show first event ----------
show_event(current_event)


# ---------- Main loop ----------
while True:

    # Upper button -> previous event
    if not buttonA.value:
        current_event -= 1

        if current_event < 0:
            current_event = len(events) - 1

        show_event(current_event)

        # Prevent one press from changing many pages
        time.sleep(0.3)

    # Lower button -> next event
    elif not buttonB.value:
        current_event += 1

        if current_event >= len(events):
            current_event = 0

        show_event(current_event)

        # Prevent one press from changing many pages
        time.sleep(0.3)

    time.sleep(0.05)