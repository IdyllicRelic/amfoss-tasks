import time
from datetime import datetime
from subprocess import run

from PIL import Image, ImageDraw, ImageFont
from screeninfo import get_monitors


def main():
    TEXT_COLOR = (255, 255, 255)
    BACKGROUND_COLOR = (240, 100, 111)
    while True:
        with open("file.txt") as f:
            text = f.read()
        width = 0
        height = 0
        for monitor in get_monitors():
            width = monitor.width
            height = monitor.height

        img = Image.new("RGB", (width, height), color=BACKGROUND_COLOR)
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default(size=70)

        current_time = datetime.now().strftime("%H:%M:%S")  # noqa: DTZ005

        draw.text((10, 30), text, fill=TEXT_COLOR, font=font)
        draw.text((width - 400, height - 300), current_time, fill=TEXT_COLOR, font=font)
        img.save("/tmp/background.png")

        run(
            [
                "gsettings",
                "set",
                "org.gnome.desktop.background",
                "picture-uri",
                "/tmp/background.png",
            ],
            check=False,
        )

        time.sleep(1)


if __name__ == "__main__":
    main()
