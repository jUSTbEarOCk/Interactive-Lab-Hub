
import time
import pi_servo_hat

# Initialize Servo
servo = pi_servo_hat.PiServoHat()
servo.restart()

SERVO_CHANNEL = 0

# Adjustable positions
HOME = 90
STRAWBERRY =45
MATCHA = 135

def rotate(angle):
    servo.move_servo_position(SERVO_CHANNEL, angle)
    time.sleep(1)

try:
    rotate(HOME)

    while True:
        print("\n===== LATTE PALETTE =====")
        print("1. Strawberry Latte")
        print("2. Matcha Latte")
        print("q. Quit")

        choice = input("Choose your latte: ").strip().lower()

        if choice == "q":
            break

        if choice == "1":
            name = "Strawberry Latte"
            angle = STRAWBERRY
        elif choice == "2":
            name = "Matcha Latte"
            angle = MATCHA
        else:
            print("Invalid choice!")
            continue

        print(f"\nYou selected {name}")
        print("Rotating coaster...")
        rotate(angle)

        print("Coaster is ready!")

        while True:
            ready = input("Have you placed your cup? (y/n): ").strip().lower()
            if ready in ("y", "yes"):
                break
            print("Place your cup and enter y when ready.")

        print(f"\nYour {name} is ready!")
        print("Enjoy your latte!")

        input("\nRemove the cup and press Enter to continue...")
        rotate(HOME)

finally:
    rotate(HOME)
    print("\nLatte Palette stopped.")

