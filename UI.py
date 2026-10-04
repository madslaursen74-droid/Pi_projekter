from gpiozero import RotaryEncoder, Button
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas
from PIL import ImageFont
from signal import pause
import time




serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)

font = ImageFont.load_default()

encoder = RotaryEncoder(17, 27, max_steps=0)
button = Button(22, pull_up=True, bounce_time=0.1)

options = ["Option 1", "Option 2"]

selected = 0
last_step = encoder.steps

def draw_menu():
    with canvas(device) as draw:
        draw.text((5, 2), "Main Menu", font=font, fill="white")

        for i, option in enumerate(options):
            y = 22 + (i * 20)

            if i == selected:
                draw.text((5, y), "> " + option, font=font, fill="black")
            else:
                draw.text((5, y), " >" + option, font=font, fill="white")


def rotated():
    global selected, last_step

    current_step = encoder.steps

    if current_step > last_step:
        selected += 1
    elif current_step < last_step:
        selected -= 1

    selected %= len(options)
    last_step = current_step

    draw_menu()


def clicked():
    with canvas(device) as draw:
        draw.text((5, 10), "Selected:", font=font, fill="white")
        draw.text((5, 30), options[selected], font=font, fill="white")

    print(f"Selected: {options[selected]}")

    time.sleep(1)

    draw_menu()


encoder.when_rotated = rotated
button.when_pressed = clicked

draw_menu()

print("Menu running...")
pause()