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
        "image": "yena.jpg"
    },
    {
        "name": "YENA",
        "date": "May 23, 2026",
        "image": "yena.jpg"
    },
    {
        "name": "Yu Zhen",
        "date": "Aug 1, 2026",
        "image": "Yu Zhen.jpg"
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
        "name": "Global Citizen Festival",
        "date": "Sep 26, 2026",
        "image": "GCF.jpg"
    },
    {
        "name": "LE SSERAFIM",
        "date": "Oct 8, 2026",
        "image": "le sserafim.jpg"
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


current_event = 0

# Used for scrolling long names
scroll_x = 7
last_scroll = time.time()


# ---------- Draw event ----------
def show_event(index, name_x=7):

    event = events[index]

    # Black background
    screen = Image.new("RGB", (width, height), "black")
    draw = ImageDraw.Draw(screen)

    # Load poster
    poster = Image.open(event["image"]).convert("RGB")

    # Resize while keeping aspect ratio
    poster.thumbnail((125, 175))

    # Center poster
    poster_x = (width - poster.width) // 2
    poster_y = 5

    screen.paste(poster, (poster_x, poster_y))

    # Event name
    draw.text(
        (name_x, 185),
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

    disp.image(screen, rotation)


# ---------- Get name width ----------
def get_name_width(name):
    box = name_font.getbbox(name)
    return box[2] - box[0]


# ---------- First event ----------
show_event(current_event)


# ---------- Main loop ----------
while True:

    # Previous event
    if not buttonA.value:

        current_event -= 1

        if current_event < 0:
            current_event = len(events) - 1

        scroll_x = 7
        show_event(current_event, scroll_x)

        # Wait until button is released
        while not buttonA.value:
            time.sleep(0.01)

        time.sleep(0.1)


    # Next event
    elif not buttonB.value:

        current_event += 1

        if current_event >= len(events):
            current_event = 0

        scroll_x = 7
        show_event(current_event, scroll_x)

        # Wait until button is released
        while not buttonB.value:
            time.sleep(0.01)

        time.sleep(0.1)


    # ---------- Scroll long event names ----------
    event_name = events[current_event]["name"]
    text_width = get_name_width(event_name)

    # Only scroll if the name is wider than the screen
    if text_width > width - 14:

        if time.time() - last_scroll > 0.05:

            scroll_x -= 1

            # Once the whole name disappears,
            # start again from the right
            if scroll_x < -text_width:
                scroll_x = width

            show_event(current_event, scroll_x)

            last_scroll = time.time()


    time.sleep(0.01)