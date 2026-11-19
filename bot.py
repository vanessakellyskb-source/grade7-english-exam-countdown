
import io
import os
from datetime import datetime, timezone, timedelta

import requests
from PIL import Image, ImageDraw, ImageFont

TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
API = f"https://api.telegram.org/bot{TOKEN}/"
TARGET = datetime(2026, 11, 26, 5, 0, tzinfo=timezone(timedelta(hours=4)))
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def telegram(method, **kwargs):
    response = requests.post(API + method, timeout=35, **kwargs)
    response.raise_for_status()
    data = response.json()
    if not data.get("ok"):
        raise RuntimeError(data)
    return data["result"]


def render():
    seconds = max(0, int((TARGET - datetime.now(timezone.utc)).total_seconds()))
    days, remainder = divmod(seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, secs = divmod(remainder, 60)

    image = Image.new("RGB", (1200, 675), "#191d58")
    draw = ImageDraw.Draw(image)

    for y in range(675):
        p = y / 674
        draw.line((0, y, 1200, y),
                  fill=(int(47-28*p), int(36+12*p), int(120-55*p)))

    def font(size):
        return ImageFont.truetype(FONT, size)

    def center(text, y, size, color):
        draw.text((600, y), text, font=font(size),
                  fill=color, anchor="mt")

    for x, y, r, color in [
        (100, 90, 9, "#ffe783"),
        (1080, 100, 9, "#7ee9ff"),
        (185, 530, 8, "#ffb6e4"),
        (1030, 540, 7, "#ffe783"),
        (920, 65, 5, "#ffffff"),
    ]:
        draw.ellipse((x-r, y-r, x+r, y+r), fill=color)

    center("GRADE 7", 48, 48, "#9feaff")
    center("END OF TERM ENGLISH EXAM", 125, 49, "#ffffff")
    center("26 NOVEMBER 2026  |  UAE TIME", 211, 29, "#ffe783")

    values = [days, hours, minutes, secs]
    labels = ["DAYS", "HOURS", "MINUTES", "SECONDS"]
    colors = ["#ffe783", "#8ff3ff", "#ffb4df", "#b9ffb0"]

    for i, (value, label, color) in enumerate(zip(values, labels, colors)):
        x = 90 + i * 260
        draw.rounded_rectangle(
            (x, 320, x+240, 495),
            radius=24,
            fill="#35447e",
            outline="#798ac7",
            width=3
        )
        draw.text((x+120, 350), f"{value:02d}",
                  font=font(85), fill=color, anchor="mt")
        draw.text((x+120, 455), label,
                  font=font(23), fill="white", anchor="mt")

    message = (
        "EXAM DAY IS HERE! YOU CAN DO IT!"
        if seconds == 0
        else "STUDY  *  PRACTISE  *  BELIEVE  *  ACHIEVE"
    )
    center(message, 550, 27, "#ffe783")
    center("Your success starts now!", 605, 22, "#d1d9ff")

    output = io.BytesIO()
    image.save(output, format="PNG")
    output.seek(0)
    return output


def find_existing_message():
    updates = telegram("getUpdates", params={"limit": 100})
    for update in reversed(updates):
        message = update.get("channel_post") or update.get("message", {})
        if str(message.get("chat", {}).get("id")) != str(CHAT_ID):
            continue
        if message.get("from", {}).get("is_bot") and \
           message.get("caption", "").startswith("Grade 7 End of Term"):
            return message["message_id"]
    return None


def main():
    photo = render()
    message_id = os.environ.get("MESSAGE_ID")

    if message_id:
        media = {
            "type": "photo",
            "media": "attach://photo",
            "caption": "Grade 7 End of Term English Exam Countdown"
        }
        telegram(
            "editMessageMedia",
            data={
                "chat_id": CHAT_ID,
                "message_id": message_id,
                "media": __import__("json").dumps(media)
            },
            files={"photo": ("countdown.png", photo, "image/png")}
        )
        print("Countdown updated.")
    else:
        result = telegram(
            "sendPhoto",
            data={
                "chat_id": CHAT_ID,
                "caption": "Grade 7 End of Term English Exam Countdown"
            },
            files={"photo": ("countdown.png", photo, "image/png")}
        )
        print("Countdown sent. Message ID:", result["message_id"])


if __name__ == "__main__":
    main()
