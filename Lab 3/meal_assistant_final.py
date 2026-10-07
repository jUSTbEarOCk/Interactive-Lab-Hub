import os
import time
import random
import subprocess

import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789


# ============================================================
# DISPLAY + BUTTON SETUP
# ============================================================

# Same setup as your working Lab 2 screen test
cs_pin = digitalio.DigitalInOut(board.D5)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

BAUDRATE = 64000000

spi = board.SPI()

display = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output(value=True)

# Buttons
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)

buttonA.switch_to_input(pull=digitalio.Pull.UP)
buttonB.switch_to_input(pull=digitalio.Pull.UP)


# ============================================================
# DISPLAY HELPERS
# ============================================================

WIDTH = display.height
HEIGHT = display.width
ROTATION = 90

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

FONT = ImageFont.truetype(FONT_PATH, 18)
SMALL_FONT = ImageFont.truetype(FONT_PATH, 13)
BIG_FONT = ImageFont.truetype(FONT_PATH, 24)


def show_screen(text, font=FONT):
    image = Image.new("RGB", (WIDTH, HEIGHT), "black")
    draw = ImageDraw.Draw(image)

    draw.multiline_text(
        (10, 10),
        text,
        font=font,
        fill="white",
        spacing=5
    )

    display.image(image, ROTATION)


def wait_for_button():
    show_screen(
        "Meal Recommendation\n"
        "Assistant\n\n"
        "Press any button\n"
        "to start"
    )

    print("\nWaiting for button...")

    while True:
        if not buttonA.value or not buttonB.value:
            time.sleep(0.3)
            return

        time.sleep(0.05)


# ============================================================
# MEAL DATABASE
# ============================================================

meal_db = {
    "chicken": [
        "chicken grain bowl",
        "chicken pasta",
        "chicken wrap",
        "chicken curry",
        "chicken noodle soup",
        "chicken tacos"
    ],
    "beef": [
        "beef rice bowl",
        "beef tacos",
        "beef stir-fry",
        "beef noodles",
        "beef curry",
        "beef pasta"
    ],
    "salmon": [
        "salmon rice bowl",
        "grilled salmon with vegetables",
        "salmon pasta",
        "salmon salad",
        "salmon tacos",
        "salmon poke bowl"
    ],
    "tofu": [
        "tofu vegetable stir-fry",
        "tofu rice bowl",
        "tofu curry",
        "tofu noodles",
        "tofu salad",
        "tofu wrap"
    ],
    "egg": [
        "egg fried rice",
        "omelet",
        "egg sandwich",
        "egg noodle soup",
        "shakshuka",
        "egg rice bowl"
    ]
}


default_meals = [
    "chicken grain bowl",
    "salmon rice bowl",
    "tofu vegetable stir-fry",
    "beef tacos",
    "chicken curry",
    "salmon pasta",
    "egg fried rice",
    "beef noodles",
    "tofu curry",
    "chicken wrap",
    "beef stir-fry",
    "salmon salad"
]


# ============================================================
# TEXT TO SPEECH
# ============================================================

def speak(text):
    voices_dir = os.path.join(
        os.path.dirname(__file__),
        "voices"
    )

    output_file = "/tmp/meal_speech.wav"

    subprocess.run([
        "python3",
        "-m",
        "piper",
        "--model",
        "en_US-lessac-medium",
        "--data-dir",
        voices_dir,
        "--output-file",
        output_file,
        "--",
        text
    ])

    subprocess.run([
        "aplay",
        output_file
    ])


# ============================================================
# SPEECH TO TEXT
# ============================================================

def listen_and_transcribe():
    audio_file = "/tmp/user_input.wav"

    print("\n=== LISTENING ===")
    show_screen("Listening...", BIG_FONT)

    subprocess.run([
        "arecord",
        "-d", "5",
        "-f", "cd",
        "-c", "1",
        "-r", "16000",
        audio_file
    ])

    print("\n=== THINKING ===")
    show_screen("Thinking...", BIG_FONT)

    result = subprocess.run([
        "python3",
        "speech-scripts/transcribe.py",
        audio_file,
        "--model",
        "tiny.en"
    ],
        capture_output=True,
        text=True
    )

    print(result.stdout)

    lines = [
        line.strip()
        for line in result.stdout.splitlines()
        if line.strip()
    ]

    if lines:
        transcription = lines[0]
    else:
        transcription = ""

    print("You said:", transcription)

    return transcription.lower()


# ============================================================
# MEAL LOGIC
# ============================================================

def get_meal_pool(user_text):
    for ingredient in meal_db:
        if ingredient in user_text:
            print("Detected ingredient:", ingredient)
            return meal_db[ingredient]

    print("No specific ingredient detected.")
    return default_meals


def choose_three(meal_pool, used_meals):
    available = [
        meal for meal in meal_pool
        if meal not in used_meals
    ]

    if len(available) < 3:
        used_meals.clear()
        available = meal_pool.copy()

    meals = random.sample(available, 3)
    used_meals.update(meals)

    return meals


def user_rejected(text):
    rejection_words = [
        "no",
        "none",
        "nope",
        "not really",
        "something else",
        "another",
        "different"
    ]

    return any(
        phrase in text
        for phrase in rejection_words
    )


# ============================================================
# MAIN CONVERSATION
# ============================================================

def run_meal_assistant():
    wait_for_button()

    show_screen(
        "Let's find\n"
        "your meal!",
        BIG_FONT
    )

    speak(
        "Thinking about what to eat today? "
        "Is there any ingredient you feel like having?"
    )

    user_text = listen_and_transcribe()

    meal_pool = get_meal_pool(user_text)

    used_meals = set()

    while True:
        print("\n=== THINKING ===")
        show_screen("Thinking...", BIG_FONT)

        time.sleep(0.5)

        meals = choose_three(
            meal_pool,
            used_meals
        )

        print("\n=== RECOMMENDATIONS ===")
        for meal in meals:
            print("-", meal)

        screen_text = (
            "How about:\n\n"
            f"1. {meals[0]}\n"
            f"2. {meals[1]}\n"
            f"3. {meals[2]}"
        )

        show_screen(
            screen_text,
            SMALL_FONT
        )

        recommendation = (
            f"How about {meals[0]}, "
            f"{meals[1]}, "
            f"or {meals[2]}?"
        )

        speak(recommendation)
        speak("Do any of these sound good?")

        answer = listen_and_transcribe()

        if user_rejected(answer):
            show_screen(
                "No problem!\n\n"
                "Finding more\n"
                "options..."
            )

            speak(
                "No problem. "
                "Let me give you some other options."
            )

            continue

        show_screen(
            "Great!\n\n"
            "Enjoy your meal!",
            BIG_FONT
        )

        speak("Great. Enjoy your meal!")

        time.sleep(3)
        break


# ============================================================
# PROGRAM LOOP
# ============================================================

while True:
    run_meal_assistant()

    show_screen(
        "Meal Recommendation\n"
        "Assistant\n\n"
        "Press any button\n"
        "to start again"
    )

    while not buttonA.value or not buttonB.value:
        time.sleep(0.05)

    time.sleep(0.5)
