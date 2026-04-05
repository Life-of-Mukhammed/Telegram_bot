import requests
import time

BOT_TOKEN = "8362796729:AAGPFNHGObUtlSq35e8Oucga-rnFPfNdne4"

CHAT_IDS = [
    -1003773173322,
]

def send_text_to_all(text):
    for chat_id in CHAT_IDS:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": text
        }
        try:
            requests.post(url, data=data)
        except Exception as e:
            print("ERROR:", e)

        time.sleep(1)


def send_photo_to_all(caption, file_id):
    for chat_id in CHAT_IDS:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        data = {
            "chat_id": chat_id,
            "photo": file_id,
            "caption": caption
        }
        try:
            requests.post(url, data=data)
        except Exception as e:
            print("ERROR:", e)

        time.sleep(1)


def get_updates(offset=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    if offset:
        url += f"?offset={offset}"
    return requests.get(url).json()


def main():
    print("Bot started...")

    last_update_id = 0

    while True:
        updates = get_updates(last_update_id + 1)

        if updates.get("ok"):
            for update in updates["result"]:
                last_update_id = update["update_id"]

                if "message" not in update:
                    continue

                msg = update["message"]

                text = msg.get("text")
                caption = msg.get("caption")

                # text yoki caption birini olamiz
                content = text if text else caption

                if content and content.startswith("/post"):
                    content = content.replace("/post", "", 1).strip()

                    # 📸 Agar rasm bo‘lsa
                    if "photo" in msg:
                        photo = msg["photo"]
                        file_id = photo[-1]["file_id"]

                        send_photo_to_all(content, file_id)
                        print("PHOTO SENT")

                    # 📄 Agar faqat text bo‘lsa
                    else:
                        send_text_to_all(content)
                        print("TEXT SENT")

        time.sleep(2)


if __name__ == "__main__":
    main()
