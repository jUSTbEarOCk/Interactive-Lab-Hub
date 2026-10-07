import random
import subprocess
import os

# ----------------------------
# Meal database
# ----------------------------

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


# ----------------------------
# Text-to-speech
# ----------------------------

def speak(text):
    voices_dir = os.path.join(os.path.dirname(__file__), "voices")

    subprocess.run([
        "python3",
        "-m",
        "piper",
        "--model",
        "en_US-lessac-medium",
        "--data-dir",
        voices_dir,
        "--output-file",
        "/tmp/meal_speech.wav",
        "--",
        text
    ])

    subprocess.run([
        "aplay",
        "/tmp/meal_speech.wav"
    ])


# ----------------------------
# Record + transcribe
# ----------------------------

def listen_and_transcribe():
    audio_file = "/tmp/user_input.wav"

    print("\nListening...")

    subprocess.run([
        "arecord",
        "-d", "5",
        "-f", "cd",
        "-c", "1",
        "-r", "16000",
        audio_file
    ])

    print("Thinking...")

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

    # transcribe.py prints transcription first,
    # so take the first non-empty line
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


# ----------------------------
# Meal recommendation logic
# ----------------------------

def get_meal_pool(user_text):
    for ingredient in meal_db:
        if ingredient in user_text:
            print(f"Detected ingredient: {ingredient}")
            return meal_db[ingredient]

    print("No specific ingredient detected.")
    return default_meals


# ----------------------------
# Main conversation
# ----------------------------

speak(
    "Thinking about what to eat today? "
    "Is there any ingredient you feel like having?"
)

user_text = listen_and_transcribe()

meal_pool = get_meal_pool(user_text)

used_meals = set()

while True:

    available_meals = [
        meal for meal in meal_pool
        if meal not in used_meals
    ]

    if len(available_meals) < 3:
        used_meals.clear()
        available_meals = meal_pool.copy()

    meals = random.sample(available_meals, 3)
    used_meals.update(meals)

    recommendation = (
        f"How about {meals[0]}, "
        f"{meals[1]}, "
        f"or {meals[2]}?"
    )

    print("\nRecommendations:")
    for meal in meals:
        print("-", meal)

    speak(recommendation)

    speak("Do any of these sound good?")

    answer = listen_and_transcribe()

    rejection_words = [
        "no",
        "none",
        "nope",
        "something else",
        "not really"
    ]

    rejected = any(
        phrase in answer
        for phrase in rejection_words
    )

    if rejected:
        speak("No problem. Let me give you some other options.")
        continue

    speak("Great. Enjoy your meal!")
    break
